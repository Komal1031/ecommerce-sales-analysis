# E-commerce Sales Analysis
**Tools:** Python · Pandas · SQL (SQLite)  
**Author:** Komal Jadhwar

## 📌 Project Overview
Analyzed e-commerce sales data to identify top-performing products, customer purchase trends, and seasonal demand patterns. Used Pandas for data cleaning and exploratory analysis, and SQL queries for business insights.

## 🔍 Key Insights
- **Laptop** generated the highest revenue among all products
- **Electronics** category contributed 83% of total revenue
- **North region** led in both order volume and revenue
- **Q2 (Apr–Jun)** showed peak seasonal demand
- Average Order Value: ₹21,440

## 📊 Analysis Performed
| Area | Details |
|------|---------|
| Data Cleaning | Null checks, duplicate removal, data type validation |
| SQL Analysis | Top products, category breakdown, region sales, top customers |
| Pandas Analysis | Monthly trends, seasonal demand, best sellers |
| Reports | 5 CSV reports exported |

## 🗂️ Project Structure
```
ecommerce_analysis/
│
├── ecommerce_analysis.py   # Main analysis script
├── README.md               # Project documentation
└── reports/                # Generated CSV reports
    ├── top_products.csv
    ├── monthly_sales.csv
    ├── seasonal_demand.csv
    ├── region_sales.csv
    └── top_customers.csv
```

## ▶️ How to Run
```bash
# Install dependency
pip install pandas

# Run the analysis
python ecommerce_analysis.py
```

## 🛠️ Technologies Used
- **Python 3** — core scripting
- **Pandas** — data cleaning and analysis
- **SQLite / SQL** — business queries and aggregations
