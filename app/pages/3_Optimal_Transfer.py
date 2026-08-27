import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, convert_rate

st.set_page_config(page_title="Optimal Transfer | WhatsTheRate", layout="wide")
st.title("Optimal Transfer Strategy")

df = load_data()

if df is not None:
    # Extract day of the week and set proper chronological ordering
    df['day'] = df['date'].dt.day_name()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    st.write("Analyze historical day-of-week averages to time your exchange for the highest yield.")
    
    # Dual-Direction HCI Tabs
    tabs = st.tabs(["🇪🇺 EUR → 🇬🇧 GBP", "🇬🇧 GBP → 🇪🇺 EUR"])
    directions = ["EUR_GBP", "GBP_EUR"]
    target_currencies = ["GBP", "EUR"]

    for tab, direction, target_curr in zip(tabs, directions, target_currencies):
        with tab:
            # 1. Convert historical rates to the tab's specific direction
            df_converted = df.copy()
            df_converted['converted_rate'] = df_converted['rate'].apply(lambda x: convert_rate(x, direction))
            
            # 2. Group by day of the week and calculate the mean
            best_days = df_converted.groupby('day')['converted_rate'].mean().reindex(days_order).reset_index()
            
            # 3. Identify the optimal day (the highest rate yields the most target currency)
            optimal_day = best_days.loc[best_days['converted_rate'].idxmax()]
            
            st.success(
                f" **Statistically Optimal Day: {optimal_day['day']}**\n\n"
                f"Historically, {optimal_day['day']}s provide the highest average return ({optimal_day['converted_rate']:.4f} {target_curr}) "
                f"for this transfer direction."
            )
            
            # 4. Interactive HCI-Compliant Bar Chart
            fig = px.bar(
                best_days, 
                x='day', 
                y='converted_rate',
                labels={'day': 'Day of the Week', 'converted_rate': f'Average Rate ({target_curr})'},
                title=f"Historical Average Yield by Weekday",
                text_auto='.4f' # Display exact values on the bars
            )
            
            # Highlight the best day in a different color
            colors = ['#1E88E5'] * 5
            best_idx = days_order.index(optimal_day['day'])
            colors[best_idx] = '#4CAF50'  # Green for the best day
            fig.update_traces(marker_color=colors, textposition='outside')
            
            fig.update_layout(
                yaxis=dict(range=[best_days['converted_rate'].min() * 0.999, best_days['converted_rate'].max() * 1.001]),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Data file is missing. Please ensure the daily automation has run successfully.")
