import pandas as pd
import streamlit as st
import plotly.express as px
df = pd.read_csv('HDDclean.csv')
st.set_page_config(page_title="HDB Resale Dashboard 2025", page_icon=":bar_chart:", layout='wide')
st.sidebar.header('Please Filter Here')
flat_types = st.sidebar.multiselect(
    "Select Flat Type",
    options=df['flat_type'].unique(),
    default=df['flat_type'].unique()[:5]
)
towns = st.sidebar.multiselect(
    "Select Town",
    options=df['town'].unique(),
    default=df['town'].unique()[:5]
)
months = st.sidebar.multiselect(
    "Select Month",
    options=df['month'].unique(),
    default=df['month'].unique()[:5]
)
st.title(":bar_chart: HDB Resale Dashboard")
st.markdown('##')

total_resale_price = df['resale_price'].sum()
unique_flat_types = df['flat_type'].nunique()

left_col, right_col = st.columns(2)
with left_col:
    st.subheader('Total Resale Price')
    st.subheader(f"US $ {total_resale_price:,.2f}")
with right_col:
    st.subheader('Number of Flat Types')
    st.subheader(f"{unique_flat_types}")
df_filtered = df.query("town == @towns and month == @months and flat_type == @flat_types")

sales_by_flat_type = df_filtered.groupby('flat_type')['resale_price'].sum().sort_values()
fig_sales_by_flat_type = px.bar(
    sales_by_flat_type,
    x=sales_by_flat_type.values,
    y=sales_by_flat_type.index,
    title="Resale Prices by Flat Type",
)

fig_sales_by_town = px.pie(
    df_filtered,
    values='resale_price',
    names='town',
    title="Resale Prices by Town"
)
sales_by_month = df_filtered.groupby('month')['resale_price'].sum().sort_values()
fig_sales_by_month = px.bar(
    sales_by_month,
    x=sales_by_month.index,
    y=sales_by_month.values,
    title="Resale Prices by Month",
    labels={"x": "Month", "y": "Total Resale Price (SGD)"}
)
a, b, c = st.columns(3)
a.plotly_chart(fig_sales_by_flat_type, use_container_width=True)
b.plotly_chart(fig_sales_by_town, use_container_width=True)
c.plotly_chart(fig_sales_by_month, use_container_width=True)

d, e = st.columns(2)
fig_line_sales_by_month = px.line(
    sales_by_month,
    x=sales_by_month.index,
    y=sales_by_month.values,
    title="Monthly Resale Price Trend",
)
d.plotly_chart(fig_line_sales_by_month, use_container_width=True)

fig_scatter_resale_price = px.scatter(
    df_filtered,
    x='resale_price',
    y='floor_area_sqm',
    title="Resale Price vs Floor Area",
)
e.plotly_chart(fig_scatter_resale_price, use_container_width=True)
