import io
import os
import pandas as pd
from flask import Flask, request, jsonify
import sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import existing rule generator and validator
from services.risk_score_service import compute_risk_score
from services.rules_generate_service import generate_rules
from services.validate_rules_service import validate
from services.anomaly_detection_service import detect_anomalies

app = Flask(__name__)

# ✅ Define paths for saving processed data
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RULES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../rules/generated_rules.json")
FLAGGED_TRANSACTIONS_PATH = os.path.join(UPLOAD_FOLDER, "flagged_transactions.csv")


@app.route("/process-data", methods=["POST"])
def process_data():
    """Process uploaded dataset & regulatory reporting instructions."""
    
    if "file" not in request.files or "instructions" not in request.files:
        return jsonify({"error": "Both dataset and regulatory instructions are required"}), 400

    file = request.files["file"]
    instructions_file = request.files["instructions"]

    file.seek(0, io.SEEK_END)
    instructions_file.seek(0, io.SEEK_END)
    file_size = file.tell()
    instructions_size = instructions_file.tell()
    file.seek(0)
    instructions_file.seek(0)

    if file_size == 0 or instructions_size == 0:
        return jsonify({"error": "One of the uploaded files is empty"}), 400

    try:
        # ✅ Read dataset
        df = pd.read_csv(io.BytesIO(file.read()))

        # ✅ Read regulatory reporting instructions
        instructions_text = instructions_file.read().decode("utf-8")
        if df.empty or not instructions_text.strip():
            return jsonify({"error": "Uploaded data or instructions are empty"}), 400

        # ✅ Generate rules dynamically based on instructions
        rules = generate_rules(df, instructions_text)  # Pass instructions for better rule generation
        if not rules:
            return jsonify({"error": "Failed to generate rules"}), 500

        # ✅ Validate transactions based on generated rules
        flagged_transactions = validate(df, rules)

        # ✅ Perform anomaly detection
        anomalies = detect_anomalies(df)

        # ✅ Compute dynamic risk scores
        df = compute_risk_score(df)

        # ✅ Save flagged transactions
        # flagged_transactions.to_csv(FLAGGED_TRANSACTIONS_PATH, index=False)

        return jsonify({
            "message": "Processing completed!",
            "rules": rules,
            "anomalies": anomalies.to_dict(orient="records"),
            "risk_scores": df[["Customer_ID", "Risk_Score_Adjusted"]].to_dict(orient="records"),
            "flagged_transactions": flagged_transactions.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": f"Failed to process data: {str(e)}"}), 500



@app.route("/flagged-transactions", methods=["GET"])
def get_flagged_transactions():
    """Return flagged transactions as JSON."""
    if not os.path.exists(FLAGGED_TRANSACTIONS_PATH):
        return jsonify({"error": "No flagged transactions available"}), 404

    df = pd.read_csv(FLAGGED_TRANSACTIONS_PATH)
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
