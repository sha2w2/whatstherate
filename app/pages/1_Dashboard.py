import streamlit as st
import plotly.graph_objects as go
from utils import load_data, get_recommendation

df = load_data()
st.title("Market Dashboard")

if df is not None:
    latest = df.iloc[-1]
# 1 Dual-Direction Tabs
    tabs = st.tabs(["🇪🇺 EUR → 🇬🇧 GBP", "🇬🇧 GBP → 🇪🇺 EUR"])
    directions = ["EUR_GBP", "GBP_EUR"]
    labels = ["GBP per 1 EUR", "EUR per 1 GBP"]
    
    for tab, direction, label in zip(tabs, directions, labels):
        with tab:
            # Calculate metrics for the current direction
            rate = convert_rate(latest['rate'], direction)
            ma_30 = convert_rate(latest['ma_30'], direction
# 2 Clearer Info Hierarchy using Columns
            col1, col2, col3 = st.columns(3)
            col1.metric(f"Current Rate", f"{rate:.4f} {label.split()[0]}")
            col2.metric("30-Day Moving Avg", f"{ma_30:.4f}", help="Average rate over the last 30 trading days.")
            
            # Fetch the dynamic recommendation
            rec_status, rec_reason = get_recommendation(latest['rate'], latest['ma_30'], direction)
            col3.metric("Algorithmic Signal", rec_status, help=rec_reason)
            
            st.divider()
            st.subheader(f"Historical Trend (Last 60 Days)")
            
            # Prep data for plotting based on the selected tab
            df_plot = df.tail(60).copy()
            if direction == "GBP_EUR":
                df_plot['rate'] = 1.0 / df_plot['rate']
                df_plot['ma_30'] = 1.0 / df_plot['ma_30']
# 3. Interactive Plotly Chart, no more static Matplotlib
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_plot['date'], y=df_plot['rate'], mode='lines', name='Exchange Rate', line=dict(color='#1E88E5')))
            fig.add_trace(go.Scatter(x=df_plot['date'], y=df_plot['ma_30'], mode='lines', name='30-Day MA', line=dict(color='#FFC107', dash='dash')))
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=label,
                hovermode="x unified",
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
