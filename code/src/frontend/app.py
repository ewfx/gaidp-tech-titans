import streamlit as st
import pandas as pd
import requests
import io

# ✅ Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

# ✅ Streamlit Page Configuration
st.set_page_config(page_title="Regulatory Profiler", page_icon="📊", layout="wide")

st.markdown("## 🚀 Regulatory Data Profiler")
st.sidebar.header("📂 Upload Transaction Data")

# ✅ Session State to Track Processed Data
if "data_processed" not in st.session_state:
    st.session_state.data_processed = False  # Initially False

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
        files={"file": ("uploaded.csv", file_bytes, "text/csv")}
    )

    if response.status_code == 200:
        st.session_state.data_processed = True  # ✅ Set flag to True after processing
        st.success("✅ Data Processed Successfully! Flagged transactions generated.")
    else:
        st.error(f"⚠️ Failed to process data: {response.json().get('error', 'Unknown error')}")

# ✅ Display Flagged Transactions ONLY After Processing New Data
if st.session_state.data_processed:
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
else:
    st.warning("📂 Upload a dataset and process it to see flagged transactions.")
