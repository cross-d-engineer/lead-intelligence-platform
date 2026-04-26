import sqlite3
from config.settings import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row       # Allows dict-like access to rows
    return conn


def initialize_db():
    """Create tables if they don't exist."""
    with open("db/schema.sql", "r") as f:
        schema = f.read()
    with get_connection() as conn:
        conn.executescript(schema)
    print("[storage] Database initialized.")


def upsert_lead(lead: dict) -> str:
    """
    Insert a lead or ignore if place_id already exists.
    Returns 'inserted' or 'skipped'.
    """
    sql = """
        INSERT OR IGNORE INTO leads (
            place_id, business_name, industry, address, city, country,
            phone, website, google_rating, total_reviews,
            search_query, search_location
        ) VALUES (
            :place_id, :business_name, :industry, :address, :city, :country,
            :phone, :website, :google_rating, :total_reviews,
            :search_query, :search_location
        )
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, lead)
        return "inserted" if cursor.rowcount > 0 else "skipped"


def get_leads(industry: str = None, city: str = None, status: str = None) -> list:
    """Query leads with optional filters."""
    conditions = []
    params = {}

    if industry:
        conditions.append("industry = :industry")
        params["industry"] = industry
    if city:
        conditions.append("city = :city")
        params["city"] = city
    if status:
        conditions.append("status = :status")
        params["status"] = status

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    with get_connection() as conn:
        rows = conn.execute(f"SELECT * FROM leads {where}", params).fetchall()
        return [dict(row) for row in rows]
