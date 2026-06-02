import sqlite3
import csv
import os
from datetime import datetime, timedelta

DB_PATH = "icp_cache.db"
CSV_PATH = "icp_cache.csv"
CSV_FIELDS = ["company", "data", "updated_at"]

CACHE_TTL_DAYS = 30


# ----------------------------
# SQLite
# ----------------------------
def get_conn():
    # check_same_thread=False can help if used across threads (optional)
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Initialize BOTH SQLite table and CSV file header.
    Keeping name init_db() for compatibility with your current usage.
    """
    # SQLite init
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS icp_cache (
            company TEXT PRIMARY KEY,
            data TEXT,
            updated_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()

    # CSV init
    _init_csv()


# ----------------------------
# Date parsing (robust)
# ----------------------------
def _parse_iso(dt_str: str):
    """
    Robust ISO parser without datetime.fromisoformat (works on older Python).
    Handles:
      - 2026-04-21T13:49:53
      - 2026-04-21T13:49:53.123456
    Returns datetime or None.
    """
    if not dt_str:
        return None

    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue

    return None


def _is_fresh(updated_at_iso: str) -> bool:
    dt = _parse_iso(updated_at_iso)
    if dt is None:
        return False
    return (datetime.now() - dt) < timedelta(days=CACHE_TTL_DAYS)


# ----------------------------
# CSV helpers
# ----------------------------
def _init_csv():
    """Create CSV with header if missing."""
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def _csv_read_all():
    """Read all CSV rows as list of dicts."""
    if not os.path.exists(CSV_PATH):
        return []

    with open(CSV_PATH, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _csv_write_all(rows):
    """Write all rows back to CSV (overwrites file)."""
    with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _csv_get(company: str):
    """Return (data, updated_at_iso) from CSV, else None."""
    rows = _csv_read_all()
    for row in rows:
        if row.get("company") == company:
            return row.get("data"), row.get("updated_at")
    return None


def _csv_upsert(company: str, data: str, updated_at_iso: str):
    """
    Insert or replace row by company key in CSV.
    """
    _init_csv()
    rows = _csv_read_all()

    for row in rows:
        if row.get("company") == company:
            row["data"] = data
            row["updated_at"] = updated_at_iso
            _csv_write_all(rows)
            return

    # not found -> append
    rows.append({"company": company, "data": data, "updated_at": updated_at_iso})
    _csv_write_all(rows)


# ----------------------------
# Public cache API
# ----------------------------
def get_cached(company: str):
    """
    Prefer SQLite. If missing/expired, fallback to CSV.
    Returns cached data string or None.
    """
    # 1) SQLite read
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT data, updated_at FROM icp_cache WHERE company=?", (company,))
    row = cur.fetchone()
    conn.close()

    if row:
        data, updated_at = row
        if _is_fresh(updated_at):
            return data

    # 2) CSV fallback
    csv_row = _csv_get(company)
    if not csv_row:
        return None

    data, updated_at = csv_row
    if _is_fresh(updated_at):
        return data

    return None


def save_cache(company: str, data: str):
    """
    Save to SQLite AND mirror to CSV.
    """
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

    # SQLite upsert
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR REPLACE INTO icp_cache(company, data, updated_at)
        VALUES (?, ?, ?)
        """,
        (company, data, now_iso),
    )
    conn.commit()
    conn.close()

    # CSV mirror
    _csv_upsert(company, data, now_iso)