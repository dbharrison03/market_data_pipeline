# market_data_pipeline

A command-line ETL pipeline that downloads daily OHLCV price data from Yahoo Finance and stores it in SQLite, fetching only new days on each run.

## Quick start

```bash
git clone https://github.com/dbharrison03/market_data_pipeline.git
cd market_data_pipeline
python -m venv .venv
.venv\Scripts\Activate.ps1        # macOS/Linux: source .venv/bin/activate
pip install -e .

market-data-pipeline TSLA
```

```
Fetching TSLA from 2020-01-01      ← first run: full history
Saved 1707 rows for TSLA

Fetching TSLA from 2026-10-16      ← later runs: only new days
Saved 1 rows for TSLA
```

Each run also prints the five most recent stored days. Data is saved to `data/market_data.db`, in one table, `market_data`, keyed on `(ticker, date)`.

## How it works

| Module | Responsibility |
|---|---|
| `cli.py` | Entry point: finds the latest stored date, fetches from there, saves, prints |
| `fetch.py` | Downloads from Yahoo Finance and cleans into the storage schema |
| `storage.py` | All SQLite access: create, save, load, latest date |

**Design choices**
- **Incremental caching:** only days since the last stored date are downloaded.
- **Upsert on `(ticker, date)`:** re-runs never duplicate rows, and the most recent day is refreshed with final values.
- **Atomic batches:** each save writes all rows or none, so a failed run can't leave gaps.
- **Separation of concerns:** storage never knows where data came from, so swapping the data source means changing one file.

## Known limitations

- **Not point-in-time:** Yahoo's prices are adjusted for splits and dividends, so stored history embeds hindsight, and backtests may carry lookahead bias.
- **Splits between runs:** older rows stay on the old price scale. To fix, delete the ticker's rows and re-run.
- **Unofficial source:** `yfinance` relies on Yahoo's public endpoints, which can change without notice.
- Daily data only. Run it from the project root, since the database path is relative. No automated tests yet.