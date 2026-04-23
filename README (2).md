# 📊 Smart Sales Analytics & Order-to-Cash (O2C) System

> A Python-powered sales analytics dashboard integrated with the complete SAP SD Order-to-Cash workflow.

---

## 👤 Project Details

| Field | Details |
|-------|---------|
| **Student** | Shreyas Das |
| **Roll No** | 23051786 |
| **Batch** | 2023–27 |
| **University** | KIIT University |
| **Subject** | SAP Data Analytics Project Work |
| **Domain** | Data Analytics |

---

## 📌 Overview

This project implements a **Smart Sales Analytics System** integrated with the **Order-to-Cash (O2C)** business process — a core workflow in SAP SD (Sales & Distribution). It combines:

- A **7-step O2C workflow** aligned with SAP SD best practices
- An **interactive analytics dashboard** built with Streamlit
- **Real-time KPIs** including DSO, Fulfillment Rate, Revenue Trends, and CLV
- **CSV-based data ingestion** for flexible analytics

---

## 🚀 Features

### 📊 Sales Overview
- Total Revenue, Orders, Avg Order Value
- Monthly Revenue Trend (line chart)
- Revenue by Region (pie chart)
- Revenue by Product Category (bar chart)
- Payment Status Breakdown

### 👥 Customer Analytics
- Customer Lifetime Value (CLV) scoring
- Top 10 customers by revenue
- Orders per customer
- CLV scatter plot (Revenue vs Frequency)

### 📦 Product Performance
- Best-selling SKUs by revenue and units
- Revenue share by category (donut chart)
- Revenue per unit analysis

### 🔄 O2C Process Monitor
- Days Sales Outstanding (DSO)
- Order-to-Ship Cycle Time
- Order Fulfillment Rate
- Invoice Rate
- O2C Funnel (order status flow)
- Pending Payments Tracker

### 📋 O2C Workflow
- Interactive 7-step workflow guide
- SAP transaction codes per step
- Live order status summary

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Core language |
| Pandas | 2.x | Data processing |
| Plotly | 5.x | Interactive charts |
| Streamlit | 1.x | Web dashboard |
| NumPy | 1.x | Numerical ops |
| GitHub | — | Version control |

---

## 📁 Project Structure

```
Smart_Sales_O2C_Project/
├── app.py                          # Main Streamlit application (5 pages)
├── sample_data.csv                 # 120-row realistic sales dataset
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── O2C_Project_Report_Shreyas_Das.pdf  # Full project report
```

---

## ⚙️ Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Shreyas13-D/smart-sales-o2c-project.git
cd smart-sales-o2c-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📊 Dataset Schema

The system uses `sample_data.csv` with these columns:

| Column | Type | Description |
|--------|------|-------------|
| order_id | String | Unique order identifier |
| customer_id | String | Customer account number |
| customer_name | String | Customer company name |
| order_date | Date | Date order was placed |
| product_sku | String | Product SKU code |
| product_name | String | Product description |
| category | String | Product category |
| quantity | Integer | Units ordered |
| unit_price | Float | Price per unit (₹) |
| discount_pct | Float | Discount percentage |
| total_amount | Float | Final order value (₹) |
| region | String | Sales region |
| order_status | String | Current O2C stage |
| payment_status | String | Payment status |
| ship_date | Date | Shipping date |
| invoice_date | Date | Invoice raised date |
| payment_date | Date | Payment received date |

---

## 🔄 O2C Workflow (SAP SD)

| Step | Process | SAP Transaction |
|------|---------|----------------|
| 1 | Customer Inquiry & Quotation | VA11 / VA21 |
| 2 | Sales Order Creation | VA01 |
| 3 | Credit Check & ATP | Automatic |
| 4 | Delivery & Goods Issue | VL01N |
| 5 | Billing & Invoice | VF01 |
| 6 | Payment Receipt | F-28 |
| 7 | Closure & Reporting | Dashboard |

---

## 📈 Key KPIs Tracked

- **Total Revenue** — SUM(Invoice Amount)
- **Days Sales Outstanding (DSO)** — (AR Balance ÷ Revenue) × Days
- **Order Fulfillment Rate** — (Closed Orders ÷ Total Orders) × 100
- **Gross Profit Margin** — ((Revenue − COGS) ÷ Revenue) × 100
- **Invoice Accuracy Rate** — (Correct Invoices ÷ Total) × 100
- **Order Cycle Time** — Delivery Date − Order Date

---

## 🔮 Future Enhancements

- SQL / PostgreSQL database backend
- AI-based demand forecasting (Prophet / scikit-learn)
- Live SAP OData API integration
- User authentication & RBAC
- Automated KPI alert system (email/SMS)

---

## 📄 License

This project is submitted as academic coursework for KIIT University.  
© 2024 Shreyas Das. All rights reserved.
