import json
import pandas as pd

# Load sample documents
with open("sample_documents.json", "r") as f:
    documents = json.load(f)

# Define compliance rules
forbidden_keywords = ["leak", "top secret", "internal use only", "confidential", "fake", "ignore policy"]

# Convert to DataFrame and filter AI docs only
df = pd.DataFrame(documents)
df_ai = df[df["author_type"] == "AI"].copy()

# Initialize violation flags
def check_violations(text):
    violations = []
    for word in forbidden_keywords:
        if word.lower() in text.lower():
            violations.append(word)
    return violations

df_ai["violations"] = df_ai["content"].apply(check_violations)
df_ai["violation_flag"] = df_ai["violations"].apply(lambda x: len(x) > 0)

# Display flagged results
flagged = df_ai[df_ai["violation_flag"]]

if not flagged.empty:
    print("\n Compliance Violations Found:\n")
    print(flagged[["doc_id", "content", "violations"]].to_string(index=False))
else:
    print("\n No compliance violations detected.")
