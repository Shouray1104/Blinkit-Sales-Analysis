import streamlit as st
import pandas as pd

df = pd.read_csv("BlinkIT Grocery Data Excel.csv")

st.write("Column Names:")
st.write(df.columns)








#import streamlit as st
#import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Blinkit Sales Dashboard", layout="wide")

st.title("🛒 Blinkit Sales Analysis Dashboard")

# Load dataset (Make sure CSV is in same folder as app.py)
df = pd.read_csv("BlinkIT Grocery Data Excel.csv")

# -------------------- DATA CLEANING --------------------
df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({
    'LF': 'Low Fat',
    'low fat': 'Low Fat',
    'reg': 'Regular'
})

# -------------------- KPIs --------------------
st.subheader("📊 Key Business Metrics")

total_sales = df['Sales'].sum()
average_sales = df['Sales'].mean()
no_of_item_sold = df['Sales'].count()
average_rating = df['Rating'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("Average Sales", f"₹ {average_sales:,.0f}")
col3.metric("Items Sold", f"{no_of_item_sold:,}")
col4.metric("Average Rating", f"{average_rating:.1f}")

st.markdown("---")

# -------------------- CHART 1 --------------------
st.subheader("Sales by Fat Content")

sales_by_fat = df.groupby('Item Fat Content')['Sales'].sum()

fig1, ax1 = plt.subplots()
ax1.pie(sales_by_fat, labels=sales_by_fat.index,
        autopct='%.1f%%', startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# -------------------- CHART 2 --------------------
st.subheader("Total Sales by Item Type")

sales_by_type = df.groupby('Item Type')['Sales'].sum().sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10,5))
sales_by_type.plot(kind='bar', ax=ax2)
plt.xticks(rotation=90)
st.pyplot(fig2)

# -------------------- CHART 3 --------------------
st.subheader("Outlet Tier by Item Fat Content")

grouped = df.groupby(['Outlet Location Type', 'Item Fat Content'])['Sales'].sum().unstack()
grouped = grouped[['Regular', 'Low Fat']]

fig3, ax3 = plt.subplots()
grouped.plot(kind='bar', ax=ax3)
st.pyplot(fig3)

# -------------------- CHART 4 --------------------
st.subheader("Sales by Outlet Establishment Year")

sales_by_year = df.groupby('Outlet Establishment Year')['Sales'].sum().sort_index()

fig4, ax4 = plt.subplots()
ax4.plot(sales_by_year.index, sales_by_year.values, marker='o')
st.pyplot(fig4)

# -------------------- CHART 5 --------------------
st.subheader("Sales by Outlet Size")

sales_by_size = df.groupby('Outlet Size')['Sales'].sum()

fig5, ax5 = plt.subplots()
ax5.pie(sales_by_size, labels=sales_by_size.index,
        autopct='%1.1f%%', startangle=90)
ax5.axis("equal")
st.pyplot(fig5)

# -------------------- CHART 6 --------------------
st.subheader("Total Sales by Outlet Location Type")

sales_by_location = df.groupby('Outlet Location Type')['Sales'].sum().reset_index()
sales_by_location = sales_by_location.sort_values('Sales', ascending=False)

fig6, ax6 = plt.subplots()
sns.barplot(x='Sales', y='Outlet Location Type', data=sales_by_location, ax=ax6)
st.pyplot(fig6)
