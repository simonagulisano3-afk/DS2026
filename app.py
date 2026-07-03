import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Transactions Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Transactions Dashboard")
st.subheader("Page 1 - Time Analysis")

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

analysis_df["Year"] = analysis_df["Date"].dt.year
analysis_df["Quarter"] = analysis_df["Date"].dt.quarter
analysis_df["Month"] = analysis_df["Date"].dt.month

analysis_df = analysis_df.dropna(
    subset=["sector", "industry", "country", "region"]
)

# ------------------------
# FILTER
# ------------------------

start_date = st.sidebar.date_input(
    "Start date",
    value=pd.to_datetime("2024-01-01")
)

end_date = st.sidebar.date_input(
    "End date",
    value=pd.to_datetime("2024-12-31")
)

filtered = analysis_df[
    (analysis_df["Date"] >= pd.to_datetime(start_date))
    &
    (analysis_df["Date"] <= pd.to_datetime(end_date))
]

st.write(f"Number of transactions: {len(filtered)}")

# ------------------------
# GRAPH 1
# ------------------------

daily = (
    filtered
    .groupby(filtered["Date"].dt.date)
    .size()
    .reset_index(name="Transactions")
)

fig = px.line(
    daily,
    x="Date",
    y="Transactions",
    title="Transactions over Time"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# GRAPH 2
# ------------------------

top_symbols = (
    filtered
    .groupby("Symbol")
    .size()
    .sort_values(ascending=False)
    .head(3)
    .reset_index(name="Transactions")
)

fig = px.bar(
    top_symbols,
    x="Symbol",
    y="Transactions",
    title="Top 3 Traded Symbols"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# GRAPH 3
# ------------------------

top_sector = (
    filtered
    .groupby("sector")
    .size()
    .sort_values(ascending=False)
    .head(5)
    .reset_index(name="Transactions")
)

fig = px.bar(
    top_sector,
    x="sector",
    y="Transactions",
    title="Top 5 Sectors"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# GRAPH 4
# ------------------------

top_industry = (
    filtered
    .groupby("industry")
    .size()
    .sort_values(ascending=False)
    .head(5)
    .reset_index(name="Transactions")
)

fig = px.bar(
    top_industry,
    x="industry",
    y="Transactions",
    title="Top 5 Industries"
)

st.plotly_chart(fig, use_container_width=True)