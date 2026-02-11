import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BlinkIT Sales Dashboard", layout="wide")

st.title("BlinkIT Sales Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("BlinkIT_Grocery_Data_Excel.csv")

    # Clean column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("-", "_")
    df.columns = df.columns.str.lower()

    return df

df = load_data()

# Standardize Item Fat Content if column exists
if "item_fat_content" in df.columns:
    df["item_fat_content"] = df["item_fat_content"].replace({
        "LF": "Low Fat",
        "low fat": "Low Fat",
        "reg": "Regular"
    })

# Sidebar Filters
st.sidebar.header("Filters")

if "outlet_location_type" in df.columns:
    location_filter = st.sidebar.multiselect(
        "Select Outlet Location Type",
        options=df["outlet_location_type"].unique(),
        default=df["outlet_location_type"].unique()
    )
    df = df[df["outlet_location_type"].isin(location_filter)]

if "item_type" in df.columns:
    item_filter = st.sidebar.multiselect(
        "Select Item Type",
        options=df["item_type"].unique(),
        default=df["item_type"].unique()
    )
    df = df[df["item_type"].isin(item_filter)]

# KPI Section
col1, col2, col3 = st.columns(3)

if "item_outlet_sales" in df.columns:
    total_sales = df["item_outlet_sales"].sum()
    avg_sales = df["item_outlet_sales"].mean()
else:
    total_sales = 0
    avg_sales = 0

col1.metric("Total Sales", f"{total_sales:,.2f}")
col2.metric("Average Sales", f"{avg_sales:,.2f}")
col3.metric("Total Items", df.shape[0])

st.markdown("---")

# Sales by Item Type
if "item_type" in df.columns and "item_outlet_sales" in df.columns:
    sales_by_item = df.groupby("item_type")["item_outlet_sales"].sum().reset_index()
    fig1 = px.bar(
        sales_by_item,
        x="item_type",
        y="item_outlet_sales",
        title="Sales by Item Type"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Sales by Outlet Location
if "outlet_location_type" in df.columns and "item_outlet_sales" in df.columns:
    sales_by_location = df.groupby("outlet_location_type")["item_outlet_sales"].sum().reset_index()
    fig2 = px.pie(
        sales_by_location,
        names="outlet_location_type",
        values="item_outlet_sales",
        title="Sales Distribution by Outlet Location"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Data Preview
st.markdown("---")
st.subheader("Data Preview")
st.dataframe(df.head())
