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

uploaded_instructions = st.sidebar.file_uploader("Upload Regulatory Instructions (TXT)", type=["txt"])
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    # ✅ Read Uploaded File
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File Uploaded Successfully")

    # ✅ Convert file to BytesIO for proper transmission
    file_bytes = io.BytesIO(uploaded_file.getvalue())
    instructions_bytes = io.BytesIO(uploaded_instructions.getvalue())

    # ✅ Send File to Backend for Processing
    st.info("🔄 Processing Uploaded Data...")
    response = requests.post(
        f"{BACKEND_URL}/process-data",
        files={"file": ("uploaded.csv", file_bytes, "text/csv"),
        "instructions": ("instructions.txt", instructions_bytes, "text/plain")}
    )

    
    if response.status_code == 200:
        st.session_state.data_processed = True  # ✅ Set flag to True after processing
        result = response.json()
        st.success("✅ Data Processed Successfully! Flagged transactions generated.")
        
        # ✅ Display Flagged Transactions
        st.subheader("🚨 Flagged Transactions")
        flagged_df = pd.DataFrame(result["flagged_transactions"])
        st.dataframe(flagged_df, use_container_width=True)

        # ✅ Display Generated Rules
        st.subheader("📜 Generated Compliance Rules")
        st.json(result["rules"], expanded=False)

        # ✅ Display Anomaly Detection Results
        st.subheader("⚠️ Anomalies Detected")
        anomalies_df = pd.DataFrame(result["anomalies"])
        st.dataframe(anomalies_df, use_container_width=True)

        # ✅ Display Risk Scores
        st.subheader("📊 Risk Scores")
        risk_scores_df = pd.DataFrame(result["risk_scores"])
        st.dataframe(risk_scores_df, use_container_width=True)
    else:
        st.error(f"⚠️ Failed to process data: {response.json().get('error', 'Unknown error')}")
if not st.session_state.data_processed:
    st.warning("📂 Upload a dataset and process it to see flagged transactions.")
