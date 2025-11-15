# Supply Chain and sales analysis

The supply chain dataset on which the analysis is done is attached along with the files as `DataCoSupplyChainDataset.csv`. The full analysis is done on `Analysis.ipynb`. The `customer_clusters.csv` has all the customers segmented into 5 categories.

## Overview

* **Analysed a 3-year online retail dataset (1.8L+ order-item transactions)** from DataCo, performing rigorous data cleaning, deduplication, missing-value imputation, ZIP-code reconciliation, and full date standardization to convert item-level entries into reliable order- and customer-level aggregates.

* **Computed 30+ operational, customer, and financial KPIs** covering delivery performance, churn behavior, discount dependency, regional contribution, SKU profitability, fraud hotspots, and working-capital risks which revealed the structural inefficiencies and revenue leakage across the supply chain.

* **Developed an interactive, multi-tab Streamlit dashboard** using Python, Plotly, and NumPy to visualize real-time insights on revenue, profit, shipping delays, churn, category margins, fraud regions, and geographic order heatmaps.

* **Built a 2-layer XGBoost model** — a classifier to predict late deliveries (SLA breaches) and a regressor to predict shipment delays — enabling proactive logistics routing and risk-aware order handling.

* **Performed customer segmentation using K-Means clustering** and identified **5 high-impact customer personas**, uncovering a 25–30% margin uplift opportunity and mismatches in the premium shipping experience.

* **Implemented exponential forecasting** using log-linear regression to project full-year 2018 revenue & profit, accounting for partial Jan-2018 data and month-wise trend momentum lost during 2017.

* **Diagnosed key bottlenecks** such as **57% late deliveries**, **51% churn risk**, **98% discount dependency**, **22% payment failures**, and **19% loss-making orders**, highlighting critical operational leakage points.

* **Delivered a 4-phase strategic roadmap (0–3, 3–6, 6–12, 12+ months)** recommending premium-shipping redesign, discount optimization, predictive logistics, market-specific expansion, SKU rationalization, and partner renegotiation for sustainable margin improvement.

---

