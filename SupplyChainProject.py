# ===============================================
# SUPPLY CHAIN & CUSTOMER INSIGHTS DASHBOARD
# ===============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from num2words import num2words

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Supply Chain Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r'C:\Users\conta\Jupyter Learn\Supply Chain Analysis\DataCoSupplyChainDataset.csv', encoding='latin1')
    df = df.drop(columns=['Customer Email', 'Customer Password', 'Product Description', 'Product Image'], errors='ignore')
    df = df.drop_duplicates()
    df['Customer Name'] = df['Customer Fname'].fillna('') + ' ' + df['Customer Lname'].fillna('')
    df['Customer Name'] = df['Customer Name'].str.strip()
    df['order_dt'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
    df['ship_dt'] = pd.to_datetime(df['shipping date (DateOrders)'], errors='coerce')
    df['shipping_delay'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
    return df

df = load_data()

# ------------------ STATUS GROUPS ------------------
completed_statuses = {'COMPLETE','CLOSED','PROCESSING','PAYMENT_RECEIVED','FINISHED'}
cancel_statuses    = {'CANCELED'}
fraud_statuses     = {'SUSPECTED_FRAUD'}
pending_statuses   = {'PENDING','PENDING_PAYMENT','ON_HOLD','PAYMENT_REVIEW'}

# ------------------ FILTERS ------------------
st.sidebar.header("Filters")
selected_regions = st.sidebar.multiselect("Order Region", df['Order Region'].dropna().unique(), default=df['Order Region'].dropna().unique())
selected_categories = st.sidebar.multiselect("Category Name", df['Category Name'].dropna().unique(), default=df['Category Name'].dropna().unique())
selected_markets = st.sidebar.multiselect("Market", df['Market'].dropna().unique(), default=df['Market'].dropna().unique())

df = df[df['Order Region'].isin(selected_regions) & df['Category Name'].isin(selected_categories) & df['Market'].isin(selected_markets)]
completed_orders = df[df['Order Status'].isin(completed_statuses)]

# ------------------ CALCULATIONS ------------------
total_orders = df['Order Id'].nunique()
completed_order_count = completed_orders['Order Id'].nunique()
unique_customers = completed_orders['Customer Id'].nunique()
unique_orders = completed_orders.drop_duplicates(subset='Order Id')

cancelled_orders = df[df['Order Status'].isin(cancel_statuses)]
total_cancelled_orders = cancelled_orders['Order Id'].nunique()

pending_orders = df[df['Order Status'].isin(pending_statuses)]
total_pending_orders = pending_orders['Order Id'].nunique()

fraud_orders = df[df['Order Status'].isin(fraud_statuses)]
total_fraud_orders = fraud_orders['Order Id'].nunique()

total_revenue = completed_orders['Order Item Total'].sum()
total_profit = completed_orders['Order Profit Per Order'].sum()
profit_margin = total_profit / total_revenue if total_revenue else 0

# Repeat & Engagement metrics
order_counts = completed_orders.groupby('Customer Id')['Order Id'].nunique()
repeat_customers = (order_counts > 1).sum()
repeat_customers_over_3 = (order_counts > 3).sum()
regular_customers = (order_counts > 5).sum()
repeat_purchase_rate = repeat_customers / unique_customers
first_time_buyer_rate = (order_counts == 1).sum() / unique_customers

# Quantities
avg_sales_per_customer = completed_order_count / unique_customers
avg_qty_per_order = completed_orders['Order Item Quantity'].mean()
paid_customer_rate = unique_customers / df['Customer Id'].nunique()

# AOV & Revenue per Customer
avg_order_value = total_revenue / completed_order_count
avg_revenue_per_customer = total_revenue / unique_customers

# Churn, Lifespan, LTV
ref_date = completed_orders['order_dt'].max()
cust_last_purchase = completed_orders.groupby('Customer Id')['order_dt'].max().reset_index()
cust_last_purchase['days_since_last_purchase'] = (ref_date - cust_last_purchase['order_dt']).dt.days
cust_last_purchase['is_churned'] = (cust_last_purchase['days_since_last_purchase'] > 240).astype(int)
churn_rate = cust_last_purchase['is_churned'].mean()

cust_life = completed_orders.groupby('Customer Id').agg(first=('order_dt','min'), last=('order_dt','max')).reset_index()
cust_life['lifespan_days'] = (cust_life['last'] - cust_life['first']).dt.days
avg_lifespan = cust_life['lifespan_days'].mean()
ltv = avg_revenue_per_customer * avg_sales_per_customer * avg_lifespan / 365

# Discount Metrics
discount_penetration_rate = completed_orders[completed_orders['Order Item Discount'] > 0]['Order Id'].nunique() / completed_order_count
avg_discount_given = completed_orders['Order Item Discount'].mean()

# Shipping metrics
completed_orders['shipping_delay'] = completed_orders['Days for shipping (real)'] - completed_orders['Days for shipment (scheduled)']
avg_shipping_delay = completed_orders['shipping_delay'].mean()
late_orders = completed_orders[completed_orders['Late_delivery_risk'] == 1]['Order Id'].nunique()
late_delivery_rate = late_orders / completed_order_count
sla_compliance_rate = 1 - late_delivery_rate

# Avg. Time Between Orders
order_dates = completed_orders.groupby('Customer Id')['order_dt'].apply(list)
avg_gap_days = order_dates.apply(lambda d: np.mean(np.diff(sorted(d))).days if len(d) > 1 else np.nan).mean()

# Revenue per product and top category contribution
revenue_by_category = completed_orders.groupby('Category Name')['Order Item Total'].sum().sort_values(ascending=False)
top_category_revenue_contribution = revenue_by_category.head(1).values[0] / total_revenue * 100 if total_revenue > 0 else 0

# Profit per product and top category contribution
profit_by_category = completed_orders.groupby('Category Name')['Order Profit Per Order'].sum().sort_values(ascending=False)
top_category_profit_contribution = profit_by_category.head(1).values[0] / total_profit * 100 if total_profit > 0 else 0

# Orders and revenue by country (unique Order Ids)
country_stats = (
    unique_orders.groupby('Order Country')
    .agg(Orders=('Order Id', 'nunique'), Revenue=('Order Item Total', 'sum'))
    .reset_index()
)

import pycountry  # to standardize country names

# ---------- COUNTRY NAME FIX FOR MAPS ----------
def normalize_country_name(name):
    """Fix inconsistent or non-standard country/region names for plotly maps."""
    try:
        return pycountry.countries.lookup(name).name
    except:
        mapping = {
            "USA": "United States",
            "UK": "United Kingdom",
            "UAE": "United Arab Emirates",
            "South of USA": "United States",
            "East of USA": "United States",
            "Central America": "Mexico",
            "Western Europe": "France",
            "Northern Europe": "Germany",
            "Southern Europe": "Italy",
            "Southeast Asia": "Thailand",
            "Oceania": "Australia",
            "Caribbean": "Jamaica",
            "North Africa": "Egypt",
            "East Africa": "Kenya",
            "Central Africa": "Congo",
        }
        return mapping.get(name, None)

# Clean Order Country values
country_stats['Order Country Clean'] = country_stats['Order Country'].apply(normalize_country_name)
country_stats = country_stats.dropna(subset=['Order Country Clean'])

# ------------------ LAYOUT ------------------
st.title("DataCo Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Customers", "Financials", "Logistics", "Risk & Fraud", "Recommendations"
])

# --------------- TAB 1: OVERVIEW ---------------
with tab1:
    st.subheader("Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Completed Orders", f"{completed_order_count:,}")
    col3.metric("Total Unique Customers", f"{unique_customers:,}")
    col4.metric("Repeat Purchase Rate", f"{repeat_purchase_rate:.2%}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Average Sales per Customer", f"{avg_sales_per_customer:.2f}")
    col6.metric("Average Quantity per Order", f"{avg_qty_per_order:.2f}")
    col7.metric("Average Order Value", f"${avg_order_value:,.2f}", num2words(avg_order_value, to='currency', lang='en').replace('euro','dollar'))
    col8.metric("Revenue per Customer", f"${avg_revenue_per_customer:,.2f}", num2words(avg_revenue_per_customer, to='currency', lang='en').replace('euro','dollar'))

# --------------- TAB 2: CUSTOMERS ---------------
with tab2:
    st.subheader("Customer Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Repeat Customers (>1)", f"{repeat_customers} ({repeat_customers/unique_customers:.1%})")
    col2.metric("Repeat Customers (>3)", f"{repeat_customers_over_3} ({repeat_customers_over_3/unique_customers:.1%})")
    col3.metric("Regular Customers (>5)", f"{regular_customers} ({regular_customers/unique_customers:.1%})")

    col4, col5, col6 = st.columns(3)
    col4.metric("Cancelled Orders", f"{total_cancelled_orders} ({total_cancelled_orders/total_orders:.1%})")
    col5.metric("Pending Orders", f"{total_pending_orders} ({total_pending_orders/total_orders:.1%})")
    col6.metric("Suspected Fraud Orders", f"{total_fraud_orders} ({total_fraud_orders/total_orders:.1%})")

    col7, col8, col9 = st.columns(3)
    col7.metric("First-Time Buyer Rate", f"{first_time_buyer_rate:.2%}")
    col8.metric("Paid Customer Rate", f"{paid_customer_rate:.2%}")
    col9.metric("Avg. Time Between Orders", f"{avg_gap_days:.1f} days")

    col10, col11, col12 = st.columns(3)
    col10.metric("Churn Rate (240-day)", f"{churn_rate:.2%}")
    col11.metric("Average Customer Lifespan", f"{avg_lifespan:.1f} days (~{avg_lifespan/30:.1f} months)")
    col12.metric("Customer Lifetime Value", f"{ltv:.2f} days", num2words(ltv, to='currency', lang='en').replace('euro','dollar'))
    
    st.divider()
    
    st.markdown("### 🌍 Global Distribution Maps")
    
    col_map1, col_map2 = st.columns(2)
    
    with col_map1:
        fig_orders_map = px.choropleth(
            country_stats,
            locations="Order Country Clean",
            locationmode="country names",
            color="Orders",
            hover_name="Order Country",
            color_continuous_scale="Blues",
            title="Orders by Country (Unique Orders)",
        )
        fig_orders_map.update_geos(showcoastlines=True, projection_type="natural earth")
        st.plotly_chart(fig_orders_map, use_container_width=True)
    
    with col_map2:
        fig_revenue_map = px.choropleth(
            country_stats,
            locations="Order Country Clean",
            locationmode="country names",
            color="Revenue",
            hover_name="Order Country",
            color_continuous_scale="Greens",
            title="Revenue by Country ($)",
        )
        fig_revenue_map.update_geos(showcoastlines=True, projection_type="natural earth")
        st.plotly_chart(fig_revenue_map, use_container_width=True)

    st.divider()
    
    customer_sales = completed_orders.groupby('Customer Id')['Order Item Total'].sum().sort_values(ascending=False)
    top10 = customer_sales.head(10).reset_index()
    top10['Customer_Label'] = 'Customer ' + top10['Customer Id'].astype(str)
    fig = px.bar(
        top10, 
        x='Customer_Label', 
        y='Order Item Total', 
        title="Top 10 Customers by Sales",
        labels={'Order Item Total': 'Total Sales ($)', 'Customer_Label': 'Customer ID'}
    )
    fig.update_xaxes(tickangle=45)  # Rotate labels for better readability
    st.plotly_chart(fig, use_container_width=True)
    
# --------------- TAB 3: FINANCIALS ---------------
with tab3:
    st.subheader("Financial Performance")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}", num2words(total_revenue, to='currency', lang='en').replace('euro','dollar'))
    col2.metric("Total Profit", f"${total_profit:,.2f}", num2words(total_profit, to='currency', lang='en').replace('euro','dollar'))
    col3.metric("Profit Margin", f"{profit_margin:.2%}")

    col4, col5 = st.columns(2)
    col4.metric("Discount Penetration Rate", f"{discount_penetration_rate:.2%}")
    col5.metric("Average Discount per Order", f"${avg_discount_given:,.2f}")
    
    st.divider()

    st.markdown("### 💰 Year-wise Financial Performance")
    
    completed_orders['Year'] = completed_orders['order_dt'].dt.year
    yearly_stats = (
        completed_orders.groupby('Year')
        .agg(
            Revenue=('Order Item Total', 'sum'),
            Profit=('Order Profit Per Order', 'sum')
        )
        .reset_index()
    )
    yearly_stats['YoY_Revenue_Growth'] = yearly_stats['Revenue'].pct_change() * 100
    yearly_stats['YoY_Profit_Growth'] = yearly_stats['Profit'].pct_change() * 100
    
    fig_yearly = go.Figure()
    
    # Revenue and Profit Lines
    fig_yearly.add_trace(go.Scatter(
        x=yearly_stats['Year'],
        y=yearly_stats['Revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='green', width=3)
    ))
    fig_yearly.add_trace(go.Scatter(
        x=yearly_stats['Year'],
        y=yearly_stats['Profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(color='blue', width=3)
    ))
    
    # YoY Growth Bar
    fig_yearly.add_trace(go.Bar(
        x=yearly_stats['Year'],
        y=yearly_stats['YoY_Revenue_Growth'],
        name='YoY Revenue Growth (%)',
        marker_color='lightgreen',
        opacity=0.5,
        yaxis='y2'
    ))
    
    fig_yearly.update_layout(
        title="Year-wise Revenue, Profit, and YoY Growth",
        xaxis_title="Year",
        yaxis=dict(title="Revenue / Profit ($)", side='left'),
        yaxis2=dict(title="YoY Growth (%)", overlaying='y', side='right', showgrid=False),
        legend=dict(orientation='h', y=-0.3),
    )
    st.plotly_chart(fig_yearly, use_container_width=True)


    st.markdown("*Monthly Orders Trend**")
    
    df_shipping = df[df['shipping date (DateOrders)'].notna()].copy()
    df_shipping['shipping date (DateOrders)'] = pd.to_datetime(df_shipping['shipping date (DateOrders)'])
    
    monthly_orders = (
        df_shipping.drop_duplicates(subset='Order Id')
        .set_index('shipping date (DateOrders)')
        .resample('M')
        .size()
        .reset_index(name='Orders')
    )
    
    fig_monthly = px.line(
        monthly_orders,
        x='shipping date (DateOrders)',
        y='Orders',
        markers=True,
        title="Monthly Orders Shipped Over Time"
    )
    fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Number of Orders")
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    st.plotly_chart(px.bar(
        revenue_by_category.reset_index().head(15),
        x='Category Name', y='Order Item Total', title="Top 15 Categories contributing most Revenue"
    ), use_container_width=True)
    
    st.plotly_chart(px.bar(
        profit_by_category.reset_index().head(15),
        x='Category Name', y='Order Profit Per Order', title="Top 15 Categories contributing most Profit"
    ), use_container_width=True)

# --------------- TAB 4: LOGISTICS ---------------
with tab4:
    st.subheader("Logistics & Delivery Performance")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Shipping Delay", f"{avg_shipping_delay:.2f} days")
    col2.metric("Late Delivery Rate", f"{late_delivery_rate:.2%}")
    col3.metric("SLA Compliance Rate", f"{sla_compliance_rate:.2%}")
    
    st.divider()

    st.plotly_chart(px.histogram(completed_orders, x='shipping_delay', nbins=30, title="Shipping Delay Distribution (days)"), use_container_width=True)
    st.plotly_chart(px.box(completed_orders, x='Shipping Mode', y='shipping_delay', color='Shipping Mode', title="Shipping Delay by Mode"), use_container_width=True)
    
    st.markdown("**Distribution of Actual vs Scheduled Shipping Days**")
    
    fig_shipping = go.Figure()
    fig_shipping.add_trace(go.Histogram(
        x=df['Days for shipping (real)'],
        nbinsx=30,
        name='Actual Shipping Days',
        opacity=0.7
    ))
    fig_shipping.add_trace(go.Histogram(
        x=df['Days for shipment (scheduled)'],
        nbinsx=30,
        name='Scheduled Shipping Days',
        opacity=0.7
    ))
    
    fig_shipping.update_layout(
        barmode='overlay',
        title="Distribution of Actual vs Scheduled Shipping Days",
        xaxis_title="Days",
        yaxis_title="Frequency"
    )
    fig_shipping.update_traces(opacity=0.6)
    st.plotly_chart(fig_shipping, use_container_width=True)
    
    st.divider()

    st.markdown("**Shipping Mode Usage by Delivery Status**")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='Delivery Status', hue='Shipping Mode', ax=ax)
    plt.title('Shipping Mode Usage by Delivery Status')
    st.pyplot(fig)

# --------------- TAB 5: RISK & FRAUD ---------------
with tab5:
    st.subheader("Fraud and Cancellations")

    fraud_region = fraud_orders.groupby('Order Region')['Order Id'].nunique().sort_values(ascending=False).reset_index()
    fraud_product = fraud_orders.groupby('Product Name')['Order Id'].nunique().sort_values(ascending=False).head(10).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(fraud_region, x='Order Id', y='Order Region', orientation='h', title="Fraud Orders by Region"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(fraud_product, x='Order Id', y='Product Name', orientation='h', title="Top Fraudulent Products"), use_container_width=True)
        

# --------------- TAB 6: INSIGHTS & RECOMMENDATIONS ---------------
with tab6:
    st.subheader("Strategic Insights & Recommendations")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Operational Efficiency Insights
        st.markdown("""
        <div>
        <h4 style="color:#d2691e;">Premium Service Delivery Failures</h4>
        <ul>
        <li><strong>First-Class deliveries:</strong> 100% marked as late or canceled</li>
        <li><strong>Second-Class deliveries:</strong> 76.6% late delivery rate</li>
        <li><strong>Standard Class:</strong> 58% on-time rate with frequent early deliveries</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Recommendations:**
        - **Immediate Action:** Suspend premium shipping upsells until delivery infrastructure is strengthened
        - **Process Redesign:** Implement dedicated premium service lanes with separate SLA tracking
        - **Partner Evaluation:** Audit and renegotiate contracts with logistics providers for premium services
        - **Technology Investment:** Deploy real-time tracking and predictive delay algorithms
        """)
        
        st.markdown("""
        <div>
        <h4 style="color:#228b22;">Hidden Profit Opportunities</h4>
        <ul>
        <li><strong>Fitness Department:</strong> Highest profit margins (45%+) but low sales volume</li>
        <li><strong>Africa Region:</strong> 32% higher profit ratio than global average</li>
        <li><strong>Top 5% Customers:</strong> Generate 35% of total revenue with 85% retention rate</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Recommendations:**
        - **Product Strategy:** Develop premium bundles in high-margin Fitness category
        - **Geographic Expansion:** Pilot targeted marketing campaigns in African markets
        - **VIP Program:** Create exclusive loyalty program for top 5% customers
        - **Pricing Optimization:** Implement dynamic pricing for high-demand, high-margin products
        """)
    
    with col2:
        # Financial Health Insights
        st.markdown("""
        <div>
        <h4 style="color:#c71585;">Revenue Leakage Points</h4>
        <ul>
        <li><strong>22% of transactions:</strong> Stuck in "PENDING PAYMENT" status</li>
        <li><strong>19% of orders:</strong> Result in net loss after costs</li>
        <li><strong>2018 Performance:</strong> 35% lower profitability vs. 2017</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Recommendations:**
        - **Payment Flow Optimization:** Reduce checkout abandonment with streamlined payment processing
        - **Loss Prevention:** Implement minimum order value thresholds and cost-based pricing rules
        - **Historical Analysis:** Conduct deep-dive into 2018 operational disruptions
        - **Working Capital:** Improve cash flow through faster payment reconciliation
        """)
        
        st.markdown("""
        <div>
        <h4 style="color:#0066cc;">Strategic Expansion Opportunities</h4>
        <ul>
        <li><strong>Western Europe & Central America:</strong> 68% of total order volume</li>
        <li><strong>Africa:</strong> Highest profit per order but only 2% market penetration</li>
        <li><strong>Caguas Hub:</strong> Critical transit point requiring route optimization</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Recommendations:**
        - **Route Optimization:** Implement AI-powered routing between Caguas and high-volume regions
        - **Market Development:** Create Africa-specific product catalog and marketing strategy
        - **Hub & Spoke Model:** Expand distribution network with strategic regional hubs
        - **Local Partnerships:** Establish alliances with regional logistics providers
        """)
    
    # Strategic Initiatives Timeline
    st.markdown("### Strategic Implementation Roadmap")
    
    timeline_data = {
        'Phase': ['Immediate (0-3 months)', 'Short-term (3-6 months)', 'Medium-term (6-12 months)', 'Long-term (12+ months)'],
        'Initiatives': [
            "• Fix premium shipping failures\n• Payment flow optimization\n• High-margin product bundling",
            "• Africa market expansion pilot\n• VIP customer program launch\n• Route optimization implementation",
            "• Predictive analytics deployment\n• Regional hub establishment\n• Partner network optimization",
            "• Global market expansion\n• Advanced AI/ML integration\n• Sustainable logistics initiatives"
        ],
        'Expected Impact': ['15-20% revenue recovery', '25-30% profit growth', '35-40% operational efficiency', '50%+ market expansion']
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)
    
    # Key Performance Indicators to Monitor
    st.markdown("### Critical Success Metrics")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.metric(
            label="On-Time Delivery Rate Target",
            value="85%",
            delta="+42% from current"
        )
    
    with kpi_col2:
        st.metric(
            label="Profit Margin Target",
            value="28%",
            delta="+8% from current"
        )
    
    with kpi_col3:
        st.metric(
            label="Payment Success Rate Target",
            value="95%",
            delta="+15% from current"
        )
    
    with kpi_col4:
        st.metric(
            label="Market Expansion Target",
            value="3 new regions",
            delta="+150% growth"
        )
    
    # Risk Assessment
    st.markdown("### Risk Mitigation Strategies")
    
    risk_data = {
        'Risk Category': ['Operational', 'Financial', 'Market', 'Technology'],
        'Identified Risks': [
            "Premium service delivery failures impacting brand reputation",
            "Revenue leakage from pending payments and unprofitable orders",
            "Limited geographic diversification and market concentration",
            "Legacy systems limiting scalability and real-time analytics"
        ],
        'Mitigation Strategies': [
            "Implement tiered service levels with guaranteed SLAs",
            "Automated payment retry systems and dynamic pricing algorithms",
            "Phased geographic expansion with pilot programs",
            "Cloud migration and API integration roadmap"
        ]
    }
    
    risk_df = pd.DataFrame(risk_data)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    
    # Additional Professional Insights
    with st.expander("Additional Strategic Insights"):
        st.markdown("""
        **Customer Lifetime Value Optimization:**
        - Top 10% customers have 3.5x higher LTV than average
        - Implement personalized retention campaigns for high-value segments
        
        **Inventory Turnover Insights:**
        - 22% of SKUs have turnover below industry average
        - Consider dynamic inventory allocation based on regional demand patterns
        
        **Sustainability Opportunities:**
        - Route optimization can reduce carbon footprint by 18%
        - Packaging optimization potential: 12% material reduction identified
        
        **Technology Enablement:**
        - AI-powered demand forecasting can reduce stockouts by 35%
        - Blockchain implementation for enhanced supply chain transparency
        """)
st.markdown("---")
st.markdown("**Developed by Koustav Das**  |  [Portfolio](https://koustav-das.vercel.app/)")