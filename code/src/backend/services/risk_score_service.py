import numpy as np

def compute_risk_score(df):
    """Compute dynamic risk scores based on transaction patterns & anomalies."""
    
    # ✅ Base Risk Score (Use existing column or initialize)
    if "Risk_Score" not in df.columns:
        df["Risk_Score"] = np.random.randint(1, 10, size=len(df))  # Assign random risk scores if missing

    # ✅ Convert Risk Score to Float for Adjustments
    df["Risk_Score_Adjusted"] = df["Risk_Score"].astype(float)

    # 🚨 Increase Risk for Large Transactions
    df.loc[df["Transaction_Amount"] > 50000, "Risk_Score_Adjusted"] += 2

    # 🚨 Increase Risk for Negative Account Balances
    df.loc[df["Account_Balance"] < 0, "Risk_Score_Adjusted"] += 3

    # 🚨 Increase Risk for Mismatched Reported & Actual Amounts
    df.loc[df["Transaction_Amount"] != df["Reported_Amount"], "Risk_Score_Adjusted"] += 1.5

    # 🚨 Increase Risk for Transactions from High-Risk Countries
    high_risk_countries = ["North Korea", "Iran", "Syria"]
    df.loc[df["Country"].isin(high_risk_countries), "Risk_Score_Adjusted"] += 4

    # ✅ Normalize Scores Between 1 and 10
    df["Risk_Score_Adjusted"] = np.clip(df["Risk_Score_Adjusted"], 1, 10)

    return df