## Understanding the KPIs
- Churn Rate: percentage of customers who stop using the service during a specific period (Customers who did not order for > 240 days)
- Average Customer Lifespan: average length of time a customer remains a customer (here: average duration from a customer's first order until their last order)
- Customer LTV: total predicted revenue a customer will generate for the business over the entire period of their relationship (total amount of money an average customer is expected to spend from the store before they stop shopping there)

- Customers inactive for > 240 days were considered churned (50%)
- Average lifespan ≈ 280 days (~9.3 months).
- LTV = Avg Revenue per Customer × Avg Sales per Customer × (Avg Lifespan / 365)

## The main causes of revenue leakage
- Pending orders: 40% of all orders — huge working capital block.
- Pending Payment Status: 22% of transactions stuck, impacting cash flow.
- 19% orders unprofitable after costs
- 2018 profitability 35% below 2017
- Churn rate: ~51% — half of customers lapse after 240 days of inactivity
- Root causes: payment delays, pricing gaps, and supply chain inefficiency

---

## The 5 Customer Clusters

### Cluster 0 – “Mass-Market High-Variety Buyers”

**Type:** General, diverse, multi-category shoppers
**Cluster Size:** 11,687 customers (largest)
**Revenue Share:** 91.95% (dominant)

**Characteristics**

* High order count per customer (≈5 orders)
* High variety: many categories & many countries (broad demand pattern)
* Moderate recency → periodic repeat buyers
* Medium delay rate (54%)
* Mix of Standard (61%) and Second-Class (18%) shipping

### Cluster 1 – “Delay-Prone Low-Frequency Buyers”**

**Type:** Low-engagement, operationally risky
**Cluster Size:** 1,812
**Revenue Share:** 1.98%

**Characteristics**

* Low frequency (~1 order)
* High delay rate (78%)
* Dominated by **Second-Class shipping (98%)**
* Higher-than-average profit margin
* Medium recency (inactive recently)

### Cluster 2 – “Standard-Class Low-Touch Value Customers”

**Type:** Simple, low-maintenance buyers
**Cluster Size:** 679
**Revenue Share:** 0.69%

**Characteristics**

* Low frequency (~1 order)
* Lower delay rate (46%)
* Strong preference for **Standard Class (73%)**
* Slightly negative profit margin (due to discounts)
* Small basket sizes

### Cluster 3 – “Price-Sensitive Occasional Buyers (High On-Time Rate)”

**Type:** Low recency, stable, low-risk
**Cluster Size:** 5,048
**Revenue Share:** 3.82%

**Characteristics**

* Very low delay rate (37%) – *best logistics behavior*
* High Standard-Class usage (91%)
* Low frequency (≈1)
* Moderate variety, small baskets
* Negative average delay (delivered before schedule)

### Cluster 4 – “Premium Service Buyers with Extreme Delay Issues”

**Type:** Premium shipping, extremely late
**Cluster Size:** 1,426
**Revenue Share:** 1.56%

**Characteristics**

* **98% First-Class usage**, but **94.8% late rate**
* Low frequency (~1)
* Higher than average profit margins
* High delay & high dissatisfaction risk
* One of the worst segments operationally

---

## Insights & Recommendations

| **Category**           | **Challenge Identified**                                                                                        | **Strategic Recommendations (Stronger & More Actionable)**                                                                                                                                                                                                      |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Delivery & SLA**     | • 57% late deliveries  • Premium shipping models consistently fail  • Intercontinental routes highly unreliable | • Segment logistics partners by region (EU, Americas, APAC) and route type (air/sea)  • Introduce **Predictive Delay Engine** using XGBoost outputs for proactive re-routing  • Redesign premium shipping with guaranteed SLA, penalty clauses & priority lanes |
| **Customer Retention** | • 51% churn rate • Avg. lifespan 9 months • Avg. 60-day reorder gap                                             | • Launch tiered **Loyalty Program** (Silver/Gold/Elite) based on RFM score  • Introduce replenishment subscriptions for recurring-use SKUs  • Personalized reactivation journeys using past order behavior                                                      |
| **Fraud Detection**    | • 9 products & 3 regions account for 60% of fraud • High-risk ZIP clusters                                      | • Build **Product-Level Fraud Score** based on ZIP code, discount usage & order velocity  • Vendor audit for high-fraud SKUs  • Deploy address verification, device fingerprinting & anomaly detection                                                          |
| **Discount Strategy**  | • 98% of orders discounted • Avg discount = $21 • Margin dilution on bestsellers                                | • Run A/B price elasticity tests per category  • Set **Discount Guardrails**—minimum required margin per product  • Migrate to **behavior-based discounting** (repeat buyers get benefits, not all buyers)                                                      |
| **Profitability**      | • 19% orders sold at a loss • Low-margin SKUs eroding performance                                               | • Dynamic pricing tied to competitor & demand signals  • Bundle low-margin SKUs with top sellers  • Rationalize unprofitable SKUs and renegotiate supplier terms                                                                                                |
| **Working Capital**    | • 23% orders stuck in pending payment • $8M revenue + $900K profit locked                                       | • One-click payment UX revamp + auto-retry logic  • Introduce alternate payments (UPI, wallets, BNPL)  • Automate reconciliation to reduce payment friction                                                                                                     |
| **Regional Growth**    | • Africa = +32% higher margin but only 2% penetration • Overdependence on Europe & Central America              | • Launch **Africa-focused product catalog**  • Partner with regional logistics firms  • Targeted marketing via localized campaigns                                                                                                                              |
| **Product Growth**     | • Fitness category = 45% margin but low sales • High revenue concentration in apparel/footwear                  | • Create premium bundles & influencer partnerships for Fitness vertical  • Expand SKU depth in high-margin categories  • Cross-sell fitness items during sports/seasonal campaigns                                                                              |


## Organizational Strategy — Implementation Roadmap

### Phase 1 — Immediate (0–3 Months)

**Objective: Stabilize delivery operations & stop financial leakage**

* Establish a **Premium Delivery Taskforce** to fix SLA failures
* Resolve payment flow friction (auto-retry, simplified checkout, alternate methods)
* Deploy **SKU-level profitability dashboards** and kill-loss SKUs
* Introduce **high-margin bundles** (Fitness, Accessories, Lifestyle)
* Quick-win route optimization for delayed intercontinental segments


### Phase 2 — Short Term (3–6 Months)

**Objective: Build predictive capabilities & unlock customer value**

* Deploy **Predictive Delay Model** into operations workflow (XGBoost output → routing actions)
* Launch **VIP customer program** for top 5% customers (85% revenue retention)
* Implement **regional route optimization** using shipping performance data
* Roll out **discount A/B tests** to cut unnecessary margin loss
* Introduce **fraud risk scoring** at SKU, ZIP and region level


### Phase 3 — Medium Term (6–12 Months)

**Objective: Expand capacity and optimize the supply chain end-to-end**

* Pilot operations in **Africa**, the highest-margin region
* Establish **Regional Hubs** (EU, Americas, APAC) for better SLA performance
* Integrate **logistics partner scorecarding** with penalty/reward structure
* Expand dynamic pricing to category-level elasticity models
* Implement **automated replenishment orders** for repeatable SKUs


### Phase 4 — Long Term (12+ Months)

**Objective: Scale globally, digitize operations, and ensure sustainable growth**

* Roll out **global expansion blueprint** for new markets
* Integrate **advanced AI/ML forecasting**, including demand sensing and optimal inventory placement
* Transition to an **API-first logistics architecture** with real-time carrier updates
* Build sustainability program: route carbon optimization, reducing packaging waste, green logistics
* Implement **end-to-end supply chain digital twin** for scenario simulation