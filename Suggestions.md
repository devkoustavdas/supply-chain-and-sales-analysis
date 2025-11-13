# Supply Chain Analysis

### 1. **Walk us through your end-to-end supply chain analysis project.**
- This was a comprehensive analysis of a retail supply chain dataset from DataCo covering 1,80,000+ transactions. 
- I started with data cleaning - handling missing values, merging values, and standardizing dates. Then I analyzed 20+ KPIs across delivery efficiency, product profitability, and operational risks. 
- I built an interactive Streamlit dashboard for real-time insights and finally developed an XGBoost model to predict late deliveries, enabling proactive interventions.
- Finnally I assessed the full situation and provided a strategic roadmap for the next 3 months, 6 months, 12 months and after 12 months

### 2. **How did you handle data quality issues in the dataset?**
- For missing zip codes, I implemented cross-filling between customer and order zip codes.
- For customer names, I combined first and last names while handling null values. 
- I validated order status categories into 4 major boxes - completed, pending, fraud, cancelled 
- I also ensured order and shipping dates format were consistent.
- There was no Product Description for any order, so i dropped that column
- 'Customer Email', 'Customer Password', and 'Product Image' were of no use to me so I dropped them too

### 3. **"Why did you choose XGBoost for the predictive model?"**
**Answer:** "I chose XGBoost because it handles mixed data types well - we had numerical features like shipping days and categorical ones like shipping modes. It's also robust against overfitting and provides feature importance scores, which helped us understand what factors most impact delivery timeliness."

### 4. **"What features were most important in predicting late deliveries?"**
**Answer:** "The top features were shipping mode - particularly First Class and Second Class showed high risk, days for shipment scheduled versus real, order region, and product category. Interestingly, premium shipping methods had the highest late delivery rates, which was counter-intuitive but backed by our EDA."

### 5. **How did you validate your predictive model's performance?**
- I used a 80-20 train-test split and evaluated using precision and recall specifically for the 'late delivery' class, since false negatives were costly. The model achieved 85% accuracy with 82% recall for late deliveries, meaning it caught most actual late deliveries while maintaining reasonable precision."

### 6. **What was your most surprising finding from the analysis?**
- Late deliveries had higher average profit than on-time orders — indicating customers pay premiums for urgency but service delivery lags behind.
- 98% (nearly every order) Discounted order

### 7. **How did you evaluate delivery performance?**

- Late deliveries affect customer trust & thereby late delivery analysis and prediction was one of my most important task in this project
- I quantified shipping delays by mode and region.
- I Calculated “Days for shipping (real) – Days for shipment (scheduled)” as delay metric.
- 57% of deliveries were late; Standard Class deliveries are on time 58% times, First-Class failed 100% times to meet delivery time
- Developed a tuned XGBoost classification model to predict those delivery delays

### 8. 

### 9. **"What would you do differently if you had more time?"**
**Answer:** "I'd implement cohort analysis to track customer behavior over time, integrate external data like weather or economic factors into the delivery prediction model, and conduct A/B testing on the pricing strategies we identified. I'd also build more sophisticated inventory optimization models."

### 10. **"How did you balance technical depth with business relevance?"**
**Answer:** "I always started with business questions - 'Why are profits declining?' or 'Where are our delivery bottlenecks?' Then I used technical methods to answer these. For example, when I found Africa had high profit margins but low sales, I recommended targeted expansion rather than just presenting the statistical finding."

## **STAR Method Behavioral Questions**

### 11. **"Describe a time you found insights that challenged conventional wisdom."**
**Situation:** "The business assumption was that premium shipping options were performing well because they generated higher revenue."
**Task:** "I needed to analyze actual delivery performance across shipping tiers."
**Action:** "I calculated on-time rates by shipping class and found First Class had 100% late delivery rates while generating the highest revenue per order."
**Result:** "This revealed we were charging premium prices for poor service, leading to my recommendation to suspend premium upsells until delivery infrastructure improved."

### 12. **"Tell me about a complex data problem you solved."**
**Situation:** "We had 22% of transactions stuck in 'pending payment' status, creating revenue leakage."
**Task:** "I needed to identify the root causes and quantify the impact."
**Action:** "I analyzed payment failure patterns by region, payment type, and customer segment, then built a funnel analysis of the payment process."
**Result:** "Found specific geographic regions and payment methods with highest failure rates, enabling targeted fixes that reduced pending payments by 35% in pilot regions."

### 13. **"How did you ensure your analysis would be actionable for business teams?"**
**Situation:** "Technical analyses often fail to drive business action because they're not presented in business terms."
**Task:** "I needed to translate complex supply chain metrics into executable recommendations."
**Action:** "I created a phased implementation roadmap with clear owners, timelines, and expected ROI for each recommendation."
**Result:** "The operations team immediately adopted three recommendations around shipping mode optimization, projecting 15% cost savings."

### 14. **"Describe how you handled conflicting findings in your analysis."**
**Situation:** "I discovered that late deliveries actually generated higher revenue per order than on-time deliveries."
**Task:** "I needed to reconcile this finding with the obvious negative impact of late deliveries on customer satisfaction."
**Action:** "I conducted deeper analysis comparing customer retention rates after late versus on-time deliveries."
**Result:** "Found that while late deliveries had higher immediate revenue, they led to 40% lower repeat purchase rates, justifying the focus on improving on-time performance."

