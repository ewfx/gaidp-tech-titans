import pandas as pd
import json
from models.anomaly_detection import detect_anomalies
from validation.validate_rules import validate

def test_anomaly_detection():
    df = pd.DataFrame({"amount": [5000, 20000, 300, 15000]})
    df = detect_anomalies(df)
    assert "anomaly_score" in df.columns

def test_rule_validation():
    with open("../rules/generated_rules.json", "w") as f:
        json.dump({"threshold": 12000}, f, indent=4)
    
    df = pd.DataFrame({"amount": [5000, 20000, 300, 15000]})
    flagged = validate(df)
    assert flagged.shape[0] == 2  # 2 transactions > 12000 should be flagged
