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

# ✅ Display Flagged Transactions Using API Call
st.subheader("🚨 Flagged Transactions")
try:
    response = requests.get(f"{BACKEND_URL}/flagged-transactions")
    if response.status_code == 200:
        flagged_df = pd.DataFrame(response.json())
        if not flagged_df.empty:
            st.dataframe(flagged_df, use_container_width=True)
        else:
            st.warning("⚠️ No flagged transactions found.")
    else:
        st.error(f"⚠️ Failed to fetch flagged transactions: {response.json().get('error', 'Unknown error')}")
except Exception as e:
    st.error(f"❌ Error fetching flagged transactions: {str(e)}")