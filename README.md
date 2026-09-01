# market_data_pipeline
ETL pipeline for daily market data — fetches, caches and stores OHLCV data in SQLite
Limitation: Database stores providers current best view of the data, not the data available during time of trade, could affect backtests.