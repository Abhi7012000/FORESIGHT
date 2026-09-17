
from fastapi import FastAPI
from pydantic import BaseModel, field_validator
import joblib
import os
import pandas as pd


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "processed",
    "foresight_model.pkl"
)

model = joblib.load(MODEL_PATH)


app = FastAPI(
    title="FORESIGHT Scoring Service",
    description="Demand forecasting and inventory risk scoring API",
    version="1.0.0"
)


class ForecastRequest(BaseModel):
    sku_id: str

    lag_1_week: float
    lag_4_week: float
    lag_52_week: float

    promo_rate: float
    avg_discount_pct: float

    rolling_mean_4_week: float
    rolling_std_4_week: float

    month: int
    week_of_year: int

    week_sin: float
    week_cos: float

    on_hand_units: float
    on_order_units: float
    unit_price: float

    @field_validator(
        "lag_1_week",
        "lag_4_week",
        "lag_52_week",
        "promo_rate",
        "avg_discount_pct",
        "rolling_mean_4_week",
        "rolling_std_4_week",
        "month",
        "week_of_year",
        "on_hand_units",
        "on_order_units",
        "unit_price"
    )
    @classmethod
    def values_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError("Value cannot be negative")
        return value


class BatchForecastRequest(BaseModel):
    requests: list[ForecastRequest]


def build_model_features(request):

    return pd.DataFrame([{
        "lag_1_week": request.lag_1_week,
        "lag_4_week": request.lag_4_week,
        "lag_52_week": request.lag_52_week,
        "promo_rate": request.promo_rate,
        "avg_discount_pct": request.avg_discount_pct,
        "rolling_mean_4_week": request.rolling_mean_4_week,
        "rolling_std_4_week": request.rolling_std_4_week,
        "month": request.month,
        "week_of_year": request.week_of_year,
        "week_sin": request.week_sin,
        "week_cos": request.week_cos
    }])


def calculate_forecast(request):

    features = build_model_features(request)

    prediction = model.predict(features)[0]
    prediction = max(float(prediction), 0)

    available_inventory = (
        request.on_hand_units + request.on_order_units
    )

    stockout_shortfall = max(
        prediction - available_inventory,
        0
    )

    overstock_excess = max(
        available_inventory - prediction,
        0
    )

    if stockout_shortfall > 0:
        risk_level = "Reorder Now"
        recommended_action = "Reorder inventory"

    elif overstock_excess > 0:
        risk_level = "Markdown/Clear"
        recommended_action = "Markdown or clear stock"

    else:
        risk_level = "Healthy"
        recommended_action = "No immediate action"

    rupee_value_at_risk = (
        stockout_shortfall * request.unit_price
    )

    return {
        "sku_id": request.sku_id,
        "forecast": round(prediction, 2),
        "available_inventory": round(available_inventory, 2),
        "stockout_shortfall_units": round(stockout_shortfall, 2),
        "overstock_excess_units": round(overstock_excess, 2),
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "rupee_value_at_risk": round(rupee_value_at_risk, 2)
    }


@app.get("/")
def home():

    return {
        "message": "FORESIGHT Scoring Service is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "FORESIGHT Scoring Service"
    }


@app.post(
    "/forecast",
    summary="Forecast and risk score for one SKU",
    response_description="Forecast and inventory risk result"
)
def forecast(request: ForecastRequest):

    return calculate_forecast(request)


@app.post(
    "/forecast/batch",
    summary="Forecast and risk score for multiple SKUs",
    response_description="Batch forecast and inventory risk results"
)
def forecast_batch(request: BatchForecastRequest):

    results = []

    for item in request.requests:
        results.append(calculate_forecast(item))

    return {
        "results": results
    }