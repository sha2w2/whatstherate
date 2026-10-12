import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

DATA_PATH = 'data/processed/features_engineered.csv'

# 'rate' (today's close) is now a feature. Before, the model only saw yesterday's
# close (prev_close / lag_1) and indirect hints, so it was effectively forecasting
# two days ahead, which is why the prediction line trails the actual line.
FEATURES = ['rate', 'ma_30', 'returns', 'prev_close', 'volatility']


def retrain():
    if not os.path.exists(DATA_PATH):
        raise SystemExit(f"{DATA_PATH} not found - run update_data.py first.")

    df = pd.read_csv(DATA_PATH).dropna().reset_index(drop=True)

    # Target = next day's rate. The final row has no "next day" yet, so it is dropped
    # (before, it was filled with its own rate, which taught the model a fake example).
    df['target'] = df['rate'].shift(-1)
    df = df.dropna(subset=['target'])

    X, y = df[FEATURES], df['target']

    # Time-ordered holdout check so the Actions log shows how good the model is
    split = int(len(df) * 0.8)
    check = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    check.fit(X.iloc[:split], y.iloc[:split])
    preds = check.predict(X.iloc[split:])
    actual = y.iloc[split:].to_numpy()
    current = X['rate'].iloc[split:].to_numpy()

    mae = mean_absolute_error(actual, preds)
    mape = np.mean(np.abs(actual - preds) / actual) * 100
    directional = np.mean(np.sign(preds - current) == np.sign(actual - current)) * 100
    print(f"Holdout MAE: {mae:.5f} | MAPE: {mape:.3f}% | Directional accuracy: {directional:.1f}%")

    # Final model trained on all available data
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/exchange_rate_rf_model.pkl')
    joblib.dump(FEATURES, 'models/feature_list.pkl')
    print("Model retrained successfully.")


if __name__ == "__main__":
    retrain()
