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
    
    # Reset index to make 'Date' a proper column
    data.reset_index(inplace=True)
    
    # Clean column names: ensure they are strings and lowercase
    # This prevents the AttributeError if any non-string artifacts remain
    data.columns = [str(c).lower() for c in data.columns]
    
    # Verify 'close' column exists before proceeding
    if 'close' not in data.columns:
        print(f"Error: 'close' column not found. Available columns: {list(data.columns)}")
        return

    # Simple feature engineering
    data['ma_30'] = data['close'].rolling(window=30).mean()
    data.rename(columns={'close': 'rate'}, inplace=True)
    
    # Ensure directory exists before saving
    save_path = 'data/processed/features_engineered.csv'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    data.to_csv(save_path, index=False)
    print(f"Data updated successfully at {save_path}")

if __name__ == "__main__":
    fetch_and_save()