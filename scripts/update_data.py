import os

import pandas as pd
import yfinance as yf

TICKER = "EURGBP=X"
START = "2010-01-01"  # was period="1y", which overwrote the full history every night
SAVE_PATH = 'data/processed/features_engineered.csv'


def fetch_and_save():
    data = yf.download(
        TICKER, start=START, interval="1d",
        progress=False, auto_adjust=False
    )

    # If Yahoo returns nothing (rate limit, outage), stop here so the workflow
    # fails and the existing CSV and model are left untouched.
    if data.empty:
        raise SystemExit("Download returned no data - keeping existing files.")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()
    data.columns = [str(c).lower() for c in data.columns]

    # Keep the same columns as download_data.py (drops 'adj close')
    data = data[['date', 'open', 'high', 'low', 'close', 'volume']]
    data = data.dropna(subset=['close'])

    # Feature engineering (must match FEATURES in retrain_model.py)
    data['ma_30'] = data['close'].rolling(window=30).mean()
    data['returns'] = data['close'].pct_change()
    data['prev_close'] = data['close'].shift(1)
    data['volatility'] = data['close'].rolling(window=5).std()

    data = data.rename(columns={'close': 'rate'})
    data = data.dropna()  # drop warm-up rows created by the rolling windows

    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    data.to_csv(SAVE_PATH, index=False)
    print(f"Data updated successfully: {len(data)} rows, latest {data['date'].iloc[-1]}")


if __name__ == "__main__":
    fetch_and_save()
