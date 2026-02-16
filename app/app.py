import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

#  PAGE CONFIGURATION 
st.set_page_config(
    page_title="EUR/GBP Exchange Rate Analysis",
    layout="wide"
)

#  LOAD DATA & MODEL 
@st.cache_data
def load_data():
    """Loads and preprocesses the engineered data."""
    # Adjust path to match where you run the command from (root directory)
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
    threshold = 0.01  # 1% deviation
    diff = (current_rate - avg_rate) / avg_rate
    
    if diff < -threshold:
        return "STRONG BUY", "The Euro is significantly undervalued relative to the 30-day average."
    elif diff > threshold:
        return "WAIT", "The Euro is currently overvalued relative to the 30-day average."
    else:
        return "NEUTRAL", "The rate is trading within the expected 30-day range."

#  MAIN APP LOGIC 
try:
    # Load resources
    df = load_data()
    model, feature_list = load_model()

    if df is None:
        st.error("Data file not found. Please ensure 'data/processed/features_engineered.csv' exists.")
        st.stop()

    if model is None:
        st.warning("Model file not found. Prediction features will be disabled.")

    # Get latest data point
    latest_data = df.iloc[-1]
    latest_date = latest_data['date'].date()
    current_rate = latest_data['rate']
    ma_30 = latest_data['ma_30']

    #  TITLE SECTION 
    st.title("EUR/GBP Exchange Rate Analysis")
    st.markdown(f"**Data Date:** {latest_date}")
    st.markdown("")

    #  METRICS ROW 
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Current Rate (GBP)", value=f"{current_rate:.4f}")

    with col2:
        st.metric(label="30-Day Average", value=f"{ma_30:.4f}")

    with col3:
        status, message = get_recommendation(current_rate, ma_30)
        st.subheader(f"Signal: {status}")
        st.caption(message)

    st.markdown("")

    #  CHART SECTION 
    st.subheader("Historical Trend (90 Days)")
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Filter for the last 90 days
    subset = df.tail(90)
    
    ax.plot(subset['date'], subset['rate'], label='Daily Rate', color='#1f77b4', linewidth=2)
    ax.plot(subset['date'], subset['ma_30'], label='30-Day Moving Average', color='#ff7f0e', linestyle='--', linewidth=2)
    
    ax.set_ylabel("Exchange Rate (GBP)")
    ax.set_xlabel("Date")
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Rotate date labels for readability
    plt.xticks(rotation=45)
    
    # Render chart
    st.pyplot(fig)

    #   MODEL PREDICTION SECTION
    if model is not None:
        st.markdown("_")
        st.subheader("AI Model Prediction")
        
        # Prepare input for prediction (reshape to 2D array)
        input_data = pd.DataFrame([latest_data[feature_list]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        st.write(f"The Random Forest model predicts the rate will move towards **{prediction:.4f}** in the next trading session.")
        
        # Calculate potential movement
        change = prediction - current_rate
        direction = "increase" if change > 0 else "decrease"
        st.info(f"Predicted movement: {abs(change):.4f} GBP {direction}")

except Exception as e:
    st.error(f"An application error occurred: {e}")