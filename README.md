# stockwise-inventory-planner-
# StockWise 📦

**Inventory tracking and demand planning for small shops.**

StockWise is a lightweight inventory-planning prototype built with Python, Streamlit, and Pandas. It helps small shop owners monitor stock levels, estimate when products may run out, and plan replenishment.

## Features

- Editable inventory table
- Stockout estimates based on average daily sales
- Reorder points based on supplier lead time and safety stock
- Suggested reorder quantities
- Low-stock alerts and business insights
- Downloadable CSV inventory report

## How It Works

StockWise calculates a reorder point using:

`Reorder Point = Daily Sales × Lead Time + Safety Stock`

It then compares the current stock with the reorder point to suggest when and how much to reorder.

## Run Locally

1. Install Python.
2. Install the dependencies:

   `pip install streamlit pandas`

3. Run the application:

   `python -m streamlit run app.py`

## Technology

- Python
- Streamlit
- Pandas

## Current Status

Early-stage prototype using sample inventory data. It has not yet been validated with real shop owners or real sales records.

## Planned Improvements

- Sales history and demand forecasting
- Inventory data persistence
- Supplier and purchase-order tracking
- User feedback and real-world testing

---

Built as a learning project exploring inventory management, analytics, and practical decision support for small businesses.
