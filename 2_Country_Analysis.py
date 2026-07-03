import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Country Analysis")

# ------------------------
# LOAD DATA
# ------------------------

country = pd.read_csv("Datasets/country.csv")

symbols = pd.read_csv(
    "Datasets/symbols.csv",
    sep=";"
)

transactions = pd.read_csv(
    "Datasets/account-statement-1-1-2024-12-31-2024.csv",
    sep=";"
)

transactions = transactions.drop(columns=["Unnamed: 5"], errors="ignore")
transactions = transactions.dropna(how="all")

transactions["Date"] = pd.to_datetime(
    transactions["Date"],
    dayfirst=True
)

symbols["country"] = symbols["country"].replace({
    "Turkey": "Türkiye",
    "Taiwan": "Taiwan, Province of China"
})

analysis_df = transactions.merge(
    symbols,
    left_on="Symbol",
    right_on="symbol",
    how="left"
)

analysis_df = analysis_df.merge(
    country,
    left_on="country",
    right_on="name",
    how="left"
)

analysis_df = analysis_df.dropna(
    subset=["sector", "industry", "country", "region"]
)

# ------------------------
# COUNTRY SELECTOR
# ------------------------
selected_country = st.selectbox(
    "Select Country",
    sorted(analysis_df["country"].unique())
)

filtered = analysis_df[
    analysis_df["country"] == selected_country
]

if filtered.empty:
    st.warning("No transactions found for this country.")
    st.stop()

# ------------------------
# LINE CHART
# ------------------------

daily = (
    filtered.groupby(filtered["Date"].dt.date)
    .size()
    .reset_index(name="Transactions")
)

fig = px.line(
    daily,
    x="Date",
    y="Transactions",
    title=f"Transactions in {selected_country}"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# BUY
# ------------------------

buy = (
    filtered[filtered["TransactionType"] == "BUY"]
    .groupby("industry")
    .size()
    .sort_values(ascending=False)
    .head(5)
    .reset_index(name="Transactions")
)

fig = px.bar(
    buy,
    x="industry",
    y="Transactions",
    title="Top 5 BUY Industries"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# SELL
# ------------------------

sell = (
    filtered[filtered["TransactionType"] == "SELL"]
    .groupby("industry")
    .size()
    .sort_values(ascending=False)
    .head(5)
    .reset_index(name="Transactions")
)

fig = px.bar(
    sell,
    x="industry",
    y="Transactions",
    title="Top 5 SELL Industries"
)

st.plotly_chart(fig, use_container_width=True)
