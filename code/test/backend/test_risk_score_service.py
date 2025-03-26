import unittest
import pandas as pd
from src.backend.services.risk_score_service import compute_risk_score

class TestRiskScoreService(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = {
            "Transaction_Amount": [10000, 60000, 30000, 70000],
            "Account_Balance": [5000, -1000, 2000, -500],
            "Reported_Amount": [10000, 60000, 25000, 70000],
            "Country": ["USA", "North Korea", "Canada", "Iran"]
        }
        self.df = pd.DataFrame(self.data)

    def test_compute_risk_score(self):
        result_df = compute_risk_score(self.df)

        # Check if Risk_Score_Adjusted column is created
        self.assertIn("Risk_Score_Adjusted", result_df.columns)

        # Check if Risk_Score_Adjusted values are within the range 1 to 10
        self.assertTrue(result_df["Risk_Score_Adjusted"].between(1, 10).all())

        # Check specific adjustments
        self.assertEqual(result_df.loc[1, "Risk_Score_Adjusted"], result_df.loc[1, "Risk_Score"] + 9)  # Large transaction, negative balance, high-risk country
        self.assertEqual(result_df.loc[3, "Risk_Score_Adjusted"], result_df.loc[3, "Risk_Score"] + 7)  # Large transaction, high-risk country

    def test_missing_risk_score_column(self):
        df = self.df.drop(columns=["Risk_Score"], errors='ignore')
        result_df = compute_risk_score(df)
        self.assertIn("Risk_Score", result_df.columns)
        self.assertIn("Risk_Score_Adjusted", result_df.columns)

    def test_no_adjustments(self):
        df = pd.DataFrame({
            "Transaction_Amount": [1000, 2000],
            "Account_Balance": [1000, 2000],
            "Reported_Amount": [1000, 2000],
            "Country": ["USA", "Canada"]
        })
        result_df = compute_risk_score(df)
        self.assertTrue((result_df["Risk_Score"] == result_df["Risk_Score_Adjusted"]).all())

    def test_high_risk_country(self):
        df = pd.DataFrame({
            "Transaction_Amount": [1000],
            "Account_Balance": [1000],
            "Reported_Amount": [1000],
            "Country": ["Syria"]
        })
        result_df = compute_risk_score(df)
        self.assertEqual(result_df.loc[0, "Risk_Score_Adjusted"], result_df.loc[0, "Risk_Score"] + 4)

if __name__ == '__main__':
    unittest.main()
