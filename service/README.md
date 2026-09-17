
# FORESIGHT Scoring Service

The FORESIGHT Scoring Service provides demand forecasts and inventory risk scores for individual SKUs or multiple SKUs.

The service is built using **FastAPI** and a trained machine learning model.

## Features

- Weekly demand forecasting
- Individual SKU forecasting
- Batch forecasting for multiple SKUs
- Inventory availability calculation
- Stockout shortfall detection
- Overstock excess detection
- Risk level classification
- Recommended inventory action
- Rupee value at risk calculation
- Input validation
- Interactive API documentation

## Technology Stack

- Python
- FastAPI
- Pydantic
- Pandas
- Joblib
- Uvicorn
- Machine Learning Model

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| POST | `/forecast` | Forecast and risk score for one SKU |
| POST | `/forecast/batch` | Forecast and risk score for multiple SKUs |

## Forecast Input

The forecast endpoint accepts the following fields:

| Field | Type | Description |
|---|---|---|
| `sku_id` | string | Unique SKU identifier |
| `lag_1_week` | float | Demand from previous week |
| `lag_4_week` | float | Demand from four weeks earlier |
| `lag_52_week` | float | Demand from same period in previous year |
| `promo_rate` | float | Promotion rate |
| `avg_discount_pct` | float | Average discount percentage |
| `rolling_mean_4_week` | float | Four-week rolling demand mean |
| `rolling_std_4_week` | float | Four-week rolling demand standard deviation |
| `month` | integer | Month number |
| `week_of_year` | integer | Week number of the year |
| `week_sin` | float | Cyclic week sine feature |
| `week_cos` | float | Cyclic week cosine feature |
| `on_hand_units` | float | Current inventory units |
| `on_order_units` | float | Inventory units already ordered |
| `unit_price` | float | Price per unit |

## Machine Learning Features

The model uses the following 11 features:

1. `lag_1_week`
2. `lag_4_week`
3. `lag_52_week`
4. `promo_rate`
5. `avg_discount_pct`
6. `rolling_mean_4_week`
7. `rolling_std_4_week`
8. `month`
9. `week_of_year`
10. `week_sin`
11. `week_cos`

## Forecast Output

The service returns:

- SKU ID
- Forecast demand
- Available inventory
- Stockout shortfall units
- Overstock excess units
- Risk level
- Recommended action
- Rupee value at risk

## Risk Logic

### Reorder Now

Returned when forecast demand is greater than available inventory.

### Markdown/Clear

Returned when available inventory is greater than forecast demand.

### Healthy

Returned when inventory is sufficient and there is no excess inventory.

## Example Request

```json
{
  "sku_id": "SKU_001",
  "lag_1_week": 150,
  "lag_4_week": 140,
  "lag_52_week": 130,
  "promo_rate": 0.1,
  "avg_discount_pct": 5,
  "rolling_mean_4_week": 145,
  "rolling_std_4_week": 20,
  "month": 12,
  "week_of_year": 50,
  "week_sin": -0.24,
  "week_cos": 0.97,
  "on_hand_units": 100,
  "on_order_units": 50,
  "unit_price": 250
}
```

## Example Response

```json
{
  "sku_id": "SKU_001",
  "forecast": 894.37,
  "available_inventory": 150,
  "stockout_shortfall_units": 744.37,
  "overstock_excess_units": 0,
  "risk_level": "Reorder Now",
  "recommended_action": "Reorder inventory",
  "rupee_value_at_risk": 186092.83
}
```

## Run the Service

Run the following command from the project root directory:

```bash
uvicorn service.api:app --reload
```

The service will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Interactive Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

## Validation

The API validates input values and returns HTTP status code `422` for invalid input.

For example:

- Negative demand values are rejected.
- Negative inventory values are rejected.
- Missing required fields are rejected.
- Incorrect data types are rejected.

## Project Scope

This service supports weekly demand forecasting and inventory risk scoring.

It does not include:

- Live inventory integrations
- Automated purchase orders
- Supplier selection
- Price optimization
- Real-time streaming
- Full inventory optimization