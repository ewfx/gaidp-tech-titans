import pandas as pd
import json
import os

# ✅ Operator Mapping
OPERATOR_MAP = {
    "!=": lambda x, y: x != y,
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    "==": lambda x, y: x == y,
    "not in": lambda x, y: ~x.isin(y) if isinstance(y, list) else x != y,
    "in": lambda x, y: x.isin(y) if isinstance(y, list) else x == y
}

# Load rules dynamically
def load_rules():
    rules_path = os.path.join(os.path.dirname(__file__), "../rules/generated_rules.json")
    try:
        with open(rules_path, "r") as f:
            print(json.load(f))
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Rules file not found at {rules_path}")
        return {"rules": []}

# Dynamically apply rules
def validate(df,rules):
    # Load the original dataset
    flagged_transactions = []
    rules = rules.get("rules", [])
    for rule in rules:
        field = rule["field"]
        operator = rule["operator"]
        value = rule["value"]
    
        if operator not in OPERATOR_MAP:
            print(f"⚠️ Skipping unsupported operator: {operator}")
            # return pd.DataFrame()
            continue
        
        try:
            flagged = df[OPERATOR_MAP[operator](df[field], value)]
            flagged["Reason"] = rule["name"]
            flagged["Action"] = rule["action"]
            flagged_transactions.append(flagged)
        except Exception as e:
            print(f"❌ Error processing rule '{rule['name']}': {str(e)}")
            return pd.DataFrame()


    # ✅ Merge flagged transactions with the original dataset
    if flagged_transactions:
        flagged_df = pd.concat(flagged_transactions)

        # ✅ Keep all original transaction columns while grouping by Customer_ID
        flagged_df = df.merge(flagged_df[["Customer_ID", "Reason", "Action"]], on="Customer_ID", how="left")

        # ✅ Combine multiple reasons per transaction **with numbering if multiple**
        def format_messages(messages):
            unique_msgs = list(set(messages.dropna()))
            if len(unique_msgs) == 1:
                return unique_msgs[0]  # No numbering for a single message
            return "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(unique_msgs)])

        flagged_df["Reason"] = flagged_df.groupby("Customer_ID")["Reason"].transform(format_messages)
        flagged_df["Action"] = flagged_df.groupby("Customer_ID")["Action"].transform(format_messages)

        # ✅ Remove duplicates after merging
        flagged_df = flagged_df.drop_duplicates()

        # Save updated flagged transactions
        flagged_df.to_csv("../results/flagged_transactions.csv", index=False)
        print(f"\n✅ {len(flagged_df)} unique transactions flagged, retaining all details.")
        return flagged_df
    else:
        print("\n⚠️ No transactions were flagged.")
