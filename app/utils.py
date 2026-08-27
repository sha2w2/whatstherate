import streamlit as st
import pandas as pd
import joblib
import os
import datetime

@st.cache_data
def load_data():
    data_path = 'data/processed/features_engineered.csv'
    if not os.path.exists(data_path):
        return None
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_resource
def load_model():
    model_path = 'models/exchange_rate_rf_model.pkl'
    features_path = 'models/feature_list.pkl'
    if not os.path.exists(model_path) or not os.path.exists(features_path):
        return None, None
    return joblib.load(model_path), joblib.load(features_path)

def get_last_updated_time():
    data_path = 'data/processed/features_engineered.csv'
    if os.path.exists(data_path):
        mtime = os.path.getmtime(data_path)
        return datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
    return "Not Available"

def convert_rate(value, direction="EUR_GBP"):
    """
    Converts the exchange rate based on the selected direction.
    Base data is EUR -> GBP. For GBP -> EUR, returns the reciprocal.
    """
    if direction == "GBP_EUR":
        return 1.0 / value if value != 0 else 0
    return value
def get_recommendation(current, ma, direction="EUR_GBP"):
    """
    Calculates buy/wait/neutral logic based on the converted direction.
    Reduces cognitive load by explicitly stating the target currency.(HCI))
    """
    rate = convert_rate(current, direction)
    avg = convert_rate(ma, direction)

    diff = (rate - avg) / avg
    target_currency = "GBP" if direction == "EUR_GBP" else "EUR"

    if diff < -0.01: 
        return "STRONG BUY", f"Rate is significantly below 30-day average. Favorable for buying {target_currency}."
    if diff > 0.01: 
        return "WAIT", f"Rate is currently above 30-day average. Expensive to buy {target_currency}."
    return "NEUTRAL", f"Rate is within the expected 30-day average range for {target_currency}."
