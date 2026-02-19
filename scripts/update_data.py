import yfinance as yf
import pandas as pd
import os

def fetch_and_save():
    ticker = "EURGBP=X"
    print(f"Downloading data for {ticker}...")
    
    # Download data
    data = yf.download(ticker, period="1y", interval="1d", progress=False)
    
    # FIX: Handle MultiIndex columns (the 'tuple' error)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    data.reset_index(inplace=True)
    data.columns = [str(c).lower() for c in data.columns]
    
    if 'close' not in data.columns:
        print(f"Error: 'close' column not found.")
        return

    # Advanced Feature Engineering
    data['ma_30'] = data['close'].rolling(window=30).mean()
    data['returns'] = data['close'].pct_change()
    data['prev_close'] = data['close'].shift(1)
    data['volatility'] = data['close'].rolling(window=5).std()
    
    data.rename(columns={'close': 'rate'}, inplace=True)
    
    # Ensure directory exists
    save_path = 'data/processed/features_engineered.csv'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    data.to_csv(save_path, index=False)
    print(f"Data updated successfully with advanced features.")

if __name__ == "__main__":
    fetch_and_save()