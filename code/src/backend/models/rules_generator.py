import openai

# Set up your OpenAI API key
OPENAI_API_KEY = "api-key"

def generate_rules(prompt, model="gpt-4", max_rules=5):
    """Generate business rules based on a given prompt."""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI that generates business rules."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        rules = response["choices"][0]["message"]["content"]
        return rules

    except Exception as e:
        return f"Error generating rules: {str(e)}"

# Example usage
prompt = "Generate banking rules for bank."
rules = generate_rules(prompt)

print("Generated Rules:\n", rules)
