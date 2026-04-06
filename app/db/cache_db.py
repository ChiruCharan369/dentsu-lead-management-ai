import sqlite3
from datetime import datetime, timedelta

DB_PATH = "icp_cache.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():

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


def get_cached(company: str):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT data, updated_at FROM icp_cache WHERE company=?",
        (company,),
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    data, updated_at = row

    updated_at = datetime.fromisoformat(updated_at)

    # 30 days window
    if datetime.now() - updated_at < timedelta(days=30):
        return data

    return None


def save_cache(company: str, data: str):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO icp_cache(company, data, updated_at)
        VALUES (?, ?, ?)
        """,
        (
            company,
            data,
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()