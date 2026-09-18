# EDA & Data Quality Insight Memo

## 1. Dataset Overview

- **Daily sales records:** 73,100
- **Unique SKUs:** 100
- **Processed sales table:** 73,100 rows × 7 columns
- **Weekly forecasting dataset:** 10,400 rows × 4 columns
- **Forecasting period:** 3 January 2022 to 25 December 2023
- **Baseline evaluation period:** 2 January 2023 to 25 December 2023
- **Baseline evaluation rows:** 5,200

## 2. Data Quality Findings

### Zero-sales observations

- There are **360 zero-sales records**, representing **0.49%** of all daily records.
- **97 SKUs** have at least one zero-sales day.
- The maximum number of zero-sales days for any SKU is **8**.
- No SKU has zero total sales across the complete observed period.

**Handling / interpretation:** Zero-sales records were retained because they may represent genuine low-demand days and are relevant to inventory-risk analysis. They were not automatically removed or treated as missing values.

### Category consistency

The category consistency check found that product IDs can appear with multiple category values. The first ten product IDs in the check each showed **five distinct category values**.

**Business implication:** Product/category mapping should be validated before using category-level reporting for operational decisions. The current project keeps the available source data and documents this limitation rather than inventing a corrected mapping.

## 3. Demand Distribution and SKU Behaviour

- Average daily units sold: **136.46**
- Standard deviation: **108.92**
- Minimum daily units sold: **0**
- Maximum daily units sold: **499**
- The demand distribution is **right-skewed**, indicating that some observations have considerably higher demand than the typical day.
- The top 10 SKUs contribute **10.61%** of total units sold.
- The top 10 SKU total is **1,058,902 units**, out of **9,975,582 total units**.

### Dead-stock indicator

The analysis did not identify any SKU with zero total sales. However, 97 SKUs had at least one zero-sales day, so intermittent low-demand behaviour exists and should be monitored rather than automatically labelled as permanent dead stock.

## 4. Demand Drivers and Seasonality

### Promotion effect

| Promotion status | Average units sold |
|---|---:|
| No promotion | 136.51 |
| Promotion | 136.42 |

The average demand during promotion and non-promotion periods is very similar in this dataset. Promotion should therefore not be assumed to create a strong demand lift without additional product-level or campaign-level analysis.

### Day-of-week pattern

Average demand varies only slightly across weekdays:

- Monday: 135.09
- Tuesday: 137.31
- Wednesday: 136.62
- Thursday: 137.28
- Friday: 136.85
- Saturday: 135.31
- Sunday: 136.81

### Seasonal pattern

Average demand by season:

| Season | Average units sold |
|---|---:|
| Autumn | 137.78 |
| Winter | 136.83 |
| Spring | 135.83 |
| Summer | 135.43 |

Autumn has the highest average demand among the four recorded seasons, while Summer has the lowest. The difference is moderate rather than extreme.

### Monthly pattern

The monthly average demand ranges from approximately **134.03 units in December** to **139.44 units in July**. This indicates moderate monthly variation rather than a highly pronounced seasonal cycle.

## 5. Correlation Observations

- Units sold and revenue have a correlation of approximately **0.79**.
- The correlations of units sold with unit price, discount percentage, and promotion flag are close to zero in this dataset.

**Interpretation:** Revenue moves with units sold, while the available price, discount, and promotion fields do not show strong linear relationships with demand in this aggregated analysis. Correlation does not establish causation and should not be treated as proof that these variables have no predictive value at SKU or time-segment level.

## 6. Feature Engineering

The following features were created for forecasting:

- Lag features: 1-day, 7-day, and 14-day lags
- Rolling features: 7-day and 14-day rolling means
- Rolling 7-day standard deviation
- Calendar features: week, month, and day of week
- Promotion flag converted to an integer feature
- Weekly SKU-level demand created by aggregating daily sales

The rolling features use shifted values so that the current observation is not included in its own rolling calculation.

## 7. Baseline Result

The seasonal-naive baseline uses the previous year's demand for the same SKU and week.

- **Evaluation period:** 2 January 2023 to 25 December 2023
- **Evaluation rows:** 5,200
- **WAPE:** 33.71%

This baseline provides a reference point for judging whether the machine-learning forecasting models improve on a simple seasonal method.

## 8. Key Business Insights

1. **Demand is uneven:** The right-skewed distribution and wide range from 0 to 499 units indicate that inventory planning should account for demand variability rather than relying only on average demand.

2. **Intermittent zero-sales behaviour needs monitoring:** 97 SKUs have at least one zero-sales day, but none has zero total sales. These SKUs should be reviewed for intermittent demand, availability issues, or temporary low demand before being classified as dead stock.

3. **Promotion is not a clear demand driver in the current aggregate data:** Promotion and non-promotion average demand are nearly identical. Operational teams should validate campaign impact at SKU, category, and campaign level before assuming that discounts will increase demand.

4. **Seasonality is moderate:** Autumn has the highest average seasonal demand, while Summer has the lowest. Seasonal features may support forecasting, but the observed differences are not large enough to justify aggressive seasonal inventory changes on their own.

5. **Category reporting requires data validation:** Product IDs appear with multiple category values. Category-level decisions should therefore be treated cautiously until the product-category mapping is confirmed.

## 9. Limitations and Next Actions

- The analysis is based on the available source fields and does not prove causal relationships.
- Promotion impact should be analysed at SKU and campaign level.
- Product-category mapping should be validated with the source owner.
- Lead time and formal reorder-point inputs were not available in the current modelling data.
- Future analysis can add stock availability, lead time, campaign identifiers, and confirmed product master data.
