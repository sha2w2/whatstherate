import streamlit as st
import pandas as pd
from utils import load_data, load_model

st.title("AI Price Projections")
model, features = load_model()
df = load_data()

if model and df is not None:
    latest_feat = pd.DataFrame([df.iloc[-1][features]])
    pred = model.predict(latest_feat)[0]
    st.success(f"Predicted Next Session Rate: {pred:.4f}")
    
    change = pred - df.iloc[-1]['rate']
    st.write(f"Directional forecast: {'Increase' if change > 0 else 'Decrease'}")