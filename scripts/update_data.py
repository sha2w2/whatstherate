import yfinance as yf
import pandas as pd
import os

def fetch_and_save():
    ticker = "EURGBP=X"
    data = yf.download(ticker, period="1y", interval="1d")
    data.reset_index(inplace=True)
    data.columns = [c.lower() for c in data.columns]
    
    # Simple feature engineering
    data['ma_30'] = data['close'].rolling(window=30).mean()
    data.rename(columns={'close': 'rate'}, inplace=True)
    
    save_path = 'data/processed/features_engineered.csv'
    data.to_csv(save_path, index=False)
    print(f"Data updated successfully at {save_path}")

if __name__ == "__main__":
    fetch_and_save()