# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Expenses Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/all_expenses.csv")

df = load_data()

# --- Build a combined month_year label to select from ---
df["month_year"] = df["source_month"] + " " + df["source_year"].astype(str)

st.title("Monthly Expenses Dashboard")

month_years = sorted(
    df["month_year"].unique(),
    key=lambda my: (int(my.split()[1]), 
                     pd.to_datetime(my.split()[0], format="%b").month)
)
selected = st.selectbox("Select Month", month_years)

month_df = df[df["month_year"] == selected]

def prepare_chart_data(month_df: pd.DataFrame) -> pd.DataFrame:
    debit = (
        month_df[month_df["transaction_type"] == "Debit"]
        .groupby("category")["Debit Amount"]
        .sum()
        .reset_index()
        .rename(columns={"Debit Amount": "amount"})
    )
    debit["bar_type"] = "Debit"

    credit_total = month_df.loc[month_df["transaction_type"] == "Credit", "Credit Amount"].sum()
    credit = pd.DataFrame({
        "category": ["Credit"],
        "amount": [credit_total],
        "bar_type": ["Credit"],
    })

    debit_total = month_df.loc[month_df["transaction_type"] == "Debit", "Debit Amount"].sum()
    total_debit = pd.DataFrame({
        "category": ["Total Debit"],
        "amount": [debit_total],
        "bar_type": ["Total Debit"],
    })
    chart_data = pd.concat([debit, credit, total_debit], ignore_index=True)
    category_order = list(debit["category"]) + ["Credit", "Total Debit"]

    return chart_data, category_order

chart_data, category_order = prepare_chart_data(month_df)

fig = px.bar(
    chart_data,
    x="category",
    y="amount",
    color="bar_type",
    color_discrete_map={"Debit": "blue", "Credit": "green", "Total Debit": "purple"},
    category_orders={"category": category_order},
    labels={"amount": "Amount ($)", "category": "Category"},
    title=f"Expenses — {selected}",
)

st.plotly_chart(fig, use_container_width=True)