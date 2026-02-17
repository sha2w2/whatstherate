import streamlit as st
from utils import load_data

st.title("Optimal Transfer Strategy")
df = load_data()

if df is not None:
    df['day'] = df['date'].dt.day_name()
    best_days = df.groupby('day')['rate'].mean().sort_values()
    
    st.write("Average historical exchange rate by day of the week:")
    st.table(best_days)
    st.info(f"Statistically, {best_days.index[0]} has been the cheapest day to buy Euros.")