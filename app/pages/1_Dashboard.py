import streamlit as st
import matplotlib.pyplot as plt
from utils import load_data, get_recommendation

df = load_data()
st.title("Market Dashboard")

if df is not None:
    latest = df.iloc[-1]
    col1, col2 = st.columns(2)
    col1.metric("Current Rate", f"{latest['rate']:.4f}")
    col2.metric("30-Day Moving Avg", f"{latest['ma_30']:.4f}")

    st.subheader("Historical Trend")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['date'].tail(60), df['rate'].tail(60), label='Rate')
    ax.grid(alpha=0.3)
    st.pyplot(fig)