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


# ✅ Generate Rules Using OpenRouter
def generate_rules(df, instructions_text):
    try:
        # Ensure "rules" folder exists
        rules_folder = os.path.join(os.path.dirname(__file__), "../rules")
        os.makedirs(rules_folder, exist_ok=True)

        # Define rules file path
        output_file = os.path.join(rules_folder, "generated_rules.json")

        # ✅ Dynamically Load Column Names from the Dataset
        VALID_FIELDS = df.columns.tolist()  # Extract column names dynamically
        # ✅ Improved AI Instructions
        formatted_instruction = (
            "Based on the following regulatory reporting instructions, generate financial compliance validation rules in JSON format.\n\n"
            f"Instructions:\n{instructions_text}\n\n"
            "Ensure each rule contains: 'name', 'condition', 'operator', 'value', 'field', and 'action'. "
            "The 'field' must be one of these valid column names from the dataset: "
            f"{', '.join(df.columns)}. "
            "Return only valid JSON output with no explanations."
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
            return generate_rules(df, instructions_text)  # Retry if AI fails

        # ✅ Convert `content` string into a valid JSON object
        try:
            rules_json = json.loads(rules_text)
        except json.JSONDecodeError:
            print("❌ AI output is not valid JSON. Retrying...")
            return generate_rules(df, instructions_text)  # Retry

        # ✅ Save Rules to File
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rules_json, f, indent=4)
        rule_count = len(rules_json.get("rules", []))  # Correctly count rules inside "rules" key
        print(f"✅ Rules successfully saved to {output_file}. Generated {rule_count} rules.")
        return rules_json

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {}

