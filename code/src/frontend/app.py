import streamlit as st
import pandas as pd
import requests
import os
import io

BACKEND_URL = "http://127.0.0.1:5000"  # Ensure backend is running

st.set_page_config(page_title="Regulatory Profiler", page_icon="📊", layout="wide")

st.markdown("## 🚀 Regulatory Data Profiler")
st.sidebar.header("📂 Upload Transaction Data")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    # ✅ Read Uploaded File
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File Uploaded Successfully")

    # ✅ Convert file to BytesIO for proper transmission
    file_bytes = io.BytesIO(uploaded_file.getvalue())

    # ✅ Send File to Backend for Processing
    st.info("🔄 Processing Uploaded Data...")
    response = requests.post(
        f"{BACKEND_URL}/process-data",
        files={"file": ("uploaded.csv", file_bytes, "text/csv")}  # Correct format
    )

# ✅ Display Flagged Transactions
st.subheader("🚨 Flagged Transactions")
try:
    flagged_df = pd.read_csv("../data/flagged_transactions.csv")
    st.dataframe(flagged_df, use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ No flagged transactions found. Upload and process a dataset first.")
