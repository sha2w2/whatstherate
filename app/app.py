import streamlit as st
from utils import load_data

# PAGE CONFIGURATION
st.set_page_config(
    page_title="EUR/GBP Exchange Rate Analysis",
    layout="wide"
)

# MAIN ENTRY POINT LOGIC
def main():
    st.title("Welcome to the EUR/GBP AI Forecast Tool")
    st.write("Use the sidebar on the left to navigate between different analysis modules.")

    st.markdown("""
    ### Available Modules:
    1.  Dashboard : View current rates and historical trends.
    2.  Predictions : See the AI's forecast for the next trading session.
    3.  Optimal Transfer : Find the best day of the week to exchange money.
    """)

    # Check data status
    try:
        df = load_data()
        if df is not None:
            latest_date = df['date'].max().date()
            st.info(f"Last data sync completed on: {latest_date}")
        else:
            st.warning("Data file not found. Please run the update script to initialize data.")
    except Exception as e:
        st.error(f"An error occurred while checking data status: {e}")

if __name__ == "__main__":
    main()