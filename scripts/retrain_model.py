import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

def retrain():
    data_path = 'data/processed/features_engineered.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run update_data.py first.")
        return

    # Load data and drop NaN rows created by the moving average
    df = pd.read_csv(data_path).dropna()
    
    features = ['ma_30'] 
    X = df[features]
    # Target is the rate shifted by one day (predicting tomorrow)
    y = df['rate'].shift(-1).fillna(df['rate'])
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save both the model and the feature list for the app to use
    joblib.dump(model, 'models/exchange_rate_rf_model.pkl')
    joblib.dump(features, 'models/feature_list.pkl')
    print("Model retrained and saved successfully.")

if __name__ == "__main__":
    retrain()