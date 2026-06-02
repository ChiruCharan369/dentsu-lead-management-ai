import csv
from pathlib import Path

from app.db.cache_db import init_db
from app.services.icp_service import get_icp_data

COMPANIES = [
"EVM India Pvt Ltd",
"JDA Infra Ltd.",
"Azentio",
"Repligen life science",

]

CSV_FILE = Path("test_company.csv")
FIELDNAMES = [
    "company",
    "email",
    "ICPIndustry",
    "ICPEmployeesRange",
    "ICPRevenueUSD",
    "ICPFundingType",
    "ICPFundingStage",
    "ICPFUndingAmount",
    "ICPParentCompany",
    "ICPLinkedInURL",
    "ICPMarketingSignal",
    "ICPFitStatus",
    "ICPFitmentTest",
]


def write_csv(rows):
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CSV_FILE.open(mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main():
    init_db()
    rows = []

    for company in COMPANIES:
        print(f"Checking ICP for: {company}")
        try:
            response = get_icp_data(company=company, email="")
            row = response.dict()
            row["company"] = company
            row["email"] = ""
            rows.append(row)
            print(f"  OK: {company}")
        except Exception as exc:
            print(f"  ERROR: {company}: {exc}")
            row = {"company": company, "email": "", **{k: "" for k in FIELDNAMES if k not in ["company", "email"]}}
            rows.append(row)

    write_csv(rows)
    print(f"Saved {len(rows)} companies to {CSV_FILE}")


if __name__ == "__main__":
    main()