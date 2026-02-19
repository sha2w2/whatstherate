import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

def retrain():
    data_path = 'data/processed/features_engineered.csv'
    if not os.path.exists(data_path): return

    df = pd.read_csv(data_path).dropna()
    
    # Must match the features created in update_data.py
    features = ['ma_30', 'returns', 'prev_close', 'volatility'] 
    X = df[features]
    y = df['rate'].shift(-1).fillna(df['rate'])
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/exchange_rate_rf_model.pkl')
    joblib.dump(features, 'models/feature_list.pkl')
    print("Model retrained successfully.")

if __name__ == "__main__":
    retrain()