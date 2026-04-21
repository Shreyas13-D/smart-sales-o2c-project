import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="O2C Analytics Dashboard", layout="wide")

st.title("Smart Sales Analytics & O2C System")

# Upload CSV
file = st.file_uploader("Upload Sales Data", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # KPIs
    st.subheader("Key Metrics")
    total_revenue = df['total_amount'].sum()
    total_orders = df['order_id'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    col2.metric("Total Orders", total_orders)

    # Revenue Trend
    st.subheader("Revenue Trend")
    df['order_date'] = pd.to_datetime(df['order_date'])
    trend = df.groupby('order_date')['total_amount'].sum().reset_index()
    fig = px.line(trend, x='order_date', y='total_amount')
    st.plotly_chart(fig, use_container_width=True)

    # Top Customers
    st.subheader("Top Customers")
    cust = df.groupby('customer_id')['total_amount'].sum().reset_index()
    cust = cust.sort_values(by='total_amount', ascending=False).head(10)
    fig2 = px.bar(cust, x='customer_id', y='total_amount')
    st.plotly_chart(fig2, use_container_width=True)

    # Product Performance
    st.subheader("Product Performance")
    prod = df.groupby('product_sku')['total_amount'].sum().reset_index()
    fig3 = px.bar(prod, x='product_sku', y='total_amount')
    st.plotly_chart(fig3, use_container_width=True)

# O2C Flow Section
st.subheader("Order-to-Cash Workflow")
st.markdown("""
1. Customer Inquiry & Quotation  
2. Sales Order Creation  
3. Credit Check & ATP  
4. Delivery & Goods Issue  
5. Billing & Invoice Generation  
6. Payment Receipt  
7. Closure & Reporting  
""")