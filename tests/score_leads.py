# score_leads.py
"""
Score leads based on ICPRevenueUSD field presence.
Processes CSV files with company data and adds score and confidence fields.

Outputs CSV `lead_scores_YYYYMMDD.csv` with added `score` and `ai_confident` (score>=0.7).

Run: python tests/score_leads.py <input_csv>

Requires: python-dotenv
"""
import os
import csv
from datetime import datetime, date
import argparse

load_dotenv = __import__('dotenv').load_dotenv
load_dotenv()




def extract_field(row: dict, names):
    """Extract a field from a row, case-insensitive search."""
    for n in names:
        if n in row and row.get(n):
            return row.get(n)
    # case-insensitive search
    lower = {k.lower(): v for k, v in row.items()}
    for n in names:
        v = lower.get(n.lower())
        if v:
            return v
    return None


def _parse_numeric_revenue(revenue_str: str) -> float | None:
    """Parse revenue strings like 500K, 2M, 1.5B, $500,000, or 500000."""
    clean_str = revenue_str.replace(",", "").replace("$", "").strip()
    multiplier = 1
    if clean_str.upper().endswith('K'):
        multiplier = 1_000
        clean_str = clean_str[:-1]
    elif clean_str.upper().endswith('M'):
        multiplier = 1_000_000
        clean_str = clean_str[:-1]
    elif clean_str.upper().endswith('B'):
        multiplier = 1_000_000_000
        clean_str = clean_str[:-1]
    return float(clean_str) * multiplier


def _parse_employee_range(employees_str: str) -> tuple[float, float] | None:
    """Parse employee range strings like 10-50, 51-200, 1000+."""
    if not employees_str:
        return None
    employees_str = employees_str.strip().replace(' ', '')
    if employees_str.endswith('+'):
        try:
            min_val = float(employees_str[:-1])
            return min_val, min_val * 5
        except ValueError:
            return None

    if '-' in employees_str:
        parts = employees_str.split('-')
        if len(parts) == 2:
            try:
                min_val = float(parts[0])
                max_val = float(parts[1])
                return min_val, max_val
            except ValueError:
                return None
    try:
        val = float(employees_str)
        return val, val
    except ValueError:
        return None


def _expected_revenue_range(employee_range: tuple[float, float]) -> tuple[float, float]:
    """Return a broad expected revenue band for the employee range."""
    employee_min, employee_max = employee_range
    return employee_min * 40_000, employee_max * 250_000


def _format_currency(value: float) -> str:
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{int(value)}"


def score_item(row: dict):
    """
    Score a row based on ICPRevenueUSD accuracy matching (1-100 percentage).
    
    Returns: tuple (score, comment)
    - 100: Revenue is valid and falls within a plausible range given the employee band
    - 75: Revenue is valid but unusual for the employee band
    - 50: Revenue format is questionable or numeric value is zero/negative
    - Rows with blank revenue are ignored (skipped)
    """
    icp_revenue = extract_field(row, ["ICPRevenueUSD", "icprevenueusd"]) or ""
    company = extract_field(row, ["Company", "CompanyEnglish"]) or ""
    revenue_str = str(icp_revenue).strip()
    employees_str = extract_field(row, ["ICPEmployeesRange", "icpemployeesrange"]) or ""

    if not revenue_str:
        return None, None

    try:
        revenue_val = _parse_numeric_revenue(revenue_str)
    except (ValueError, AttributeError):
        comment = f"Revenue format questionable: {revenue_str}. Contains special characters or invalid format. Requires verification against {company} website and Google search results to confirm actual revenue."
        return 50, comment

    if revenue_val <= 0:
        comment = f"Revenue value is zero or negative: {revenue_str}. Data format is valid but value seems incorrect for {company}. Requires manual verification against website and Google information."
        return 50, comment

    employee_range = _parse_employee_range(str(employees_str))
    if employee_range:
        expected_min, expected_max = _expected_revenue_range(employee_range)
        if expected_min <= revenue_val <= expected_max:
            comment = f"Valid revenue data found: {revenue_str}. Value matches expected range for {company} based on {employees_str} employees."
            return 100, comment
        comment = (
            f"Revenue looks unusual for {employees_str} employees: {revenue_str}. "
            f"Expected broadly {_format_currency(expected_min)} to {_format_currency(expected_max)} for this employee band."
        )
        return 75, comment

    comment = f"Valid revenue data found: {revenue_str}. Employee range is missing or not recognized, so score is based on revenue validity alone."
    return 80, comment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="Input CSV file to score")
    parser.add_argument("--output", help="Output CSV file (default: lead_scores_YYYYMMDD.csv)")
    args = parser.parse_args()

    # Read input CSV
    if not os.path.exists(args.input_csv):
        print(f"Error: Input file '{args.input_csv}' not found")
        return

    rows = []
    try:
        with open(args.input_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    if not rows:
        print("No rows found in input CSV")
        return

    # Process and score each row, preserving all original columns.
    # Skip rows with blank ICPRevenueUSD.
    output_rows = []
    for row in rows:
        icp_revenue = extract_field(row, ["ICPRevenueUSD", "icprevenueusd"]) or ""
        
        # Skip rows with blank revenue
        if not str(icp_revenue).strip():
            continue
        
        score, score_comment = score_item(row)
        
        # Only add if score is not None (already filtered, but for safety)
        if score is not None:
            output_row = dict(row)
            output_row["score"] = score
            output_row["score_comment"] = score_comment if score_comment else ""
            output_rows.append(output_row)

    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        output_file = f"lead_scores_{date.today().strftime('%Y%m%d')}.csv"

    # Write output CSV preserving input columns and appending score columns
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            original_fieldnames = rows[0].keys() if rows else []
            fieldnames = list(original_fieldnames) + ["score", "score_comment"]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in output_rows:
                writer.writerow(r)

        print(f"Scored {len(output_rows)} rows and wrote to {output_file}")
    except Exception as e:
        print(f"Error writing output CSV: {e}")
        return



if __name__ == "__main__":
    main()
