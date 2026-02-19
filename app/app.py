import streamlit as st
from utils import load_data, get_last_updated_time

st.set_page_config(
    page_title="WhatsTheRate | EUR-GBP Forecast",
    layout="wide"
)

def main():
    # Sidebar Automation Status
    with st.sidebar:
        st.header("Pipeline Status")
        last_update = get_last_updated_time()
        st.success(f"Last Sync: {last_update}")
        st.info("AI Model: Active")

    st.title("Welcome to WhatsTheRate- the EUR/GBP Forecast Tool.")
    st.write("Use the sidebar to explore real-time market insights, AI predictions, and transfer strategies.")

    st.markdown("""
    ---
    ### Navigation Guide:
    * **1_Dashboard**: Visual trends and current market status.
    * **2_Predictions**: AI-powered forecasts with confidence ratings.
    * **3_Optimal_Transfer**: Data-driven analysis of the best days to exchange.
    """)

    df = load_data()
    if df is not None:
        st.success("System operational. Data is up to date.")
    else:
        st.warning("Initializing data... If this is a new deployment, please wait for the first automated run.")

if __name__ == "__main__":
    main()