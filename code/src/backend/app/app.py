import io
import os
import pandas as pd
from flask import Flask, request, jsonify
import sys

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import existing rule generator and validator
from models.rules_generate import generate_rules
from validation.validate_rules import validate

app = Flask(__name__)

# ✅ Define paths for saving processed data
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RULES_FILE_PATH = os.path.join(os.path.dirname(__file__), "../rules/generated_rules.json")
FLAGGED_TRANSACTIONS_PATH = os.path.join(UPLOAD_FOLDER, "flagged_transactions.csv")


@app.route("/process-data", methods=["POST"])
def process_data():
    """Process uploaded CSV, generate dynamic rules, validate transactions, and return flagged results."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file.seek(0, io.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size == 0:
        return jsonify({"error": "Uploaded file is empty"}), 400

    try:
        # ✅ Read CSV
        df = pd.read_csv(io.BytesIO(file.read()))

        if df.empty:
            return jsonify({"error": "Uploaded CSV contains no data"}), 400

        # ✅ Generate rules dynamically
        rules = generate_rules(df)  # ✅ Calling the existing `generate_rules()` function
        if not rules:
            return jsonify({"error": "Failed to generate rules"}), 500

        # ✅ Validate transactions based on generated rules
        flagged_transactions = validate(df, rules)  # ✅ Calling the existing `validate()` function

        # ✅ Save flagged transactions
        flagged_transactions.to_csv(FLAGGED_TRANSACTIONS_PATH, index=False)

        return jsonify({
            "message": "CSV processed successfully!",
            "rules": rules,
            "flagged_transactions": flagged_transactions.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": f"Failed to process CSV: {str(e)}"}), 500


@app.route("/flagged-transactions", methods=["GET"])
def get_flagged_transactions():
    """Return flagged transactions as JSON."""
    if not os.path.exists(FLAGGED_TRANSACTIONS_PATH):
        return jsonify({"error": "No flagged transactions available"}), 404

    df = pd.read_csv(FLAGGED_TRANSACTIONS_PATH)
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
