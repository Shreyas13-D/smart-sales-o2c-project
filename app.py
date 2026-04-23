import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Sales Analytics & O2C System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 1.9rem; font-weight: 700; color: #1B2A4A;
        border-bottom: 3px solid #2563EB; padding-bottom: 0.4rem; margin-bottom: 1rem;
    }
    .sub-header { font-size: 1rem; font-weight: 600; color: #1B2A4A; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Smart Sales O2C")
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊 Sales Overview",
        "👥 Customer Analytics",
        "📦 Product Performance",
        "🔄 O2C Process Monitor",
        "📋 O2C Workflow",
    ])
    st.markdown("---")
    st.markdown("**Upload Your Data**")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    st.markdown("---")
    st.caption("Shreyas Das | Roll: 23051786")
    st.caption("Batch: 2023–27 | KIIT University")
    st.caption("Subject: SAP Data Analytics")

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file=None):
    df = pd.read_csv(file) if file else pd.read_csv("sample_data.csv")
    for col in ["order_date", "ship_date", "invoice_date", "payment_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

df = load_data(uploaded)

# ── Filters ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**Filters**")
    regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
    sel_region = st.selectbox("Region", regions)
    date_range = st.date_input("Date Range",
        value=[df["order_date"].min(), df["order_date"].max()])

fdf = df.copy()
if sel_region != "All":
    fdf = fdf[fdf["region"] == sel_region]
if len(date_range) == 2:
    fdf = fdf[(fdf["order_date"] >= pd.Timestamp(date_range[0])) &
              (fdf["order_date"] <= pd.Timestamp(date_range[1]))]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — SALES OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Sales Overview":
    st.markdown('<div class="main-header">📊 Sales Overview Dashboard</div>', unsafe_allow_html=True)

    total_rev  = fdf["total_amount"].sum()
    total_ord  = fdf["order_id"].nunique()
    avg_ord    = fdf["total_amount"].mean()
    cleared    = fdf[fdf["payment_status"] == "Cleared"]["total_amount"].sum()
    pending    = fdf[fdf["payment_status"] != "Cleared"]["total_amount"].sum()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("💰 Total Revenue",   f"₹{total_rev:,.0f}")
    c2.metric("🛒 Total Orders",    f"{total_ord}")
    c3.metric("📈 Avg Order Value", f"₹{avg_ord:,.0f}")
    c4.metric("✅ Cleared Revenue", f"₹{cleared:,.0f}")
    c5.metric("⏳ Pending Revenue", f"₹{pending:,.0f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sub-header">📅 Monthly Revenue Trend</div>', unsafe_allow_html=True)
        t = fdf.copy()
        t["month"] = t["order_date"].dt.to_period("M").astype(str)
        monthly = t.groupby("month")["total_amount"].sum().reset_index()
        fig = px.line(monthly, x="month", y="total_amount", markers=True,
                      color_discrete_sequence=["#2563EB"])
        fig.update_traces(line_width=2.5, marker_size=7)
        fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                          xaxis_title="Month", yaxis_title="Revenue (₹)", yaxis_tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sub-header">🗺️ Revenue by Region</div>', unsafe_allow_html=True)
        reg = fdf.groupby("region")["total_amount"].sum().reset_index()
        fig2 = px.pie(reg, names="region", values="total_amount",
                      color_discrete_sequence=px.colors.sequential.Blues_r)
        fig2.update_traces(textinfo="label+percent", pull=[0.04]*len(reg))
        fig2.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sub-header">📂 Revenue by Category</div>', unsafe_allow_html=True)
        cat = fdf.groupby("category")["total_amount"].sum().reset_index().sort_values("total_amount")
        fig3 = px.bar(cat, x="total_amount", y="category", orientation="h",
                      color="total_amount", color_continuous_scale="Blues")
        fig3.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                           xaxis_tickformat=",.0f", coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="sub-header">💳 Payment Status</div>', unsafe_allow_html=True)
        pay = fdf.groupby("payment_status")["total_amount"].sum().reset_index()
        cmap = {"Cleared":"#16A34A","Pending":"#F59E0B","Partially Paid":"#2563EB"}
        fig4 = px.pie(pay, names="payment_status", values="total_amount",
                      color="payment_status", color_discrete_map=cmap)
        fig4.update_traces(textinfo="label+percent")
        fig4.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="sub-header">📋 Data Table</div>', unsafe_allow_html=True)
    st.dataframe(fdf.sort_values("order_date", ascending=False).reset_index(drop=True),
                 use_container_width=True, height=280)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CUSTOMER ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👥 Customer Analytics":
    st.markdown('<div class="main-header">👥 Customer Analytics</div>', unsafe_allow_html=True)

    cdf = fdf.groupby(["customer_id","customer_name"]).agg(
        total_revenue=("total_amount","sum"),
        total_orders=("order_id","nunique"),
        avg_order_value=("total_amount","mean"),
    ).reset_index()
    cdf["clv_score"] = (cdf["total_revenue"] * cdf["total_orders"]) / 1000

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("👥 Total Customers",  f"{cdf['customer_id'].nunique()}")
    c2.metric("🏆 Top Revenue",      f"₹{cdf['total_revenue'].max():,.0f}")
    c3.metric("♻️ Repeat Customers", f"{(cdf['total_orders']>1).sum()}")
    c4.metric("⭐ Avg CLV Score",    f"{cdf['clv_score'].mean():.1f}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sub-header">🏆 Top Customers by Revenue</div>', unsafe_allow_html=True)
        top10 = cdf.sort_values("total_revenue", ascending=False).head(10)
        fig = px.bar(top10, x="total_revenue", y="customer_name", orientation="h",
                     color="total_revenue", color_continuous_scale="Blues", text="total_revenue")
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                          xaxis_tickformat=",.0f", coloraxis_showscale=False, yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sub-header">📦 Orders per Customer</div>', unsafe_allow_html=True)
        fig2 = px.bar(cdf.sort_values("total_orders", ascending=False),
                      x="customer_name", y="total_orders",
                      color="total_orders", color_continuous_scale="Blues")
        fig2.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                           coloraxis_showscale=False, xaxis_title="", yaxis_title="Orders")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sub-header">⭐ CLV: Revenue vs Order Frequency</div>', unsafe_allow_html=True)
    fig3 = px.scatter(cdf, x="total_orders", y="total_revenue", size="clv_score",
                      color="customer_name", hover_data=["avg_order_value"],
                      size_max=50, title="Bubble size = CLV Score")
    fig3.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC", yaxis_tickformat=",.0f")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="sub-header">📋 Customer Summary</div>', unsafe_allow_html=True)
    d = cdf.copy()
    d["total_revenue"]   = d["total_revenue"].apply(lambda x: f"₹{x:,.0f}")
    d["avg_order_value"] = d["avg_order_value"].apply(lambda x: f"₹{x:,.0f}")
    d["clv_score"]       = d["clv_score"].apply(lambda x: f"{x:.1f}")
    st.dataframe(d.rename(columns={"customer_id":"ID","customer_name":"Name",
        "total_revenue":"Revenue","total_orders":"Orders",
        "avg_order_value":"Avg Value","clv_score":"CLV"}), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PRODUCT PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📦 Product Performance":
    st.markdown('<div class="main-header">📦 Product Performance</div>', unsafe_allow_html=True)

    pdf = fdf.groupby(["product_sku","product_name","category"]).agg(
        total_revenue=("total_amount","sum"),
        units_sold=("quantity","sum"),
        orders=("order_id","nunique"),
        avg_unit_price=("unit_price","mean"),
    ).reset_index()
    pdf["revenue_per_unit"] = pdf["total_revenue"] / pdf["units_sold"]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📦 Products",       f"{pdf['product_sku'].nunique()}")
    c2.metric("📦 Units Sold",     f"{pdf['units_sold'].sum():,}")
    c3.metric("🏆 Top SKU Rev",    f"₹{pdf['total_revenue'].max():,.0f}")
    c4.metric("📊 Categories",     f"{pdf['category'].nunique()}")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sub-header">🏆 Revenue by Product</div>', unsafe_allow_html=True)
        fig = px.bar(pdf.sort_values("total_revenue",ascending=False),
                     x="product_name", y="total_revenue", color="category",
                     color_discrete_sequence=px.colors.sequential.Blues_r, text="total_revenue")
        fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                          xaxis_title="", yaxis_tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sub-header">📦 Units Sold by Product</div>', unsafe_allow_html=True)
        fig2 = px.bar(pdf.sort_values("units_sold",ascending=True),
                      x="units_sold", y="product_name", orientation="h",
                      color="units_sold", color_continuous_scale="Blues")
        fig2.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                           coloraxis_showscale=False, xaxis_title="Units", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sub-header">🗂️ Revenue Share by Category</div>', unsafe_allow_html=True)
        cat_rev = pdf.groupby("category")["total_revenue"].sum().reset_index()
        fig3 = px.pie(cat_rev, names="category", values="total_revenue",
                      color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.4)
        fig3.update_traces(textinfo="label+percent")
        fig3.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="sub-header">💰 Revenue per Unit</div>', unsafe_allow_html=True)
        fig4 = px.bar(pdf.sort_values("revenue_per_unit",ascending=False),
                      x="product_name", y="revenue_per_unit",
                      color="revenue_per_unit", color_continuous_scale="Blues", text="revenue_per_unit")
        fig4.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
        fig4.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                           coloraxis_showscale=False, xaxis_title="", yaxis_tickformat=",.0f")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="sub-header">📋 Product Summary</div>', unsafe_allow_html=True)
    d = pdf.copy()
    d["total_revenue"]    = d["total_revenue"].apply(lambda x: f"₹{x:,.0f}")
    d["avg_unit_price"]   = d["avg_unit_price"].apply(lambda x: f"₹{x:,.0f}")
    d["revenue_per_unit"] = d["revenue_per_unit"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(d.rename(columns={"product_sku":"SKU","product_name":"Product",
        "category":"Category","total_revenue":"Revenue","units_sold":"Units Sold",
        "orders":"Orders","avg_unit_price":"Avg Price","revenue_per_unit":"Rev/Unit"}),
        use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — O2C PROCESS MONITOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔄 O2C Process Monitor":
    st.markdown('<div class="main-header">🔄 O2C Process Monitor</div>', unsafe_allow_html=True)

    cleared_df = fdf[fdf["payment_status"] == "Cleared"].copy()
    cleared_df["days_to_pay"] = (cleared_df["payment_date"] - cleared_df["order_date"]).dt.days
    dso = cleared_df["days_to_pay"].mean() if len(cleared_df) else 0

    shipped_df = fdf[fdf["ship_date"].notna()].copy()
    shipped_df["cycle_days"] = (shipped_df["ship_date"] - shipped_df["order_date"]).dt.days
    avg_cycle = shipped_df["cycle_days"].mean() if len(shipped_df) else 0

    total_ord    = fdf["order_id"].nunique()
    closed_ord   = fdf[fdf["order_status"] == "Closed"]["order_id"].nunique()
    fulfillment  = (closed_ord / total_ord * 100) if total_ord else 0
    invoiced_pct = (fdf[fdf["invoice_date"].notna()]["order_id"].nunique() / total_ord * 100) if total_ord else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📅 Avg DSO",             f"{dso:.1f} days")
    c2.metric("🚚 Avg Cycle Time",      f"{avg_cycle:.1f} days")
    c3.metric("✅ Fulfillment Rate",    f"{fulfillment:.1f}%")
    c4.metric("🧾 Invoice Rate",        f"{invoiced_pct:.1f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sub-header">📊 O2C Funnel — Order Status</div>', unsafe_allow_html=True)
        status_order = ["Order Placed","Processing","Shipped","Delivered","Invoiced","Closed"]
        sc = fdf["order_status"].value_counts().reindex(status_order, fill_value=0).reset_index()
        sc.columns = ["status","count"]
        fig = px.funnel(sc, x="count", y="status",
                        color_discrete_sequence=["#1B2A4A"])
        fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sub-header">💳 Payment Status by Region</div>', unsafe_allow_html=True)
        pay_reg = fdf.groupby(["region","payment_status"])["total_amount"].sum().reset_index()
        cmap = {"Cleared":"#16A34A","Pending":"#F59E0B","Partially Paid":"#2563EB"}
        fig2 = px.bar(pay_reg, x="region", y="total_amount", color="payment_status",
                      barmode="group", color_discrete_map=cmap)
        fig2.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                           xaxis_title="", yaxis_tickformat=",.0f")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sub-header">⏱️ Days-to-Payment Distribution</div>', unsafe_allow_html=True)
        if len(cleared_df) > 0:
            fig3 = px.histogram(cleared_df, x="days_to_pay", nbins=20,
                                color_discrete_sequence=["#2563EB"])
            fig3.add_vline(x=dso, line_dash="dash", line_color="#1B2A4A",
                           annotation_text=f"Avg: {dso:.0f}d")
            fig3.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                               xaxis_title="Days to Payment", yaxis_title="Orders")
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="sub-header">📅 Monthly Order Volume</div>', unsafe_allow_html=True)
        fdf2 = fdf.copy()
        fdf2["month"] = fdf2["order_date"].dt.to_period("M").astype(str)
        mv = fdf2.groupby("month")["order_id"].nunique().reset_index()
        mv.columns = ["month","orders"]
        fig4 = px.bar(mv, x="month", y="orders", color_discrete_sequence=["#2563EB"])
        fig4.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC",
                           xaxis_title="", yaxis_title="Orders")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="sub-header">📋 Pending Payments Tracker</div>', unsafe_allow_html=True)
    pend = fdf[fdf["payment_status"] != "Cleared"][
        ["order_id","customer_name","order_date","total_amount","order_status","payment_status","region"]
    ].sort_values("total_amount", ascending=False).reset_index(drop=True)
    pend["total_amount"] = pend["total_amount"].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(pend, use_container_width=True, height=250)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — O2C WORKFLOW
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📋 O2C Workflow":
    st.markdown('<div class="main-header">📋 Order-to-Cash Workflow</div>', unsafe_allow_html=True)
    st.markdown("Complete 7-step O2C process aligned with SAP SD best practices.")
    st.markdown("---")

    steps = [
        ("1","Customer Inquiry & Quotation","VA11 / VA21","📝",
         "Customer contacts the business with a requirement. A formal quotation is prepared with product details, pricing, and validity. This is the entry point of the O2C cycle."),
        ("2","Sales Order Creation","VA01","📄",
         "Once the customer approves the quotation, a Sales Order is raised capturing customer ID, product SKUs, quantity, agreed price, delivery date, and payment terms."),
        ("3","Credit Check & ATP Verification","Automatic","🔍",
         "The system checks the customer credit limit and performs an Available-to-Promise (ATP) check on inventory. Orders are confirmed or placed on hold accordingly."),
        ("4","Delivery & Goods Issue","VL01N","🚚",
         "Warehouse executes picking, packing, and shipping. A Delivery document is created and Goods Issue is posted, reducing stock and triggering accounting entries."),
        ("5","Billing & Invoice Generation","VF01","🧾",
         "A commercial invoice is generated with itemised charges, applicable GST/taxes, discounts, and payment due date."),
        ("6","Payment Receipt","F-28","💳",
         "Customer makes payment. Finance team records the incoming payment against the open invoice item and clears the receivable account."),
        ("7","Transaction Closure & Reporting","Dashboard","📊",
         "All documents are archived and marked complete. The analytics dashboard updates with final revenue, DSO metrics, and customer KPIs."),
    ]

    for num, title, txn, icon, desc in steps:
        with st.expander(f"{icon}  Step {num}: {title}  —  SAP Txn: **{txn}**", expanded=True):
            col1, col2 = st.columns([1, 5])
            with col1:
                st.markdown(f"""
                <div style='background:#1B2A4A;color:white;border-radius:50%;
                width:56px;height:56px;display:flex;align-items:center;
                justify-content:center;font-size:1.5rem;margin:auto;'>{icon}</div>
                <p style='text-align:center;margin-top:6px;'>
                <span style='background:#2563EB;color:white;padding:2px 8px;
                border-radius:10px;font-size:0.75rem;font-weight:600;'>{txn}</span></p>
                """, unsafe_allow_html=True)
            with col2:
                st.write(desc)

    st.markdown("---")
    st.markdown("### 📊 Live O2C Status Summary")
    status_order = ["Order Placed","Processing","Shipped","Delivered","Invoiced","Closed"]
    sc = fdf["order_status"].value_counts()
    colors = ["#94A3B8","#F59E0B","#60A5FA","#3B82F6","#2563EB","#1B2A4A"]
    cols = st.columns(6)
    for i, (s, c) in enumerate(zip(status_order, colors)):
        cnt = sc.get(s, 0)
        cols[i].markdown(f"""
        <div style='background:{c};color:white;border-radius:8px;padding:12px;text-align:center;'>
        <div style='font-size:1.5rem;font-weight:700;'>{cnt}</div>
        <div style='font-size:0.72rem;'>{s}</div></div>""", unsafe_allow_html=True)
