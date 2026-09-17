import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "retail_store_inventory.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"


# Step 1: Load raw data

def load_raw_data():
    """Load the raw retail inventory dataset."""

    df = pd.read_csv(RAW_PATH)

    return df

# Step 2: Prepare base data


def prepare_base_data(df):
    """Prepare basic data types and create SKU ID."""

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Create unique SKU = Store + Product
    df["sku_id"] = (
        df["Store ID"].astype(str)
        + "_"
        + df["Product ID"].astype(str)
    )

    # Negative demand forecasts are invalid.
    # Mark them as missing instead of changing the raw data.
    df["Demand Forecast"] = df["Demand Forecast"].mask(
        df["Demand Forecast"] < 0
    )

    return df



# Step 3: Create sales_daily

def create_sales_daily(df):
    """Create the analysis-ready sales_daily table."""

    # Calculate revenue after discount
    df["revenue"] = (
        df["Units Sold"]
        * df["Price"]
        * (1 - df["Discount"] / 100)
    )

    # Aggregate store-product data to SKU-day level
    sales_daily = (
        df.groupby(["Date", "sku_id"])
        .agg(
            units_sold=("Units Sold", "sum"),
            revenue=("revenue", "sum"),
            unit_price=("Price", "mean"),
            discount_pct=("Discount", "mean"),
            promo_flag=("Holiday/Promotion", "max")
        )
        .reset_index()
    )

    # Standardize column name
    sales_daily = sales_daily.rename(
        columns={"Date": "date"}
    )

    # Arrange columns
    sales_daily = sales_daily[
        [
            "date",
            "sku_id",
            "units_sold",
            "revenue",
            "unit_price",
            "discount_pct",
            "promo_flag"
        ]
    ]

    return sales_daily

def create_sku_master(df):
    """Create the SKU master table."""

    sku_master = (
        df[["sku_id", "Store ID", "Product ID"]]
        .drop_duplicates()
        .sort_values("sku_id")
        .reset_index(drop=True)
    )

    sku_master = sku_master.rename(
        columns={
            "Store ID": "store_id",
            "Product ID": "product_id"
        }
    )

    return sku_master

def create_calendar(df):
    """Create the calendar table."""

    calendar = (
        df[["Date"]]
        .drop_duplicates()
        .copy()
    )

    calendar["week"] = calendar["Date"].dt.isocalendar().week.astype(int)
    calendar["month"] = calendar["Date"].dt.month

    calendar = calendar.rename(
        columns={"Date": "date"}
    )

    calendar = calendar[
        [
            "date",
            "week",
            "month"
        ]
    ].sort_values("date").reset_index(drop=True)

    return calendar


def create_inventory_snapshots(df):
    """Create the inventory snapshots table."""

    inventory_snapshots = df[
        [
            "Date",
            "sku_id",
            "Inventory Level",
            "Units Ordered"
        ]
    ].copy()

    inventory_snapshots = inventory_snapshots.rename(
        columns={
            "Date": "date",
            "Inventory Level": "on_hand_units",
            "Units Ordered": "on_order_units"
        }
    )

    return inventory_snapshots


def validate_tables(sales_daily, sku_master, calendar, inventory_snapshots):
    """Run basic data-quality checks on all processed tables."""

    print("\nRunning data-quality checks...")

    # Primary key checks
    assert not sales_daily.duplicated(
        ["date", "sku_id"]
    ).any(), "Duplicate found in sales_daily"

    assert not sku_master.duplicated(
        ["sku_id"]
    ).any(), "Duplicate found in sku_master"

    assert not calendar.duplicated(
        ["date"]
    ).any(), "Duplicate found in calendar"

    assert not inventory_snapshots.duplicated(
        ["date", "sku_id"]
    ).any(), "Duplicate found in inventory_snapshots"

    # Missing-value checks
    assert not sales_daily.isnull().any().any(), \
        "Missing value found in sales_daily"

    assert not sku_master.isnull().any().any(), \
        "Missing value found in sku_master"

    assert not calendar.isnull().any().any(), \
        "Missing value found in calendar"

    assert not inventory_snapshots.isnull().any().any(), \
        "Missing value found in inventory_snapshots"

    # Referential integrity
    master_skus = set(sku_master["sku_id"])

    assert set(sales_daily["sku_id"]).issubset(master_skus), \
        "Sales SKU missing from sku_master"

    assert set(inventory_snapshots["sku_id"]).issubset(master_skus), \
        "Inventory SKU missing from sku_master"

    calendar_dates = set(calendar["date"])

    assert set(sales_daily["date"]).issubset(calendar_dates), \
        "Sales date missing from calendar"

    assert set(inventory_snapshots["date"]).issubset(calendar_dates), \
        "Inventory date missing from calendar"

    print("✓ Primary keys are unique")
    print("✓ No missing values")
    print("✓ SKU relationships are valid")
    print("✓ Date relationships are valid")
    print("✓ All quality checks passed!")



# Main program

if __name__ == "__main__":

    # Load raw data
    df = load_raw_data()

    # Prepare base data
    df = prepare_base_data(df)

    # Create all project tables
    sales_daily = create_sales_daily(df)
    sku_master = create_sku_master(df)
    calendar = create_calendar(df)
    inventory_snapshots = create_inventory_snapshots(df)

    validate_tables(
    sales_daily,
    sku_master,
    calendar,
    inventory_snapshots
    )

    # Save processed files
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    sales_daily.to_csv(
        PROCESSED_PATH / "sales_daily.csv",
        index=False
    )

    sku_master.to_csv(
        PROCESSED_PATH / "sku_master.csv",
        index=False
    )

    calendar.to_csv(
        PROCESSED_PATH / "calendar.csv",
        index=False
    )

    inventory_snapshots.to_csv(
        PROCESSED_PATH / "inventory_snapshots.csv",
        index=False
    )

    # Summary
    print("Raw data loaded successfully!")
    print("Raw shape:", df.shape)
    print("Unique SKUs:", df["sku_id"].nunique())

    print("\nProcessed tables created:")
    print("sales_daily:", sales_daily.shape)
    print("sku_master:", sku_master.shape)
    print("calendar:", calendar.shape)
    print("inventory_snapshots:", inventory_snapshots.shape)
    print("\nAll 4 files saved successfully!")

    print("\nAll 4 files saved successfully!")