import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

def retrain():
    df = pd.read_csv('data/processed/features_engineered.csv').dropna()
    features = ['ma_30'] # Add more features from your notebook here
    X = df[features]
    y = df['rate'].shift(-1).fillna(df['rate'])
    
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X, y)
    
    joblib.dump(model, 'models/exchange_rate_rf_model.pkl')
    joblib.dump(features, 'models/feature_list.pkl')
    print("Model retrained and saved.")

if __name__ == "__main__":
    retrain()