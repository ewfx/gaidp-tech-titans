import unittest
import pandas as pd
from src.backend.services.validate_rules_service import validate, load_rules

class TestValidateRulesService(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            "Customer_ID": [1, 2, 3, 4],
            "Amount": [100, 200, 300, 400],
            "Country": ["US", "UK", "US", "FR"]
        })
        self.rules = {
            "rules": [
                {"field": "Amount", "operator": ">", "value": 150, "name": "High Amount", "action": "Review"},
                {"field": "Country", "operator": "==", "value": "US", "name": "US Customer", "action": "Monitor"}
            ]
        }

    def test_validate(self):
        result = validate(self.df, self.rules)
        self.assertFalse(result.empty)
        self.assertIn("Reason", result.columns)
        self.assertIn("Action", result.columns)
        self.assertEqual(len(result), 4)

    def test_load_rules(self):
        rules = load_rules()
        self.assertIsInstance(rules, dict)
        self.assertIn("rules", rules)

if __name__ == "__main__":
    unittest.main()
