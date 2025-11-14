# Supply Chain and sales analysis

* **Analyzed a 3-year online retail dataset (1.8L+ order-item transactions)** from DataCo, performing extensive data cleaning, deduplication, missing-value handling, zipcode reconciliation, and date standardization.

* **Computed 30+ business-critical KPIs** across logistics performance, customer behavior, profitability, cancellation/fraud risk, and region-wise contribution — uncovering system-wide delivery inefficiencies and revenue leakage.

* **Built a fully interactive Streamlit analytics dashboard** using Python, Plotly, and NumPy to visualize real-time insights on revenue, profit, inventory, shipping delays, churn, and customer segmentation.

* **Developed XGBoost models** — classifier to predict late deliveries and regressor to estimate shipment delays — plus exponential revenue forecasting to project the full-year 2018 revenue trajectory.

* **Performed customer clustering using RFM + behavioral variables** and segmented buyers into 4 actionable personas, exposing 25–30% untapped high-margin opportunity and misaligned premium-shipping experience.

* **Diagnosed systemic bottlenecks**: 57% late deliveries, 51% churn risk, 22% payment failures, and non-profitable product lines driving >19% loss-making orders.

* **Delivered a strategic 4-phase operational roadmap (0–3, 3–6, 6–12, 12+ months)** recommending premium-shipping redesign, pricing optimization, geographic expansion, predictive logistics, and partner renegotiation.


### **Tthe main causes of revenue leakage**
- Pending orders: 40% of all orders — huge working capital block.
- Pending Payment Status: 22% of transactions stuck, impacting cash flow.
- 19% orders unprofitable after costs
- 2018 profitability 35% below 2017
- Churn rate: ~51% — half of customers lapse after 240 days of inactivity
- Root causes: payment delays, pricing gaps, and supply chain inefficiency

### **Insights & Recommendations**
| **Category**       | **Challenge Identified**            | **Strategic Focus**                         |
| ------------------ | ----------------------------------- | ------------------------------------------- |
| Delivery & SLA     | 57% late deliveries                 | Predictive analytics + partner optimization |
| Customer Retention | 51% churn, 9-month lifespan, on an avg. orders after 60 days         | Loyalty & reactivation campaigns, Subscription on repeatable items            |
| Discounts      | 98% (nearly every order) Discounted order,    | Run A/B tests to understand which products can sustain reduced discounts without affecting conversion        |
| Profitability      | Low-margin SKUs, 19% loss orders    | Dynamic pricing & bundling                  |
| Working Capital    | 40% pending orders                  | Payment automation                          |
| Regional Growth    | Africa high-margin, low penetration | Targeted market pilots                      |
| Premium Shipping   | First-Class & Second-Class: 100% and 77% late or canceled respectively, 60% orders late delivery         | Suspend First/Second-Class upsells until premium service reliability improves, SLA segregation & tracking                  |

### Organizational Strategy — Implementation Roadmap
| **Phase**                     | **Initiatives**                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| **Immediate (0–3 months)**    | Fix premium shipping failures, optimize payment flows, high-margin bundling                    |
| **Short Term (3–6 months)**   | Pilot Africa market expansion, launch VIP loyalty program, implement route optimization        |
| **Medium Term (6–12 months)** | Deploy predictive analytics & delay models, establish regional hubs, optimize partner networks |
| **Long Term (12+ months)**    | Scale global expansion, integrate advanced AI/ML, introduce sustainable logistics initiatives  |

### Understanding the KPIs
- Churn Rate: percentage of customers who stop using the service during a specific period (Customers who did not order for > 240 days)
- Average Customer Lifespan: average length of time a customer remains a customer (here: average duration from a customer's first order until their last order)
- Customer LTV: total predicted revenue a customer will generate for the business over the entire period of their relationship (total amount of money an average customer is expected to spend from the store before they stop shopping there)

- Customers inactive for > 240 days were considered churned (50%)
- Average lifespan ≈ 280 days (~9.3 months).
- LTV = Avg Revenue per Customer × Avg Sales per Customer × (Avg Lifespan / 365)