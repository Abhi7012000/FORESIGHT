"""
Universal data loader for the FORESIGHT demand forecasting application.

This module accepts a business CSV file, standardizes common column-name
variations, validates the minimum required fields, and creates a consistent
schema for downstream processing.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

import pandas as pd


# Canonical column names used by the application.
COLUMN_ALIASES: Dict[str, List[str]] = {
    "date": [
        "date",
        "day",
        "timestamp",
        "transaction_date",
        "order_date",
        "sales_date",
    ],
    "store_id": [
        "store_id",
        "store",
        "shop_id",
        "branch_id",
        "location_id",
    ],
    "product_id": [
        "product_id",
        "product",
        "sku",
        "sku_id",
        "item_id",
        "item",
    ],
    "category": [
        "category",
        "product_category",
        "item_category",
        "department",
    ],
    "units_sold": [
        "units_sold",
        "quantity",
        "qty",
        "sales_quantity",
        "units",
        "demand",
    ],
    "price": [
        "price",
        "unit_price",
        "selling_price",
        "sale_price",
    ],
    "discount": [
        "discount",
        "discount_pct",
        "discount_percent",
        "markdown",
    ],
    "inventory_level": [
        "inventory_level",
        "inventory",
        "stock",
        "stock_level",
        "available_stock",
    ],
    "units_ordered": [
        "units_ordered",
        "order_quantity",
        "replenishment_quantity",
    ],
    "weather": [
        "weather",
        "weather_condition",
        "climate",
    ],
    "promotion": [
        "promotion",
        "holiday_promotion",
        "promo",
        "promo_flag",
        "is_promotion",
    ],
}


def _normalise_name(name: object) -> str:
    """Convert a column name into a comparable snake_case form."""
    value = str(name).strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _build_alias_lookup() -> Dict[str, str]:
    lookup: Dict[str, str] = {}

    for canonical_name, aliases in COLUMN_ALIASES.items():
        for alias in [canonical_name, *aliases]:
            lookup[_normalise_name(alias)] = canonical_name

    return lookup


ALIAS_LOOKUP = _build_alias_lookup()


def standardize_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Standardize recognized column names.

    Returns:
        standardized dataframe
        mapping of original column names to canonical names
    """
    rename_map: Dict[str, str] = {}

    for original_name in df.columns:
        normalized_name = _normalise_name(original_name)
        canonical_name = ALIAS_LOOKUP.get(normalized_name)

        if canonical_name:
            rename_map[original_name] = canonical_name

    standardized = df.rename(columns=rename_map).copy()

    # Avoid duplicate columns after alias mapping.
    duplicated_columns = standardized.columns[standardized.columns.duplicated()].tolist()
    if duplicated_columns:
        raise ValueError(
            "Multiple input columns mapped to the same canonical column: "
            f"{sorted(set(duplicated_columns))}"
        )

    return standardized, rename_map


def create_sku_id(df: pd.DataFrame) -> pd.DataFrame:
    """Create a stable SKU identifier when product/store information exists."""
    result = df.copy()

    if "sku_id" in result.columns:
        result["sku_id"] = result["sku_id"].astype(str)
    elif "product_id" in result.columns and "store_id" in result.columns:
        result["sku_id"] = (
            result["store_id"].astype(str).str.strip()
            + "_"
            + result["product_id"].astype(str).str.strip()
        )
    elif "product_id" in result.columns:
        result["sku_id"] = result["product_id"].astype(str).str.strip()

    return result


def validate_data(
    df: pd.DataFrame,
    require_date: bool = True,
    require_demand: bool = True,
) -> Dict[str, object]:
    """
    Validate the standardized dataframe.

    The loader requires a date and demand/units-sold column for forecasting.
    Other business columns are optional.
    """
    required_columns: List[str] = []

    if require_date:
        required_columns.append("date")

    if require_demand:
        if "units_sold" not in df.columns:
            return {
                "valid": False,
                "missing_columns": ["units_sold"],
                "message": (
                    "A demand column is required. Supported examples include "
                    "units_sold, quantity, qty, sales_quantity, units, or demand."
                ),
            }

        required_columns.append("units_sold")

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        return {
            "valid": False,
            "missing_columns": missing_columns,
            "message": f"Missing required columns: {missing_columns}",
        }

    result = {
        "valid": True,
        "missing_columns": [],
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "null_counts": {
            str(column): int(count)
            for column, count in df.isna().sum().items()
            if int(count) > 0
        },
        "message": "Data passed the minimum structural validation.",
    }

    return result


def prepare_uploaded_data(
    df: pd.DataFrame,
    parse_dates: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Standardize, prepare, and validate an uploaded business dataframe.
    """
    if df is None or df.empty:
        raise ValueError("The uploaded file is empty.")

    prepared, rename_map = standardize_columns(df)

    if parse_dates and "date" in prepared.columns:
        prepared["date"] = pd.to_datetime(prepared["date"], errors="coerce")

    numeric_columns = [
        "units_sold",
        "price",
        "discount",
        "inventory_level",
        "units_ordered",
    ]

    for column in numeric_columns:
        if column in prepared.columns:
            prepared[column] = pd.to_numeric(prepared[column], errors="coerce")

    prepared = create_sku_id(prepared)
    validation = validate_data(prepared)

    metadata = {
        "rename_map": rename_map,
        "validation": validation,
        "recognized_columns": [
            column for column in COLUMN_ALIASES if column in prepared.columns
        ],
        "unrecognized_columns": [
            column
            for column in prepared.columns
            if column not in COLUMN_ALIASES and column != "sku_id"
        ],
    }

    return prepared, metadata


def load_csv_file(file_or_path) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Load a CSV from a Streamlit UploadedFile or a filesystem path."""
    df = pd.read_csv(file_or_path)
    return prepare_uploaded_data(df)
