import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data, load_model, convert_rate

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
    tree_preds = np.array([tree.predict(latest_feat.values) for tree in model.estimators_])
    uncertainty = np.std(tree_preds)
    
    # Convert uncertainty to a 0-100% 
    confidence_score = max(0, min(100, 100 - (uncertainty / 0.005 * 100)))
    tabs = st.tabs(["EUR → GBP", "GBP → EUR"])
directions = ["EUR_GBP", "GBP_EUR"]
target_currencies = ["GBP", "EUR"]

for tab, direction, target_curr in zip(tabs, directions, target_currencies):
    with tab:
        # Convert values according to tab direction
        latest_row = df.iloc[-1]
        curr_rate = convert_rate(latest_row['rate'], direction)
        pred_rate = convert_rate(pred, direction)
        change = pred_rate - curr_rate

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label=f"Current Spot Rate ({target_curr})", 
                value=f"{curr_rate:.4f}"
            )
            st.metric(
                label=f"Predicted Next Rate ({target_curr})", 
                value=f"{pred_rate:.4f}", 
                delta=f"{change:+.4f}"
            )

        with col2:
            st.write("### AI Model Confidence")
            st.progress(int(confidence_score) / 100)
            st.write(f"Reliability Rating: **{confidence_score:.1f}%**")

        st.divider()

        if change > 0:
            st.success(
                f"Directional Forecast: INCREASE\n\n"
                f"The model projects the rate to rise to {pred_rate:.4f} {target_curr}. "
                f"Holding base currency may yield more {target_curr} in the upcoming session."
            )
        elif change < 0:
            st.warning(
                f"Directional Forecast: DECREASE\n\n"
                f"The model projects the rate to drop to {pred_rate:.4f} {target_curr}. "
                f"Executing transfers earlier may avoid rate drops."
            )
        else:
            st.info("Directional Forecast: NEUTRAL\n\nThe rate is projected to remain steady.")

st.caption(
    "How the Confidence Score works: This score represents the level of agreement among internal decision trees. "
    "Higher percentages indicate stronger model certainty in current market volatility patterns."
)

else:
    st.error("Model or data files are missing. Please ensure the daily automation has run successfully.")
