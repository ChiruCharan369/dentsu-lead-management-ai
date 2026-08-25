
from app.services.company_resolver import normalize_company
from app.prompts.icp_prompt import ICP_PROMPT
from app.models.icp_model import ICPResponse
from app.llm.llm_client import llm
from app.db.cache_db import get_cached, save_cache

import json
import re
import os
import csv
import statistics
from typing import Tuple, Dict, Optional


def clean_json(text: str):

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    text = re.sub(r'(\w+):', r'"\1":', text)

    text = text.replace('"https"://', '"https://')
    text = text.replace('""https://', '"https://')

    text = re.sub(
        r'"ICPLinkedInURL":\s*(https?://[^",]+)',
        r'"ICPLinkedInURL": "\1"',
        text,
    )

    return text.strip()


def safe_load_json(text: str):

    try:
        return json.loads(text)
    except Exception as e:
        print("JSON ERROR:", e)
        print(text)
        return {}


def _empty_icp_response() -> ICPResponse:
    return ICPResponse(
        ICPIndustry="",
        ICPEmployeesRange="",
        ICPRevenueUSD="",
        ICPFundingType="",
        ICPFundingStage="",
        ICPFUndingAmount="",
        ICPParentCompany="",
        ICPLinkedInURL="",
        ICPMarketingSignal="",
        ICPFitStatus="Not Fit",
        ICPFitmentTest="ICP non Fitment",
        ConfidenceScore=0,
        ScoreComment="",
        ManualCheck="Manual check needed",
    )


def _set_manual_check_needed(data: dict) -> dict:
    try:
        confidence_score = int(data.get("ConfidenceScore", 0))
    except (TypeError, ValueError):
        confidence_score = 0

    data["ManualCheck"] = (
        "Manual check needed"
        if confidence_score < 70
        else "Manual check not needed"
    )
    return data


def _sanitize_icp_response(data: dict, resolved_company: str) -> dict:
    if not resolved_company:
        return {}

    sanitized = dict(data or {})
    parent_company = (sanitized.get("ICPParentCompany") or "").strip()
    if not parent_company:
        return sanitized

    if normalize_company(parent_company, "") == "":
        sanitized["ICPParentCompany"] = ""

    return sanitized


def _parse_money_to_number(s: str) -> float:
    if not s or not isinstance(s, str):
        return 0.0

    s = s.strip().replace(',', '').replace('$', '').upper()
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*([KMB]?)$", s)
    if m:
        val = float(m.group(1))
        unit = m.group(2)
        if unit == 'K':
            return val * 1_000
        if unit == 'M':
            return val * 1_000_000
        if unit == 'B':
            return val * 1_000_000_000
        return val

    num_match = re.search(r"([0-9]+(\.[0-9]+)?)", s)
    if num_match:
        try:
            return float(num_match.group(1))
        except Exception:
            return 0.0

    return 0.0


def _parse_employees_range(s: str) -> Tuple[int, int]:
    if not s or not isinstance(s, str):
        return (0, 0)

    s = s.strip().replace(',', '')
    plus = False
    if '+' in s:
        plus = True
        s = s.replace('+', '')

    parts = re.split(r"[-–—]", s)
    nums = []
    for p in parts:
        m = re.search(r"(\d+)", p)
        if m:
            nums.append(int(m.group(1)))

    if len(nums) == 0:
        return (0, 0)
    if len(nums) == 1:
        if plus:
            return (nums[0], nums[0] * 10)
        return (nums[0], nums[0])
    return (nums[0], nums[1])


def _estimate_employees_from_revenue(revenue_num: float, industry: str) -> Tuple[int, int]:
    if not revenue_num or revenue_num <= 0:
        return (0, 0)

    industry_l = (industry or "").lower()
    benchmarks = _load_dynamic_benchmarks()
    avg = benchmarks.get("__default__", 100_000)
    for k, v in benchmarks.items():
        if k == "__default__":
            continue
        if k in industry_l:
            avg = v
            break

    est = max(1, int(revenue_num / avg))
    min_est = max(1, int(est * 0.8))
    max_est = int(est * 1.25)
    return (min_est, max_est)


_DYNAMIC_BENCHMARKS: Optional[Dict[str, float]] = None


def _load_dynamic_benchmarks() -> Dict[str, float]:
    global _DYNAMIC_BENCHMARKS
    if _DYNAMIC_BENCHMARKS is not None:
        return _DYNAMIC_BENCHMARKS

    json_path = os.environ.get("REVENUE_PER_EMPLOYEE_JSON")
    if json_path and os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                _DYNAMIC_BENCHMARKS = {k.lower(): float(v) for k, v in data.items()}
                if "__default__" not in _DYNAMIC_BENCHMARKS:
                    _DYNAMIC_BENCHMARKS["__default__"] = statistics.median(list(_DYNAMIC_BENCHMARKS.values()))
                return _DYNAMIC_BENCHMARKS
        except Exception:
            pass

    cache_path = os.path.join(os.getcwd(), "icp_cache.csv")
    industry_vals: Dict[str, list] = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    raw = row.get('data') or row.get('Data') or ''
                    if not raw:
                        continue
                    try:
                        obj = json.loads(raw)
                    except Exception:
                        continue
                    ind = (obj.get('ICPIndustry') or '').strip().lower()
                    rev = _parse_money_to_number(obj.get('ICPRevenueUSD') or '')
                    emp_range = obj.get('ICPEmployeesRange') or ''
                    if not ind or rev <= 0 or not emp_range:
                        continue
                    emp_min, emp_max = _parse_employees_range(emp_range)
                    emp_mid = emp_min if emp_max == emp_min else int((emp_min + emp_max) / 2)
                    if emp_mid <= 0:
                        continue
                    rpe = rev / emp_mid
                    industry_vals.setdefault(ind, []).append(rpe)

            benchmarks_calc: Dict[str, float] = {}
            all_vals = []
            for ind, vals in industry_vals.items():
                if vals:
                    med = statistics.median(vals)
                    benchmarks_calc[ind] = max(1.0, med)
                    all_vals.extend(vals)
            if all_vals:
                benchmarks_calc['__default__'] = statistics.median(all_vals)
                _DYNAMIC_BENCHMARKS = benchmarks_calc
                return _DYNAMIC_BENCHMARKS
        except Exception:
            pass

    _DYNAMIC_BENCHMARKS = {
        'consulting': 120_000,
        'professional services': 120_000,
        'information technology': 140_000,
        'technology': 200_000,
        'saas': 220_000,
        'platforms': 220_000,
        'manufacturing': 150_000,
        'advertising': 80_000,
        'media': 60_000,
        'fintech': 180_000,
        '__default__': 100_000,
    }
    return _DYNAMIC_BENCHMARKS


