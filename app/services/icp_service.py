
from app.services.company_resolver import normalize_company
from app.prompts.icp_prompt import ICP_PROMPT
from app.models.icp_model import ICPResponse
from app.llm.llm_client import llm
from app.db.cache_db import get_cached, save_cache

import json
import re


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
    )


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

    # SAVE CACHE
    save_cache(
        resolved_company,
        json.dumps(data),
    )

    # # WRITE CSV HERE
    # write_structured(data)
    # write_raw(resolved_company, email, data)

    return ICPResponse(**data)
