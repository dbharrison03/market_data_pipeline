from pathlib import Path
import sqlite3
import pandas as pd

def init_db(db_path):
    """Create the database file and market data table if they don't exist.

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

def save_prices(df, ticker , db_path):
    """Upsert one ticker's daily prices into the market_data table.

        Rows whose (ticker, date) already exist are overwritten with the new
        values. The whole batch is saved atomically: all rows or none.

        Precondition: df holds prices for a single ticker, has no ticker
        column, and has columns date (str, 'YYYY-MM-DD'), open, high, low,
        close, volume.

        Args:
            df: DataFrame of daily prices for one ticker.
            ticker: Symbol to store the rows under, e.g. 'AAPL'.
            db_path: Path to the SQLite database file.

        Returns:
            Number of rows written.
        """

    ordered = df[['date', 'open','high','low','close','volume' ]]

    rows = [(ticker, *row) for row in ordered.itertuples(index=False)]

    sql = """
            INSERT INTO market_data (ticker, date, open, high, low, close, volume)
            VALUES ( ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT ( ticker, date) DO UPDATE SET
            open = excluded.open,
            high = excluded.high,
            low = excluded.low,
            close = excluded.close,
            volume = excluded.volume
            """

    conn = sqlite3.connect(db_path)
    try:
        with conn:
            conn.executemany(sql, rows)

    finally:
        conn.close()

    return len(rows)



