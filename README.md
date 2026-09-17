
# 📊 FORESIGHT
## Demand Forecasting & Inventory Risk Intelligence

FORESIGHT is a data-driven demand forecasting and inventory risk intelligence project designed to help businesses monitor demand, identify inventory risks, and support inventory planning decisions.

## 🚀 Project Features

- Demand forecasting and forecast monitoring
- Forecast vs actual demand comparison
- Inventory coverage analysis
- Inventory risk classification
- Prioritized reorder recommendations
- Markdown / clearance identification
- SKU-level risk analysis
- Model performance comparison
- Interactive Streamlit dashboard
- FastAPI service
- CSV export for filtered risk data

## 🏗️ Project Structure

```text
FORESIGHT/
│
├── app/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_check.ipynb
│   ├── 02_eda.ipynb
│   └── 03_modeling.ipynb
│
├── reports/
│
├── service/
│   ├── api.py
│   ├── requirements.txt
│   └── README.md
│
├── src/
│   └── pipeline.py
│
├── .gitignore
├── render.yaml
├── requirements.txt
└── README.md
```

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- FastAPI
- Matplotlib
- Jupyter Notebook
- Git & GitHub

## 📈 Dashboard Modules

1. KPI Metrics
2. Risk Overview
3. Forecast vs Actual
4. Forecast Uncertainty
5. Inventory Coverage
6. Prioritized Reorder List
7. Markdown / Clear List
8. Inventory Risk Decision Grid
9. Value at Risk Analysis
10. Model Performance
11. Executive Summary
12. Filtered Risk Data Download

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FORESIGHT
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Dashboard

```bash
streamlit run app/dashboard.py
```

## ▶️ Run the API

Start the FastAPI service using the command configured for the project.

Refer to `service/README.md` for API-specific instructions.

## 📊 Model Evaluation

The project includes model comparison and forecast error monitoring using WAPE.

The reported performance values should be interpreted with reference to the project's evaluation data and methodology.

## ⚠️ Data Notes

- Raw data is excluded from version control.
- Processed datasets are stored in `data/processed/`.
- Dataset limitations and quality notes are documented in the `reports/` directory.
- Forecast and inventory risk results depend on the available source data.

## 🔮 Future Improvements

- Automated data ingestion
- Real-time inventory updates
- Improved forecasting models
- Automated alerts for critical inventory risks
- Cloud deployment enhancements
- Role-based dashboard access

## 👨‍💻 Author

Abhinav Kumar Singh
Prachi Hedau
Bharath H R
## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.