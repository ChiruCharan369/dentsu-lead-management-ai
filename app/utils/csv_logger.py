import csv
import os
import json
from datetime import datetime

# target folder: app/csv_files
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CSV_DIR = os.path.join(BASE_DIR, "csv_files")


# ensure folder exists
os.makedirs(CSV_DIR, exist_ok=True)

STRUCTURED_FILE = os.path.join(CSV_DIR, "icp_structured.csv")
RAW_FILE = os.path.join(CSV_DIR, "icp_raw.csv")


def write_structured(data: dict):

    print("Writing structured CSV →", STRUCTURED_FILE)

    file_exists = os.path.isfile(STRUCTURED_FILE)

    with open(STRUCTURED_FILE, mode="a", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def write_raw(company: str, email: str, data: dict):

    print("Writing raw CSV →", RAW_FILE)

    file_exists = os.path.isfile(RAW_FILE)

    with open(RAW_FILE, mode="a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["company", "email", "json", "timestamp"])

        writer.writerow([
            company,
            email,
            json.dumps(data),
            datetime.now().isoformat()
        ])