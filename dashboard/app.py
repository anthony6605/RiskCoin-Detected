import streamlit as st
import pandas as pd

st.title("📊 Stablecoin Risk Monitor")

df = pd.read_csv("data/processed/stablecoin_metrics.csv")

st.line_chart(df.pivot(index="timestamp", columns="coin", values="price"))
st.dataframe(df.tail(10))