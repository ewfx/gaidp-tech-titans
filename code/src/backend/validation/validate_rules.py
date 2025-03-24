import pandas as pd
import json
import os

# Load the original dataset
csv_path = os.path.join(os.path.dirname(__file__), "../data/transactions.csv")
regulatory_df = pd.read_csv(csv_path)

# Load rules dynamically
def load_rules():
    rules_path = os.path.join(os.path.dirname(__file__), "../rules/generated_rules.json")
    try:
        with open(rules_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Rules file not found at {rules_path}")
        return {"rules": []}

# Dynamically apply rules
def validate(data):
    rules = load_rules().get("rules", [])
    flagged_transactions = []

    for rule in rules:
        field = rule.get("field")
        operator = rule.get("operator")
        threshold = rule.get("value")  
        reason = rule.get("name")  # ✅ Use 'name' as the reason
        action = rule.get("action")  # ✅ Use 'action' from rules

        if not operator or threshold is None:
            print(f"⚠️ Rule '{reason}' skipped due to missing operator or value.")
            continue

        # ✅ Ensure field is numeric before applying conditions
        if data[field].dtype == "object" and operator not in ["equal", "notEqual"]:
            data[field] = pd.to_numeric(data[field], errors="coerce")

        # ✅ Apply rule based on operator
        if isinstance(threshold, list):  
            flagged = data[data[field].isin(threshold)]  # ✅ Use `.isin()` for lists  
        elif operator == "greaterThan":
            flagged = data[data[field] > threshold]
        elif operator == "lessThan":
            flagged = data[data[field] < threshold]
        elif operator == "greaterThanOrEqual":
            flagged = data[data[field] >= threshold]
        elif operator == "lessThanOrEqual":
            flagged = data[data[field] <= threshold]
        elif operator == "equal":
            flagged = data[data[field] == threshold]
        elif operator == "notEqual":
            flagged = data[data[field] != threshold]
        else:
            print(f"⚠️ Skipping unsupported operator: {operator}")
            continue

        if not flagged.empty:
            flagged = flagged.copy()  # ✅ Prevents `SettingWithCopyWarning`
            flagged["Reason"] = reason
            flagged["Action"] = action  # ✅ Store action for flagged transactions
            flagged_transactions.append(flagged)

    # ✅ Merge flagged transactions with the original dataset
    if flagged_transactions:
        flagged_df = pd.concat(flagged_transactions)

        # ✅ Keep all original transaction columns while grouping by Customer_ID
        flagged_df = regulatory_df.merge(flagged_df[["Customer_ID", "Reason", "Action"]], on="Customer_ID", how="left")

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
    else:
        print("\n⚠️ No transactions were flagged.")

# Load dataset dynamically
df = pd.read_csv(csv_path)

# Run validation
validate(df)
