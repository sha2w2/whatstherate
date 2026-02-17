import yfinance as yf
import pandas as pd
import os

def fetch_and_save():
    ticker = "EURGBP=X"
    # Download data
    data = yf.download(ticker, period="1y", interval="1d", auto_adjust=False)
    
    if data.empty:
        print("Error: No data downloaded. Check ticker or internet connection.")
        return

    # Reset index to make 'Date' a column
    data = data.reset_index()

    # FIX: Handle MultiIndex columns (the 'tuple' error)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Ensure all column names are strings and lowercase
    data.columns = [str(c).lower() for c in data.columns]
    
    # Verify the 'close' column exists after renaming
    if 'close' not in data.columns:
        print(f"Error: 'close' column not found. Available columns: {list(data.columns)}")
        return

    # Simple feature engineering
    data['ma_30'] = data['close'].rolling(window=30).mean()
    data.rename(columns={'close': 'rate'}, inplace=True)
    
    # Ensure directory exists
    save_path = 'data/processed/features_engineered.csv'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    data.to_csv(save_path, index=False)
    print(f"Data updated successfully at {save_path}")

if __name__ == "__main__":
    fetch_and_save()