# EDA Insight Memo

The dataset contains 100 SKUs across 73,100 daily records.

Demand is right-skewed, and the top 10 SKUs contribute 10.61% of total units sold. There are 360 zero-sales records, representing 0.49% of all records.

Promotion and non-promotion periods show very similar average demand. Weekly demand also shows only small variation across days, while seasonal demand varies moderately.

Lag, rolling, calendar, and promotion features were engineered for forecasting.

The seasonal-naive baseline uses the previous year's same-week demand and achieves a WAPE of 33.71% on the 2023 evaluation period.