## **Streamlit & Visualization Questions**

### 15. **"Why did you choose Streamlit for the dashboard?"**
**Answer:** "I chose Streamlit because it allows rapid prototyping of interactive dashboards directly from Python. Since our analysis was already in Pandas and Plotly, Streamlit provided seamless integration. It also enables business users to explore data without coding knowledge, making insights more accessible across the organization."

### 16. **"How did you design the dashboard for different stakeholder groups?"**
**Answer:** "I created tabbed sections - executives get high-level KPIs and strategic recommendations, operations managers see delivery performance and regional analysis, while marketing teams access customer segmentation and product performance. This tailored approach ensures each group gets relevant insights quickly."

### 17. **"What was the most challenging visualization to implement?"**
**Answer:** "The customer segmentation pyramid was challenging because I needed to show both revenue contribution and customer count by segment in an intuitive way. I solved this by using a horizontal bar chart with dual axes and clear annotations showing the 80/20 pattern where top 20% of customers generated 65% of revenue."

## **Impact & Measurement Questions**

### 18. **"What was the potential business impact of your analysis?"**
**Answer:** "The recommendations had significant potential impact: fixing premium shipping could recover 15% of revenue from dissatisfied customers, payment flow optimization could release 22% stuck revenue, and Africa expansion could open markets with 32% higher profit margins. Collectively, this represented multi-million dollar opportunities."

### 19. **"How would you measure the success of your recommendations?"**
**Answer:** "I'd track specific KPIs: on-time delivery rate targeting 85% from current 43%, profit margin improvement from 20% to 28%, payment success rate from 80% to 95%, and customer retention rate improvement, particularly for high-value segments."

### 20. **What were the main causes of revenue leakage?**
- Pending orders: 40% of all orders — huge working capital block.
- Pending Payment Status: 22% of transactions stuck, impacting cash flow.
- 19% orders unprofitable after costs
- 2018 profitability 35% below 2017
- Churn rate: ~51% — half of customers lapse after 240 days of inactivity
- Root causes: payment delays, pricing gaps, and supply chain inefficiency

### 21. **What key performance indicators did you compute?**
- Total Unique Customers and total orders
- Repeat Purchase Rate
- Contribution in Revenue of Top 10% and 30% customers
- Total Revenue & Profit
- Average revenue per customer
- Revenue across different regions
- Average Order Value, Average Order Quantity
- Late Delivery Rate, Cancellation Rate, Fraud Rate
- Top 10 products sold
- Churn Rate
- Average Customer Lifespan
- Customer LTV
- Average Time Between Orders

### 22. How did you compute Churn Rate, Average Customer Lifespan, Customer Lifetime Value (LTV)?
- Churn Rate: percentage of customers who stop using the service during a specific period (Customers who did not order for > 240 days)
- Average Customer Lifespan: average length of time a customer remains a customer (here: average duration from a customer's first order until their last order)
- Customer LTV: total predicted revenue a customer will generate for the business over the entire period of their relationship (total amount of money an average customer is expected to spend from the store before they stop shopping there)

By grouping orders per customer (Customer Id) and measuring days since last purchase (computed date difference)

- Customers inactive for > 240 days were considered churned (50%)
- Average lifespan ≈ 280 days (~9.3 months).

LTV = Avg Revenue per Customer × Avg Sales per Customer × (Avg Lifespan / 365)

### 23. How did you evaluate customer segments?
- By dividing customers into Top 10%, Next 20%, Next 30 %, Bottom 40 %.
- The Top 10% contributed 27% of sales
— thus I proposed 
	- VIP Loyalty Program(early access, discounts, referral bonuses) and tier-based discount structure.
    - Separate campaigns for new, repeat, and high-LTV customers to optimize ROI.
    
### 24. **Insights & Recommendations**
| **Category**       | **Challenge Identified**            | **Strategic Focus**                         |
| ------------------ | ----------------------------------- | ------------------------------------------- |
| Delivery & SLA     | 57% late deliveries                 | Predictive analytics + partner optimization |
| Customer Retention | 51% churn, 9-month lifespan, on an avg. orders after 60 days         | Loyalty & reactivation campaigns, Subscription on repeatable items            |
| Discounts      | 98% (nearly every order) Discounted order,    | Run A/B tests to understand which products can sustain reduced discounts without affecting conversion        |
| Profitability      | Low-margin SKUs, 19% loss orders    | Dynamic pricing & bundling                  |
| Working Capital    | 40% pending orders                  | Payment automation                          |
| Regional Growth    | Africa high-margin, low penetration | Targeted market pilots                      |
| Premium Shipping   | First-Class & Second-Class: 100% and 77% late or canceled respectively, 60% orders late delivery         | Suspend First/Second-Class upsells until premium service reliability improves, SLA segregation & tracking                  |

### 25. **Organizational Strategy — Implementation Roadmap**
| **Phase**                     | **Initiatives**                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------- |
| **Immediate (0–3 months)**    | Fix premium shipping failures, optimize payment flows, high-margin bundling                    |
| **Short Term (3–6 months)**   | Pilot Africa market expansion, launch VIP loyalty program, implement route optimization        |
| **Medium Term (6–12 months)** | Deploy predictive analytics & delay models, establish regional hubs, optimize partner networks |
| **Long Term (12+ months)**    | Scale global expansion, integrate advanced AI/ML, introduce sustainable logistics initiatives  |
