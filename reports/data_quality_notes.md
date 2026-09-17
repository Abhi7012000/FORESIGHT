# FORESIGHT — Data Quality & Preparation Notes

## 1. Source Dataset

The project uses the Retail Store Inventory Forecasting Dataset as the source dataset.

The raw dataset contains:

- 73,100 rows
- 15 original columns
- Daily records from 2022-01-01 to 2024-01-01
- 5 stores
- 20 products
- 100 store-product combinations

The raw file is stored at:

`data/raw/retail_store_inventory.csv`

---

## 2. Data Preparation

The raw dataset was transformed into four analysis-ready tables:

1. `sales_daily.csv`
2. `sku_master.csv`
3. `calendar.csv`
4. `inventory_snapshots.csv`

The complete transformation is implemented in:

`src/pipeline.py`

The pipeline can be rerun from the raw data using:

```bash
python src/pipeline.py

Haan bhai, ab exact content daalte hain. 👍

### Step 86 — `data_quality_notes.md` me ye poora content paste karo

````markdown
# FORESIGHT — Data Quality & Preparation Notes

## 1. Source Dataset

The project uses the Retail Store Inventory Forecasting Dataset as the source dataset.

The raw dataset contains:

- 73,100 rows
- 15 original columns
- Daily records from 2022-01-01 to 2024-01-01
- 5 stores
- 20 products
- 100 store-product combinations

The raw file is stored at:

`data/raw/retail_store_inventory.csv`

---

## 2. Data Preparation

The raw dataset was transformed into four analysis-ready tables:

1. `sales_daily.csv`
2. `sku_master.csv`
3. `calendar.csv`
4. `inventory_snapshots.csv`

The complete transformation is implemented in:

`src/pipeline.py`

The pipeline can be rerun from the raw data using:

```bash
python src/pipeline.py
````

---

## 3. SKU Definition

A unique SKU was created using:

`Store ID + Product ID`

Example:

`S001_P0001`

This produces 100 unique SKUs.

This approach was used because the same product appears across multiple stores.

---

## 4. Sales Table

`sales_daily.csv` contains one record per SKU per day.

Columns:

* `date`
* `sku_id`
* `units_sold`
* `revenue`
* `unit_price`
* `discount_pct`
* `promo_flag`

Revenue was derived as:

`Units Sold × Price × (1 - Discount / 100)`

Sales data was aggregated from store-product-day level to SKU-day level.

---

## 5. SKU Master

`sku_master.csv` contains:

* `sku_id`
* `store_id`
* `product_id`

The source `Category` field was not used in the final SKU master because the same Product ID was associated with multiple categories in the source data.

Therefore, category information was not fabricated or arbitrarily assigned.

---

## 6. Calendar

`calendar.csv` contains:

* `date`
* `week`
* `month`

Week and month were derived from the date.

The source `Seasonality` and `Holiday/Promotion` fields were not treated as date-level calendar attributes because their values were not consistent for a given date across records.

A separate reliable holiday field was not available in the source dataset.

---

## 7. Inventory Snapshots

`inventory_snapshots.csv` contains:

* `date`
* `sku_id`
* `on_hand_units`
* `on_order_units`

The source dataset does not provide reliable `lead_time_days` or `reorder_point` fields.

These values were therefore not fabricated.

---

## 8. Data Quality Issues

### Negative Demand Forecast

The source dataset contains negative values in the `Demand Forecast` column.

These values are logically invalid for demand forecasting.

Negative forecast values were converted to missing values during processing.

The raw dataset was not modified.

### Zero Sales

Zero values in `Units Sold` were retained because zero demand can be a valid business observation.

### Missing Values

No missing values were found in the original dataset.

After processing, all four analysis-ready tables passed the missing-value validation.

### Duplicate Records

No exact duplicate rows were found in the raw dataset.

The processed tables also passed their primary-key uniqueness checks.

---

## 9. Validation

The following checks are performed automatically by `src/pipeline.py`:

* Primary-key uniqueness
* Missing-value checks
* Sales SKU to SKU master relationship
* Inventory SKU to SKU master relationship
* Sales date to calendar relationship
* Inventory date to calendar relationship

All validation checks passed.

---

## 10. Final Table Sizes

| Table               |   Rows | Columns |
| ------------------- | -----: | ------: |
| sales_daily         | 73,100 |       7 |
| sku_master          |    100 |       3 |
| calendar            |    731 |       3 |
| inventory_snapshots | 73,100 |       4 |

---

## 11. Important Limitations

The source dataset does not provide all fields specified in the project brief.

Unavailable or unsuitable fields include:

* `subcategory`
* `launch_date`
* `unit_cost`
* `list_price`
* `lead_time_days`
* `reorder_point`
* reliable date-level `is_holiday`

These fields have not been fabricated.

Any later forecasting or inventory-risk logic using these concepts must explicitly document the assumptions used.

```