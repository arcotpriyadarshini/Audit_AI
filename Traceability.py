import json
import pandas as pd

# Load documents
with open("sample_documents.json", "r") as f:
    documents = json.load(f)

# Load AI usage logs
with open("ai_usage_logs.json", "r") as f:
    usage_logs = json.load(f)

# Convert to DataFrames
df_docs = pd.DataFrame(documents)
df_logs = pd.DataFrame(usage_logs)

# Filter only AI-generated documents
df_ai_docs = df_docs[df_docs["author_type"] == "AI"]

# Merge logs with documents based on doc_id
merged = pd.merge(df_ai_docs, df_logs, left_on="doc_id", right_on="response_doc_id", how="left")

# Use correct column names
trace_df = merged[["doc_id", "user_id", "prompt_y", "timestamp_y", "content"]]
trace_df.rename(columns={
    "prompt_y": "prompt",
    "timestamp_y": "prompt_timestamp"
}, inplace=True)

# Display traceability report
print("\n📄 AI Traceability Report:")
print(trace_df.to_string(index=False))

