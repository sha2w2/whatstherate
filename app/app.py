import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

# PAGE CONFIGURATION 
st.set_page_config(
    page_title="EUR/GBP Exchange Rate Analysis",
    layout="wide"
)

# LOAD DATA & MODEL 
@st.cache_data
def load_data():
    """Loads and preprocesses the engineered data."""
    data_path = 'data/processed/features_engineered.csv'
    
    if not os.path.exists(data_path):
        return None
        
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_resource
def load_model():
    """Loads the trained Random Forest model and feature list."""
    model_path = 'models/exchange_rate_rf_model.pkl'
    features_path = 'models/feature_list.pkl'
    
    if not os.path.exists(model_path) or not os.path.exists(features_path):
        return None, None
        
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    return model, features

def get_recommendation(current_rate, avg_rate):
    """Generates a Buy/Sell signal based on moving average deviation."""
    threshold = 0.01 
    diff = (current_rate - avg_rate) / avg_rate
    
    if diff < -threshold:
        return "STRONG BUY", "The Euro is significantly undervalued relative to the 30-day average."
    elif diff > threshold:
        return "WAIT", "The Euro is currently overvalued relative to the 30-day average."
    else:
        return "NEUTRAL", "The rate is trading within the expected 30-day range."

# MAIN APP LOGIC 
try:
    df = load_data()
    model, feature_list = load_model()

    if df is None:
        st.error("Data file not found. Please ensure 'data/processed/features_engineered.csv' exists.")
        st.stop()

    # --- SIDEBAR CONTROLS ---
    st.sidebar.header("Dashboard Settings")
    days_to_show = st.sidebar.slider("Select timeframe (days)", 30, 365, 90)
    
    # NEW: CURRENCY CONVERTER SECTION
    st.sidebar.divider()
    st.sidebar.header("Currency Converter")
    eur_amount = st.sidebar.number_input("Enter Amount in EUR", min_value=0.0, value=100.0, step=10.0)
    
    # Get latest data point
    latest_data = df.iloc[-1]
    latest_date = latest_data['date'].date()
    current_rate = latest_data['rate']
    ma_30 = latest_data['ma_30']

    # Calculation for converter
    gbp_result = eur_amount * current_rate
    st.sidebar.success(f"{eur_amount:,.2f} EUR = {gbp_result:,.2f} GBP")
    st.sidebar.caption(f"Using current rate: {current_rate:.4f}")

    # --- TITLE SECTION ---
    st.title("EUR/GBP Exchange Rate Analysis")
    st.write(f"Analyzing historical trends to optimize currency exchange. Last updated: {latest_date}")
    st.divider()

    # --- METRICS ROW ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Current Rate (GBP)", value=f"{current_rate:.4f}")

    with col2:
        st.metric(label="30-Day Average", value=f"{ma_30:.4f}")

    with col3:
        status, message = get_recommendation(current_rate, ma_30)
        st.subheader(f"Signal: {status}")
        st.caption(message)

    st.divider()

    # --- CHART SECTION ---
    st.subheader(f"Historical Trend (Last {days_to_show} Days)")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    subset = df.tail(days_to_show)
    
    ax.plot(subset['date'], subset['rate'], label='Daily Rate', color='#1f77b4', linewidth=2)
    ax.plot(subset['date'], subset['ma_30'], label='30-Day Moving Average', color='#ff7f0e', linestyle='--', linewidth=2)
    
    ax.set_ylabel("Exchange Rate (GBP)")
    ax.set_xlabel("Date")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.xticks(rotation=45)
    
    st.pyplot(fig)

    # --- OPTIMAL TRANSFER ANALYSIS ---
    st.divider()
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Historical Best Trading Days")
        df['day_name'] = df['date'].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        avg_by_day = df.groupby('day_name')['rate'].mean().reindex(day_order)
        
        st.write("Average historical rates by day of the week:")
        st.dataframe(avg_by_day.rename("Average Rate"))
        st.caption("Lower rates represent better value for those buying Euros with GBP.")

    with right_col:
        if model is not None:
            st.subheader("AI Model Prediction")
            input_data = pd.DataFrame([latest_data[feature_list]])
            prediction = model.predict(input_data)[0]
            
            st.write(f"Projected next-day rate: **{prediction:.4f}**")
            
            change = prediction - current_rate
            direction = "increase" if change > 0 else "decrease"
            
            if abs(change) > 0.001:
                st.warning(f"Significant movement predicted: {abs(change):.4f} GBP {direction}")
            else:
                st.info("Market expected to remain stable.")
        else:
            st.warning("Model file not found. Prediction features are disabled.")

except Exception as e:
    st.error(f"An application error occurred: {e}")