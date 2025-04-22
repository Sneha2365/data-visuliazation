import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
orders = pd.read_csv("Sample Superstore 2022 - Orders.csv")
returns = pd.read_csv("Sample Superstore 2022 - Returns.csv")

# Merge returns to orders
orders['Returned'] = orders['Order ID'].isin(returns['Order ID'])

# Preprocessing
orders['Order Date'] = pd.to_datetime(orders['Order Date'])
orders['Month'] = orders['Order Date'].dt.to_period('M').astype(str)

# Dashboard Title
st.set_page_config(layout="wide")
st.title("📊 Superstore Sales Dashboard")

# KPIs
total_sales = orders['Sales'].sum()
total_profit = orders['Profit'].sum()
total_orders = orders['Order ID'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", total_orders)

st.markdown("---")

# Sales and Profit by Region
region_df = orders.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
fig1 = px.bar(region_df, x='Region', y=['Sales', 'Profit'],
              barmode='group', title="Sales and Profit by Region")
st.plotly_chart(fig1, use_container_width=True)

# Sales and Profit by Category/Sub-Category
cat_df = orders.groupby(['Category', 'Sub-Category'])[['Sales', 'Profit']].sum().reset_index()
fig2 = px.sunburst(cat_df, path=['Category', 'Sub-Category'], values='Sales',
                   color='Profit', title="Sales Distribution by Category/Sub-Category")
st.plotly_chart(fig2, use_container_width=True)

# Time Series Trend
monthly = orders.groupby('Month')[['Sales', 'Profit']].sum().reset_index().sort_values('Month')
fig3 = px.line(monthly, x='Month', y=['Sales', 'Profit'], title="Sales & Profit Over Time")
st.plotly_chart(fig3, use_container_width=True)

# Returns Analysis
returns_df = orders.groupby('Returned')[['Sales']].count().reset_index()
returns_df['Returned'] = returns_df['Returned'].map({True: 'Returned', False: 'Not Returned'})
fig4 = px.pie(returns_df, names='Returned', values='Sales', title="Return Rate")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Segment Performance
segment_df = orders.groupby('Segment')[['Sales', 'Profit']].sum().reset_index()
fig5 = px.bar(segment_df, x='Segment', y='Profit', color='Sales', title="Segment Performance")
st.plotly_chart(fig5, use_container_width=True)

# Footer
st.caption("📍 Built with Streamlit | Superstore Data Storytelling")

