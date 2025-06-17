import json
import pandas as pd

# Load data
with open("sample_documents.json", "r") as f:
    documents = json.load(f)

with open("ai_usage_logs.json", "r") as f:
    usage_logs = json.load(f)

# Convert to DataFrames
df_docs = pd.DataFrame(documents)
df_logs = pd.DataFrame(usage_logs)

# Merge AI usage into docs
df = pd.merge(df_docs, df_logs, left_on="doc_id", right_on="response_doc_id", how="left")

# Add a basic compliance checker
forbidden_keywords = ["leak", "top secret", "internal use only", "confidential", "fake", "ignore policy"]

def check_violations(text):
    found = [word for word in forbidden_keywords if word.lower() in text.lower()]
    return found

df["violations"] = df["content"].apply(check_violations)
df["violation_count"] = df["violations"].apply(len)

# Add risk score (simple rule-based)
def compute_risk(row):
    if row["author_type"] == "Human":
        return 0
    score = 50  # Base score for AI content
    score += row["violation_count"] * 25  # Each violation adds 25
    return min(score, 100)

df["risk_score"] = df.apply(compute_risk, axis=1)

# Rename columns for clarity
df.rename(columns={
    "author_type": "generated_by",
    "user_id": "ai_user_id",
    "timestamp_y": "ai_generated_at"
}, inplace=True)

# Select columns to export
report = df[[
    "doc_id",
    "generated_by",
    "ai_user_id",
    "ai_generated_at",
    "content",
    "violations",
    "risk_score"
]]

# Save report
report.to_csv("ai_audit_risk_report.csv", index=False)
print("Risk report saved as: ai_audit_risk_report.csv")
