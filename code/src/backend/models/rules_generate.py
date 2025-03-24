import os
import json
import requests
import pandas as pd

# ✅ Load API Key
OR_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OR_API_KEY:
    raise ValueError("❌ OpenRouter API key not found. Set OPENROUTER_API_KEY as an environment variable.")

# ✅ Define OpenRouter API URL
OR_MODEL_URL = "https://openrouter.ai/api/v1/chat/completions"

# Ensure "rules" folder exists
rules_folder = os.path.join(os.path.dirname(__file__), "../rules")
os.makedirs(rules_folder, exist_ok=True)

# Define rules file path
output_file = os.path.join(rules_folder, "generated_rules.json")

# ✅ Dynamically Load Column Names from the Dataset
dataset_path = os.path.join(os.path.dirname(__file__), "../data/transactions.csv")
print(dataset_path)
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path, nrows=1)  # Load just 1 row to get column names
    VALID_FIELDS = df.columns.tolist()  # Extract column names dynamically
else:
    print("⚠️ Dataset not found. Using default column names.")
    VALID_FIELDS = ["Customer_ID", "Account_Balance", "Transaction_Amount",
                    "Reported_Amount", "Currency", "Country", "Transaction_Date", "Risk_Score"]

# ✅ Generate Rules Using OpenRouter
def generate_rules():
    try:
        # ✅ Improved AI Instructions
        formatted_instruction = (
            "Generate financial compliance validation rules in JSON format for banking transactions. "
            "Rules must follow fraud detection, money laundering prevention, and regulatory compliance. "
            "Ensure all rules have: 'name', 'condition' (Python-compatible format), 'operator', 'value', 'field', and 'action'. "
            "The 'field' must be one of these valid column names: "
            f"{', '.join(VALID_FIELDS)}. "
            "Ensure 'operator' is one of ['greaterThan', 'lessThan', 'greaterThanOrEqual', 'lessThanOrEqual', 'equal', 'notEqual']. "
            "Ensure 'value' contains a numeric threshold. "
            "Ensure the 'condition' field replaces 'value' with the actual numeric threshold. "
            "Return ONLY valid JSON output with no explanations."
        )

        headers = {
            "Authorization": f"Bearer {OR_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "anthropic/claude-3-haiku",
            "messages": [
                {"role": "system", "content": "You are a financial compliance AI that generates only valid JSON rules."},
                {"role": "user", "content": formatted_instruction}
            ],
            "temperature": 0.3
        }

        response = requests.post(OR_MODEL_URL, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"❌ OpenRouter API Error: {response.text}")
            return {}

        response_data = response.json()

        # ✅ Extract AI's generated text from the response
        choices = response_data.get("choices")
        if not choices or not isinstance(choices, list):
            print(f"❌ No valid 'choices' in response: {response_data}")
            return {}

        # ✅ Get the `content` field, which contains rules as a string
        rules_text = choices[0].get("message", {}).get("content", "").strip()
        if not rules_text:
            print("❌ No valid rules generated. Retrying...")
            return generate_rules()  # Retry if AI fails

        # ✅ Convert `content` string into a valid JSON object
        try:
            rules_json = json.loads(rules_text)
        except json.JSONDecodeError:
            print("❌ AI output is not valid JSON. Retrying...")
            return generate_rules()  # Retry

        # ✅ Validate & Fix `field` Names
        for rule in rules_json:
            if "field" not in rule or rule["field"] not in VALID_FIELDS:
                print(f"⚠️ Rule '{rule.get('name', 'Unknown')}' has an invalid 'field'. Assigning default field.")
                rule["field"] = "Transaction_Amount"  # Default fallback

            # ✅ Ensure "condition" replaces "value" with actual numeric threshold
            if "condition" in rule and "value" in rule:
                rule["condition"] = rule["condition"].replace("value", str(rule["value"]))

        # ✅ Save Rules to File
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"rules": rules_json}, f, indent=4)

        print(f"✅ Rules successfully saved to {output_file}. Generated {len(rules_json)} rules.")
        return rules_json

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {}

# Run rule generation
generate_rules()
