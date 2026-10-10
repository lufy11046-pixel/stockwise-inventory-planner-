import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="StockWise", page_icon="📦", layout="wide")

st.title("📦 StockWise")
st.caption("Simple inventory and demand planning for small shops")

if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"Product": "Rice (kg)", "Stock": 25, "Daily Sales": 4, "Lead Time": 3, "Safety Stock": 5},
        {"Product": "Cooking Oil (L)", "Stock": 12, "Daily Sales": 2, "Lead Time": 4, "Safety Stock": 3},
        {"Product": "Eggs (pieces)", "Stock": 60, "Daily Sales": 10, "Lead Time": 2, "Safety Stock": 15},
        {"Product": "Lentils (kg)", "Stock": 18, "Daily Sales": 1, "Lead Time": 5, "Safety Stock": 4},
    ])

st.subheader("Inventory dashboard")
st.write("Edit the table below to match your shop's inventory.")

edited = st.data_editor(
    st.session_state.inventory,
    num_rows="dynamic",
    use_container_width=True,
    key="inventory_editor",
    column_config={
        "Stock": st.column_config.NumberColumn(min_value=0, step=1),
        "Daily Sales": st.column_config.NumberColumn(min_value=0, step=1),
        "Lead Time": st.column_config.NumberColumn(min_value=0, step=1),
        "Safety Stock": st.column_config.NumberColumn(min_value=0, step=1),
    },
)

df = edited.copy()
for col in ["Stock", "Daily Sales", "Lead Time", "Safety Stock"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["Days Left"] = df.apply(
    lambda row: round(row["Stock"] / row["Daily Sales"], 1)
    if row["Daily Sales"] > 0 else float("inf"),
    axis=1,
)

df["Reorder Point"] = df["Daily Sales"] * df["Lead Time"] + df["Safety Stock"]
df["Suggested Order"] = (
    df["Reorder Point"] - df["Stock"]
).clip(lower=0).apply(lambda x: int(x + 0.999999))

df["Status"] = df.apply(
    lambda row: "🔴 Reorder now"
    if row["Stock"] <= row["Reorder Point"]
    else ("🟡 Running low" if row["Days Left"] <= 7 else "🟢 Healthy"),
    axis=1,
)

total_products = len(df)
urgent = int((df["Status"] == "🔴 Reorder now").sum())
low = int((df["Status"] == "🟡 Running low").sum())

a, b, c = st.columns(3)
a.metric("Products tracked", total_products)
b.metric("Need reordering", urgent)
c.metric("Running low", low)

st.subheader("Stock alerts")
st.dataframe(
    df[["Product", "Stock", "Daily Sales", "Days Left",
        "Reorder Point", "Suggested Order", "Status"]],
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "Download inventory report (CSV)",
    df.to_csv(index=False).encode("utf-8"),
    file_name="stockwise_inventory_report.csv",
    mime="text/csv",
)

st.info("Planning estimates only. Actual demand and supplier lead times may vary.")
st.divider()
st.subheader("📊 Business Insights")

if not df.empty:
    valid_sales = df[df["Daily Sales"] > 0].copy()

    if not valid_sales.empty:
        fastest = valid_sales.sort_values("Days Left").iloc[0]
        st.metric(
            "First product likely to run out",
            str(fastest["Product"]),
            f'{fastest["Days Left"]:.1f} days of stock left'
        )

        priority = df.sort_values(
            ["Status", "Days Left"],
            ascending=[True, True]
        )

        st.write("**Products to review**")
        st.dataframe(
            priority[["Product", "Days Left", "Reorder Point",
                      "Suggested Order", "Status"]],
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Estimates assume daily sales stay constant. "
            "Use actual sales and supplier lead times for better decisions."
        )
    else:
        st.info("Enter daily sales above zero to generate demand insights.")
else:
    st.info("Add products to generate business insights.")
