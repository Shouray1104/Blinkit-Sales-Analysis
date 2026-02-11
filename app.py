import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="BlinkIT Sales Dashboard",
    layout="wide"
)

# -------------------------------------------------
# Custom Blinkit Theme Styling
# -------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #1C1C1C;
    }

    h1, h2, h3 {
        color: #F7C600;
    }

    div[data-testid="metric-container"] {
        background-color: #1C1C1C;
        border: 1px solid #F7C600;
        padding: 15px;
        border-radius: 10px;
    }

    div[data-testid="metric-container"] > label {
        color: #F7C600;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.markdown(
    "<h1 style='text-align: center; color: #F7C600;'>BlinkIT Sales Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("BlinkIT_Grocery_Data.csv")

    # Clean column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("-", "_")
    df.columns = df.columns.str.lower()

    # Clean Fat Content
    if "item_fat_content" in df.columns:
        df["item_fat_content"] = df["item_fat_content"].replace({
            "LF": "Low Fat",
            "low fat": "Low Fat",
            "reg": "Regular"
        })

    return df


df = load_data()

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filters")

if "item_type" in df.columns:
    selected_items = st.sidebar.multiselect(
        "Select Item Type",
        options=df["item_type"].unique(),
        default=df["item_type"].unique()
    )
    df = df[df["item_type"].isin(selected_items)]

# -------------------------------------------------
# KPIs
# -------------------------------------------------
total_sales = df["sales"].sum()
average_sales = df["sales"].mean()
total_items = df["sales"].count()
average_rating = df["rating"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Average Sales", f"${average_sales:,.0f}")
col3.metric("Total Items Sold", f"{total_items:,}")
col4.metric("Average Rating", f"{average_rating:.1f}")

st.markdown("---")

# -------------------------------------------------
# Charts
# -------------------------------------------------

# 1. Sales by Fat Content
if "item_fat_content" in df.columns:
    sales_by_fat = df.groupby("item_fat_content")["sales"].sum().reset_index()

    fig1 = px.pie(
        sales_by_fat,
        names="item_fat_content",
        values="sales",
        title="Sales by Fat Content",
        color_discrete_sequence=["#F7C600", "#FFD84D"]
    )
    fig1.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="white"
    )

    st.plotly_chart(fig1, use_container_width=True)


# 2. Sales by Item Type
if "item_type" in df.columns:
    sales_by_type = df.groupby("item_type")["sales"].sum().reset_index()
    sales_by_type = sales_by_type.sort_values("sales", ascending=False)

    fig2 = px.bar(
        sales_by_type,
        x="item_type",
        y="sales",
        title="Total Sales by Item Type",
        color_discrete_sequence=["#F7C600"]
    )
    fig2.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)


# 3. Sales by Outlet Location
if "outlet_location_type" in df.columns:
    sales_by_location = df.groupby("outlet_location_type")["sales"].sum().reset_index()

    fig3 = px.bar(
        sales_by_location,
        x="outlet_location_type",
        y="sales",
        title="Sales by Outlet Location Type",
        color_discrete_sequence=["#F7C600"]
    )
    fig3.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="white"
    )

    st.plotly_chart(fig3, use_container_width=True)


# 4. Sales by Establishment Year
if "outlet_establishment_year" in df.columns:
    sales_by_year = df.groupby("outlet_establishment_year")["sales"].sum().reset_index()

    fig4 = px.line(
        sales_by_year,
        x="outlet_establishment_year",
        y="sales",
        title="Sales by Outlet Establishment Year",
        markers=True
    )
    fig4.update_traces(line_color="#F7C600")
    fig4.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="white"
    )

    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------
# Data Preview
# -------------------------------------------------
st.markdown("---")
st.subheader("Dataset Preview")
st.dataframe(df.head())
