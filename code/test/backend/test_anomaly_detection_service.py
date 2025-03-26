import unittest
import pandas as pd
from src.backend.services.anomaly_detection_service import detect_anomalies

class TestAnomalyDetectionService(unittest.TestCase):

    def setUp(self):
        # Create a sample dataframe for testing
        data = {
            'feature1': [1, 2, 3, 4, 1000],
            'feature2': [10, 20, 30, 40, 1000]
        }
        self.df = pd.DataFrame(data)

    def test_detect_anomalies(self):
        # Test the detect_anomalies function
        result_df = detect_anomalies(self.df)
        self.assertIn('anomaly_score', result_df.columns)
        self.assertEqual(len(result_df), len(self.df))
        self.assertTrue(result_df['anomaly_score'].isin([-1, 1]).all())

if __name__ == '__main__':
    unittest.main()
