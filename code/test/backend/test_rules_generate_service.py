import os
import json
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.backend.services.rules_generate_service import generate_rules

class TestGenerateRules(unittest.TestCase):

    @patch("src.backend.services.rules_generate_service.requests.post")
    def test_generate_rules_success(self, mock_post):
        # Mock environment variable
        os.environ["OPENROUTER_API_KEY"] = "test_api_key"

        # Mock DataFrame
        data = {
            "column1": [1, 2, 3],
            "column2": [4, 5, 6]
        }
        df = pd.DataFrame(data)

        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "rules": [
                                {"name": "Rule 1", "condition": "condition1", "operator": "==", "value": "value1", "field": "column1", "action": "action1"}
                            ]
                        })
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        # Call the function
        rules = generate_rules(df, "Test instructions")

        # Assertions
        self.assertIn("rules", rules)
        self.assertEqual(len(rules["rules"]), 1)
        self.assertEqual(rules["rules"][0]["name"], "Rule 1")

    @patch("src.backend.services.rules_generate_service.requests.post")
    def test_generate_rules_api_error(self, mock_post):
        # Mock environment variable
        os.environ["OPENROUTER_API_KEY"] = "test_api_key"

        # Mock DataFrame
        data = {
            "column1": [1, 2, 3],
            "column2": [4, 5, 6]
        }
        df = pd.DataFrame(data)

        # Mock API response with error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        # Call the function
        rules = generate_rules(df, "Test instructions")

        # Assertions
        self.assertEqual(rules, {})

    @patch("src.backend.services.rules_generate_service.requests.post")
    def test_generate_rules_invalid_json(self, mock_post):
        # Mock environment variable
        os.environ["OPENROUTER_API_KEY"] = "test_api_key"

        # Mock DataFrame
        data = {
            "column1": [1, 2, 3],
            "column2": [4, 5, 6]
        }
        df = pd.DataFrame(data)

        # Mock API response with invalid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Invalid JSON"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        # Call the function
        rules = generate_rules(df, "Test instructions")

        # Assertions
        self.assertEqual(rules, {})

if __name__ == "__main__":
    unittest.main()