def _apply_deterministic_fitment(data: dict) -> dict:
    industry = (data.get("ICPIndustry") or "").strip()
    revenue_str = (data.get("ICPRevenueUSD") or "").strip()
    employees_str = (data.get("ICPEmployeesRange") or "").strip()

    revenue_num = _parse_money_to_number(revenue_str)
    emp_min, emp_max = _parse_employees_range(employees_str)
    emp_min = emp_min or 0

    try:
        est_min, est_max = _estimate_employees_from_revenue(revenue_num, industry)
        adjusted = False
        orig_emp_str = employees_str
        if emp_min == 0 or (est_min > 0 and (emp_min < est_min * 0.5 or emp_min > est_max * 2)):
            emp_min, emp_max = est_min, est_max
            employees_str = f"{emp_min}-{emp_max}"
            data["ICPEmployeesRange"] = employees_str
            adjusted = True
    except Exception:
        adjusted = False

    threshold = 1_000_000
    near_lower = threshold * 0.95

    industry_l = industry.lower()
    is_media_or_ad = industry_l in ("media", "advertising")

    # Industry exclusion
    if is_media_or_ad:
        data["ConfidenceScore"] = 10
        data["ScoreComment"] = f"Industry {industry} excluded for ICP (Media/Advertising)."
        data["ICPFitmentTest"] = "ICP non Fitment"
        data["ICPFitStatus"] = "Not Fit"
        return data

    confidence = 50
    if re.search(r"[KM B]$", revenue_str.replace(' ', '')) or re.search(r"[KMB]", revenue_str.upper()):
        confidence += 20
    if revenue_num > 0:
        confidence += min(15, int((revenue_num / (threshold if threshold else 1)) * 5))
    else:
        confidence -= 30
    if emp_min >= 10:
        confidence += 10
    if emp_min >= 1000:
        confidence += 5

    if revenue_num >= threshold and emp_min >= 10:
        fit_test = "ICP Fitment"
        fit_status = "Good Fit"
        confidence = max(confidence, 90)
    elif revenue_num >= near_lower and revenue_num < threshold and emp_min >= 10:
        fit_test = "Near Fit"
        fit_status = "Near Fit"
        confidence = max(confidence, 75)
    else:
        fit_test = "ICP non Fitment"
        fit_status = "Not Fit"

    confidence = max(0, min(100, int(confidence)))

    if revenue_num == 0:
        comment = f"No numeric revenue found in '{revenue_str}'; low confidence ({confidence})."
    else:
        comment = f"Revenue {revenue_str} parsed as {int(revenue_num)}; confidence {confidence}."

    try:
        if adjusted:
            comment = comment + f" Employees adjusted from '{orig_emp_str}' to '{employees_str}' based on revenue and industry norms."
            confidence = min(100, confidence + 10)
    except NameError:
        pass

    data["ConfidenceScore"] = int(confidence)
    data["ScoreComment"] = comment
    data["ICPFitmentTest"] = fit_test
    data["ICPFitStatus"] = fit_status

    return data


def get_icp_data(company: str, email: str) -> ICPResponse:

    resolved_company = normalize_company(company, email)

    if not resolved_company:
        return _empty_icp_response()

    # CHECK CACHE
    cached = get_cached(resolved_company)

    if cached:

        data = json.loads(cached)
        data = _sanitize_icp_response(data, resolved_company)

        data["company"] = resolved_company
        data["email"] = email
        data = _set_manual_check_needed(data)

        print("CACHE HIT")

        # # WRITE CSV (even from cache)
        # write_structured(data)
        # write_raw(resolved_company, email, data)

        return ICPResponse(**data)

    print("LLM CALL")

    prompt = ICP_PROMPT.format(company=resolved_company)

    response = llm.invoke(prompt)

    text = clean_json(response.content)

    data = safe_load_json(text)
    data = _sanitize_icp_response(data, resolved_company)

    data = {k: (v if v else "") for k, v in data.items()}

    data["company"] = resolved_company
    data["email"] = email

    # Apply deterministic fitment scoring and consistency override
    try:
        data = _apply_deterministic_fitment(data)
    except Exception as e:
        print("Fitment computation error:", e)

    data = _set_manual_check_needed(data)

    # SAVE CACHE
    save_cache(
        resolved_company,
        json.dumps(data),
    )

    # # WRITE CSV HERE
    # write_structured(data)
    # write_raw(resolved_company, email, data)

    return ICPResponse(**data)
