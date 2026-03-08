# ============================================================
# E-commerce Sales Analysis
# Tools: Python, Pandas, SQLite (SQL)
# Author: Komal Jadhwar
# Description: Analyze sales data to identify top products,
#              customer trends, and seasonal demand patterns
# ============================================================

import pandas as pd
import sqlite3
import os

# ── 1. CREATE SAMPLE DATASET ────────────────────────────────
print("=" * 55)
print("   E-COMMERCE SALES ANALYSIS")
print("=" * 55)

# Simulate realistic e-commerce data
data = {
    "order_id": range(1, 101),
    "order_date": pd.date_range(start="2024-01-05", periods=100, freq="3D"),
    "customer_id": [f"C{str(i % 30 + 1).zfill(3)}" for i in range(100)],
    "product": [
        "Laptop", "Mobile Phone", "Headphones", "Keyboard", "Mouse",
        "Monitor", "Tablet", "Charger", "Webcam", "Speaker"
    ] * 10,
    "category": [
        "Electronics", "Electronics", "Accessories", "Accessories", "Accessories",
        "Electronics", "Electronics", "Accessories", "Accessories", "Accessories"
    ] * 10,
    "quantity": [2, 1, 3, 1, 2, 1, 1, 4, 2, 3] * 10,
    "unit_price": [55000, 20000, 3500, 1500, 800, 18000, 30000, 1200, 4500, 3000] * 10,
    "region": ["North", "South", "East", "West", "North",
               "South", "East", "West", "North", "South"] * 10,
}

df = pd.DataFrame(data)
df["order_date"] = pd.to_datetime(df["order_date"])
df["total_sales"] = df["quantity"] * df["unit_price"]
df["month"] = df["order_date"].dt.month_name()
df["month_num"] = df["order_date"].dt.month

print("\n✅ Dataset created successfully!")
print(f"   Total Orders : {len(df)}")
print(f"   Date Range   : {df['order_date'].min().date()} to {df['order_date'].max().date()}")
print(f"   Products     : {df['product'].nunique()}")
print(f"   Customers    : {df['customer_id'].nunique()}")

# ── 2. DATA CLEANING ────────────────────────────────────────
print("\n" + "─" * 55)
print("STEP 1: DATA CLEANING")
print("─" * 55)
print(f"  Missing values   : {df.isnull().sum().sum()}")
print(f"  Duplicate rows   : {df.duplicated().sum()}")
print(f"  Data types       :\n{df.dtypes.to_string()}")

# ── 3. SQL ANALYSIS ─────────────────────────────────────────
print("\n" + "─" * 55)
print("STEP 2: SQL ANALYSIS")
print("─" * 55)

# Load into SQLite in-memory database
conn = sqlite3.connect(":memory:")
df.to_sql("sales", conn, index=False, if_exists="replace")

# SQL Query 1 — Top 5 Products by Revenue
q1 = """
    SELECT product,
           SUM(quantity) AS total_units_sold,
           SUM(total_sales) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
    LIMIT 5
"""
top_products = pd.read_sql(q1, conn)
print("\n📦 Top 5 Products by Revenue:")
print(top_products.to_string(index=False))

# SQL Query 2 — Sales by Category
q2 = """
    SELECT category,
           COUNT(order_id) AS total_orders,
           SUM(total_sales) AS total_revenue
    FROM sales
    GROUP BY category
    ORDER BY total_revenue DESC
"""
category_sales = pd.read_sql(q2, conn)
print("\n🗂️  Sales by Category:")
print(category_sales.to_string(index=False))

# SQL Query 3 — Sales by Region
q3 = """
    SELECT region,
           COUNT(order_id) AS total_orders,
           SUM(total_sales) AS revenue
    FROM sales
    GROUP BY region
    ORDER BY revenue DESC
"""
region_sales = pd.read_sql(q3, conn)
print("\n🌍 Sales by Region:")
print(region_sales.to_string(index=False))

# SQL Query 4 — Top 5 Customers by Spend
q4 = """
    SELECT customer_id,
           COUNT(order_id) AS orders_placed,
           SUM(total_sales) AS total_spend
    FROM sales
    GROUP BY customer_id
    ORDER BY total_spend DESC
    LIMIT 5
"""
top_customers = pd.read_sql(q4, conn)
print("\n👤 Top 5 Customers by Spend:")
print(top_customers.to_string(index=False))

conn.close()

# ── 4. PYTHON / PANDAS ANALYSIS ─────────────────────────────
print("\n" + "─" * 55)
print("STEP 3: PYTHON & PANDAS ANALYSIS")
print("─" * 55)

# Monthly Sales Trend
monthly = df.groupby(["month_num", "month"])["total_sales"].sum().reset_index()
monthly = monthly.sort_values("month_num")
monthly = monthly.rename(columns={"total_sales": "monthly_revenue"})
print("\n📅 Monthly Sales Trend:")
print(monthly[["month", "monthly_revenue"]].to_string(index=False))

# Seasonal demand (Q1-Q4)
df["quarter"] = df["order_date"].dt.quarter
seasonal = df.groupby("quarter")["total_sales"].sum().reset_index()
seasonal.columns = ["quarter", "revenue"]
seasonal["quarter"] = seasonal["quarter"].map({1: "Q1 (Jan-Mar)", 2: "Q2 (Apr-Jun)", 3: "Q3 (Jul-Sep)", 4: "Q4 (Oct-Dec)"})
print("\n🗓️  Seasonal Demand (Quarterly):")
print(seasonal.to_string(index=False))

# Average order value
avg_order = df["total_sales"].mean()
print(f"\n💰 Average Order Value : ₹{avg_order:,.0f}")

# Most popular product by quantity
top_qty = df.groupby("product")["quantity"].sum().idxmax()
print(f"🏆 Best Seller (Units) : {top_qty}")

# Highest revenue product
top_rev = df.groupby("product")["total_sales"].sum().idxmax()
print(f"💎 Highest Revenue     : {top_rev}")

# ── 5. SAVE REPORTS ─────────────────────────────────────────
print("\n" + "─" * 55)
print("STEP 4: SAVING REPORTS")
print("─" * 55)

os.makedirs("reports", exist_ok=True)
top_products.to_csv("reports/top_products.csv", index=False)
monthly[["month", "monthly_revenue"]].to_csv("reports/monthly_sales.csv", index=False)
seasonal.to_csv("reports/seasonal_demand.csv", index=False)
region_sales.to_csv("reports/region_sales.csv", index=False)
top_customers.to_csv("reports/top_customers.csv", index=False)

print("  ✅ reports/top_products.csv")
print("  ✅ reports/monthly_sales.csv")
print("  ✅ reports/seasonal_demand.csv")
print("  ✅ reports/region_sales.csv")
print("  ✅ reports/top_customers.csv")

print("\n" + "=" * 55)
print("   ANALYSIS COMPLETE")
print("=" * 55)
