import yfinance as yf

def fetch_prices(ticker, start):
    """Download one tickers daily prices from start to current date.

    Args:
        ticker: ticker ID to download e.g. 'AAPL'
        start: date to start downloading data from, 'YYYY-MM-DD' (inclusive)

    Returns:
        Dataframe with columns: date, open, high, low, close, volume, in the shape
        save_prices expects. Empty if nothing found
    """

    df = yf.Ticker(ticker).history(start=start)

    if df.empty:
        return df

    df = df.reset_index()

    df.columns = df.columns.str.lower()

    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    return df


