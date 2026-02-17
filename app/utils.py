import streamlit as st
import pandas as pd
import joblib
import os

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

def get_recommendation(current, ma):
    diff = (current - ma) / ma
    if diff < -0.01: return "STRONG BUY", "Rate is significantly below 30-day average."
    if diff > 0.01: return "WAIT", "Rate is currently above 30-day average."
    return "NEUTRAL", "Rate is within expected range."