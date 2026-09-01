from pathlib import Path
import sqlite3

def init_db(db_path):
    """Create the database file and prices table if they don't exist.

    Args:
        db_path: Path to the SQLite database file.
    """
    path = Path(db_path)
    folder = path.parent
    folder.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    sql = """CREATE TABLE IF NOT EXISTS market_data (
    ticker TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    PRIMARY KEY (ticker, date))"""

    conn.execute(sql)
    conn.commit()
    conn.close()

def get_latest_date(ticker, db_path):
    """Returns the most recent date for a given ticker."""
    conn = sqlite3.connect(db_path)
    sql = """SELECT MAX(date) FROM market_data WHERE ticker = ?"""
    cursor = conn.execute(sql, (ticker,))
    row = cursor.fetchone()
    conn.close()
    return row[0]