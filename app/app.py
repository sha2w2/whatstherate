import streamlit as st
from utils import load_data, get_last_updated_time

# PAGE CONFIGURATION
st.set_page_config(
    page_title="WhatsTheRate | EUR-GBP Forecast",
    layout="wide"
)

def main():
    # Sidebar Automation Status
    with st.sidebar:
        st.header("Pipeline Status")
        last_update = get_last_updated_time()
        st.success(f"Data Refresh: {last_update}")
        st.info("AI Model: Active")

    # Brand Title Update
    st.title("Welcome to WhatsTheRate- the EUR/GBP Forecast Tool.")
    st.write("Navigate using the sidebar to explore real-time market insights and AI predictions.")

    st.markdown("""
    ### Current Capabilities:
    * **Dashboard**: Monitor live rates and technical trends.
    * **Predictions**: View AI-generated next-day price forecasts.
    * **Optimal Transfer**: Identify statistically advantageous days for currency exchange[cite: 3].
    """)

    try:
        df = load_data()
        if df is not None:
            latest_date = df['date'].max().date()
            st.info(f"Market data current as of: {latest_date}")
        else:
            st.warning("Historical data is initializing. Please check back shortly.")
    except Exception as e:
        st.error(f"System Check: {e}")

if __name__ == "__main__":
    main()