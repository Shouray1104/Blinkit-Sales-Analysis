import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BlinkIT Sales Dashboard", layout="wide")

st.title("BlinkIT Sales Analysis Dashboard")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("BlinkIT_Grocery_Data.csv")

    # Clean column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("-", "_")
    df.columns = df.columns.str.lower()

    # Clean Item Fat Content
    if "item_fat_content" in df.columns:
        df["item_fat_content"] = df["item_fat_content"].replace({
            "LF": "Low Fat",
            "low fat": "Low Fat",
            "reg": "Regular"
        })

    return df


df = load_data()

# -------------------------
# Sidebar Filter
# -------------------------
st.sidebar.header("Filters")

if "item_type" in df.columns:
    item_types = st.sidebar.multiselect(
        "Select Item Type",
        options=df["item_type"].unique(),
        default=df["item_type"].unique()
    )

    df = df[df["item_type"].isin(item_types)]

# -------------------------
# KPIs
# -------------------------
total_sales = df["sales"].sum()
average_sales = df["sales"].mean()
total_items = df["sales"].count()
average_rating = df["rating"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Average Sales", f"${average_sales:,.0f}")
col3.metric("Total Items", f"{total_items:,}")
col4.metric("Average Rating", f"{average_rating:.1f}")

st.markdown("---")

# -------------------------
# Charts
# -------------------------

# Sales by Fat Content
if "item_fat_content" in df.columns:
    sales_by_fat = df.groupby("item_fat_content")["sales"].sum().reset_index()

    fig1 = px.pie(
        sales_by_fat,
        names="item_fat_content",
        values="sales",
        title="Sales by Fat Content"
    )

    st.plotly_chart(fig1, use_container_width=True)


# Sales by Item Type
if "item_type" in df.columns:
    sales_by_type = df.groupby("item_type")["sales"].sum().reset_index()
    sales_by_type = sales_by_type.sort_values("sales", ascending=False)

    fig2 = px.bar(
        sales_by_type,
        x="item_type",
        y="sales",
        title="Total Sales by Item Type"
    )

    st.plotly_chart(fig2, use_container_width=True)


# Sales by Outlet Location Type
if "outlet_location_type" in df.columns:
    sales_by_location = df.groupby("outlet_location_type")["sales"].sum().reset_index()

    fig3 = px.bar(
        sales_by_location,
        x="outlet_location_type",
        y="sales",
        title="Total Sales by Outlet Location Type"
    )

    st.plotly_chart(fig3, use_container_width=True)


# Sales by Outlet Establishment Year
if "outlet_establishment_year" in df.columns:
    sales_by_year = df.groupby("outlet_establishment_year")["sales"].sum().reset_index()

    fig4 = px.line(
        sales_by_year,
        x="outlet_establishment_year",
        y="sales",
        title="Sales by Outlet Establishment Year",
        markers=True
    )

    st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# Data Preview
# -------------------------
st.markdown("---")
st.subheader("Data Preview")
st.dataframe(df.head())
