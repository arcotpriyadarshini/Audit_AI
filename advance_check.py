import pandas as pd
import openai
import time

openai.api_key = "your-api-key-here"  # Replace with your key

# Load your AI audit report
df = pd.read_csv("ai_audit_risk_report.csv")

# Filter AI-generated documents only
ai_docs = df[df["generated_by"] == "AI"].copy()

# Add empty columns for new insights
ai_docs["tone_risk"] = ""
ai_docs["hallucination_risk"] = ""
ai_docs["flag_for_review"] = ""

# Prompt template
def audit_prompt(text):
    return f"""
You are an AI compliance auditor.

Given the following AI-generated content, do three things:
1. Classify the tone as one of: ["Neutral", "Formal", "Aggressive", "Emotional", "Sarcastic"]
2. Estimate the hallucination risk as one of: ["Low", "Medium", "High"]
3. Should this be flagged for human review? ("Yes" or "No")

Content:
{text}

Respond in this exact JSON format:
{{"tone": "...", "hallucination_risk": "...", "flag_for_review": "..."}}
"""

# Run through OpenAI
for i, row in ai_docs.iterrows():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
            messages=[
                {"role": "user", "content": audit_prompt(row["content"])}
            ]
        )
        content = response['choices'][0]['message']['content']
        result = eval(content)

        ai_docs.at[i, "tone_risk"] = result.get("tone", "")
        ai_docs.at[i, "hallucination_risk"] = result.get("hallucination_risk", "")
        ai_docs.at[i, "flag_for_review"] = result.get("flag_for_review", "")
        time.sleep(1.2)  # Respect rate limit

    except Exception as e:
        print(f"Error processing doc {row['doc_id']}: {e}")
        continue

# Save updated report
merged = pd.merge(df, ai_docs[["doc_id", "tone_risk", "hallucination_risk", "flag_for_review"]], on="doc_id", how="left")
merged.to_csv("ai_audit_risk_report_enhanced.csv", index=False)
print("Enhanced audit report saved: ai_audit_risk_report_enhanced.csv")
