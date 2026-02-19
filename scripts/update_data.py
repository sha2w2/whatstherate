import yfinance as yf
import pandas as pd
import os

def fetch_and_save():
    ticker = "EURGBP=X"
    data = yf.download(ticker, period="1y", interval="1d", progress=False)
    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    data.reset_index(inplace=True)
    data.columns = [str(c).lower() for c in data.columns]
    
    # Feature Engineering
    data['ma_30'] = data['close'].rolling(window=30).mean()
    data['returns'] = data['close'].pct_change()
    data['prev_close'] = data['close'].shift(1)
    data['volatility'] = data['close'].rolling(window=5).std()
    
    data.rename(columns={'close': 'rate'}, inplace=True)
    
    save_path = 'data/processed/features_engineered.csv'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    data.to_csv(save_path, index=False)
    print("Data updated successfully.")

if __name__ == "__main__":
    fetch_and_save()