import unittest
from unittest.mock import patch
import pandas as pd
from src.frontend.utils import fetch_flagged_transactions

class TestFetchFlaggedTransactions(unittest.TestCase):

    @patch('src.frontend.utils.requests.get')
    def test_fetch_flagged_transactions_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "amount": 100, "flagged": True},
            {"id": 2, "amount": 200, "flagged": True}
        ]
        mock_get.return_value = mock_response

        result = fetch_flagged_transactions()
        expected = pd.DataFrame([
            {"id": 1, "amount": 100, "flagged": True},
            {"id": 2, "amount": 200, "flagged": True}
        ])
        pd.testing.assert_frame_equal(result, expected)

    @patch('src.frontend.utils.requests.get')
    def test_fetch_flagged_transactions_failure(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = fetch_flagged_transactions()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
