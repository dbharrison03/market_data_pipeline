import argparse
from market_data_pipeline.storage import init_db, get_latest_date, save_prices, load_prices
from market_data_pipeline.fetch import fetch_prices

DB_PATH = 'data/market_data.db'
DEFAULT_START = '2020-01-01'


def main():

    """Fetch and store daily prices for a specified ticker"""

    parser = argparse.ArgumentParser(description='Fetch and store daily prices for a ticker.')

    parser.add_argument('ticker')

    args = parser.parse_args()

    ticker = args.ticker.upper()

    init_db(DB_PATH)

    latest = get_latest_date(ticker,DB_PATH)

    if latest is None:
        start_date = DEFAULT_START

    else:
        start_date = latest

    print('Fetching', ticker, 'from', start_date)

    df = fetch_prices(ticker, start_date)

    if df.empty:
        print('No data found for', ticker)
        return

    rows = save_prices(df, ticker, DB_PATH)
    print('Saved', rows, 'rows for', ticker)

    recent = load_prices(ticker, DB_PATH).tail(5)
    print('Latest Prices:')
    print(recent)