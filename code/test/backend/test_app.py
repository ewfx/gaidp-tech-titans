import io
import os
import unittest
from unittest.mock import patch
from flask import jsonify
from app.app import app, FLAGGED_TRANSACTIONS_PATH

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("app.app.generate_rules")
    @patch("app.app.validate")
    @patch("app.app.detect_anomalies")
    @patch("app.app.compute_risk_score")
    def test_process_data(self, mock_compute_risk_score, mock_detect_anomalies, mock_validate, mock_generate_rules):
        mock_generate_rules.return_value = [{"rule": "example_rule"}]
        mock_validate.return_value = pd.DataFrame([{"Transaction_ID": 1, "Flagged": True}])
        mock_detect_anomalies.return_value = pd.DataFrame([{"Transaction_ID": 1, "Anomaly": True}])
        mock_compute_risk_score.return_value = pd.DataFrame([{"Customer_ID": 1, "Risk_Score_Adjusted": 0.5}])

        data = {
            "file": (io.BytesIO(b"Customer_ID,Transaction_Amount\n1,100"), "test.csv"),
            "instructions": (io.BytesIO(b"Example instructions"), "instructions.txt")
        }
        response = self.app.post("/process-data", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Processing completed!", response.json["message"])

    def test_get_flagged_transactions_no_file(self):
        if os.path.exists(FLAGGED_TRANSACTIONS_PATH):
            os.remove(FLAGGED_TRANSACTIONS_PATH)
        response = self.app.get("/flagged-transactions")
        self.assertEqual(response.status_code, 404)
        self.assertIn("No flagged transactions available", response.json["error"])

    @patch("pandas.read_csv")
    def test_get_flagged_transactions_with_file(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame([{"Transaction_ID": 1, "Flagged": True}])
        with open(FLAGGED_TRANSACTIONS_PATH, "w") as f:
            f.write("Transaction_ID,Flagged\n1,True\n")
        response = self.app.get("/flagged-transactions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["Transaction_ID"], 1)

if __name__ == "__main__":
    unittest.main()
