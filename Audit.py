import json
from datetime import datetime, timedelta
import random

# Sample prompts for AI-generated docs
ai_prompts = [
    "Write a short financial update email about quarterly revenue increase.",
    "Summarize cost-saving measures for the quarterly financial report.",
    "Generate an internal memo reminding staff to submit expense reports.",
    "Create a client-facing email about product updates and improvements."
]

# Human-written sample texts
human_texts = [
    "Please make sure to submit all expense reports by the end of the week.",
    "Looking forward to our team meeting next Tuesday to discuss the new project.",
    "Remember to review the budget forecast before Friday.",
    "Thanks for your hard work on the recent product launch."
]

# Function to generate AI-generated content (simulate)
def generate_ai_content(prompt):
    # For demo, just return prompt + " (AI generated content)"
    return f"{prompt} (AI generated content)"

# Generate sample documents
def generate_documents(num_docs=10):
    documents = []
    usage_logs = []
    base_time = datetime.now()

    for i in range(num_docs):
        is_ai = random.choice([True, False])
        doc_id = f"doc_{i+1:03d}"
        timestamp = (base_time + timedelta(minutes=i*10)).isoformat()

        if is_ai:
            prompt = random.choice(ai_prompts)
            content = generate_ai_content(prompt)
            author_type = "AI"

            # Log AI usage
            usage_logs.append({
                "user_id": f"user_{random.randint(1,5)}",
                "prompt": prompt,
                "response_doc_id": doc_id,
                "timestamp": timestamp
            })

        else:
            prompt = None
            content = random.choice(human_texts)
            author_type = "Human"

        doc = {
            "doc_id": doc_id,
            "author_type": author_type,
            "content": content,
            "timestamp": timestamp,
            "prompt": prompt
        }
        documents.append(doc)

    return documents, usage_logs

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    docs, logs = generate_documents(20)
    save_json(docs, "sample_documents.json")
    save_json(logs, "ai_usage_logs.json")
    print("Sample data generated: sample_documents.json, ai_usage_logs.json")

