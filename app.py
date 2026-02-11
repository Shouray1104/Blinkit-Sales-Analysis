import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Blinkit Grocery Sales Dashboard",
    layout="wide"
)

st.title("Blinkit Grocery Sales Dashboard")
st.markdown("Interactive Sales Analysis using Streamlit and Plotly")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("BlinkIT_Grocery_Data_Excel.csv")
    return df

df = load_data()

# ---------------------------
# Data Cleaning
# ---------------------------
df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
    'LF': 'Low Fat',
    'low fat': 'Low Fat',
    'reg': 'Regular'
})

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("Filters")

outlet = st.sidebar.multiselect(
    "Select Outlet Type",
    options=df['Outlet_Type'].unique(),
    default=df['Outlet_Type'].unique()
)

item_type = st.sidebar.multiselect(
    "Select Item Type",
    options=df['Item_Type'].unique(),
    default=df['Item_Type'].unique()
)

filtered_df = df[
    (df['Outlet_Type'].isin(outlet)) &
    (df['Item_Type'].isin(item_type))
]

# ---------------------------
# KPI Section
# ---------------------------
total_sales = filtered_df['Item_Outlet_Sales'].sum()
avg_sales = filtered_df['Item_Outlet_Sales'].mean()
total_items = filtered_df.shape[0]
avg_rating = filtered_df['Rating'].mean() if 'Rating' in filtered_df.columns else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Average Sales", f"${avg_sales:,.0f}")
col3.metric("Total Items", total_items)
col4.metric("Average Rating", f"{avg_rating:.1f}")

st.markdown("---")

# ---------------------------
# Sales by Outlet Type
# ---------------------------
st.subheader("Sales by Outlet Type")

sales_by_outlet = (
    filtered_df
    .groupby("Outlet_Type")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_by_outlet,
    x="Outlet_Type",
    y="Item_Outlet_Sales",
    color="Outlet_Type",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# Sales by Item Type
# ---------------------------
st.subheader("Sales by Item Type")

sales_by_item = (
    filtered_df
    .groupby("Item_Type")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    sales_by_item,
    x="Item_Type",
    y="Item_Outlet_Sales",
    color="Item_Type"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# Sales by Fat Content
# ---------------------------
st.subheader("Sales by Fat Content")

fat_sales = (
    filtered_df
    .groupby("Item_Fat_Content")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    fat_sales,
    names="Item_Fat_Content",
    values="Item_Outlet_Sales"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# Sales by Outlet Location
# ---------------------------
st.subheader("Sales by Outlet Location Type")

location_sales = (
    filtered_df
    .groupby("Outlet_Location_Type")["Item_Outlet_Sales"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    location_sales,
    x="Outlet_Location_Type",
    y="Item_Outlet_Sales",
    color="Outlet_Location_Type"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# Raw Data Section
# ---------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
