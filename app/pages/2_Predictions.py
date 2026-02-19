import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, load_model

st.set_page_config(page_title="AI Projections | WhatsTheRate")
st.title("$$ AI Price Projections")

model, features = load_model()
df = load_data()

if model and df is not None:
    # Get the most recent data point
    latest_feat = pd.DataFrame([df.iloc[-1][features]])
    
    # 1. Base Prediction
    pred = model.predict(latest_feat)[0]
    
    # 2. Confidence Score Calculation
    # We look at the variance between all 100 trees in the forest
    tree_preds = np.array([tree.predict(latest_feat.values) for tree in model.estimators_])
    uncertainty = np.std(tree_preds)
    
    # Convert uncertainty to a 0-100% score (Heuristic based on typical EUR/GBP volatility)
    confidence_score = max(0, min(100, 100 - (uncertainty / 0.005 * 100)))

    # Display Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Predicted Next Rate", f"{pred:.4f}")
        change = pred - df.iloc[-1]['rate']
        st.write(f"Trend: {'↑ Increase' if change > 0 else '↓ Decrease'}")

    with col2:
        st.write("### AI Confidence")
        st.progress(int(confidence_score) / 100)
        st.write(f"Reliability Rating: **{confidence_score:.1f}%**")

    st.divider()
    st.info("""
    **How the Confidence Score works:** This score represents the level of agreement among the internal AI decision trees. 
    A higher percentage suggests the model sees a clear pattern in the current market volatility and indicators.
    """)
else:
    st.error("Model or data files are missing. Please ensure the daily automation has run successfully.")