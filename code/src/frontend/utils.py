import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:5000"  # Adjust if needed

def fetch_flagged_transactions():
    """Fetch flagged transactions from backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/flagged-transactions")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        st.error("⚠️ Failed to load flagged transactions.")
    except Exception as e:
        st.error(f"🚨 Error: {e}")
    return None
