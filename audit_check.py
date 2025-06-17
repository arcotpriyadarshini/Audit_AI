import streamlit as st
import pandas as pd
import json
import datetime

st.set_page_config(page_title="AI Audit Dashboard", layout="wide")
st.title("AI Audit Dashboard")

st.markdown("Track, audit, and assess AI-generated content for compliance.")

# ========== File Upload ========== #
st.sidebar.header("Upload New Documents")
uploaded_file = st.sidebar.file_uploader("Upload a JSON or CSV file", type=["json", "csv"])

@st.cache_data
def load_uploaded_data(file):
    if file.name.endswith(".json"):
        raw = json.load(file)
        return pd.DataFrame(raw)
    else:
        return pd.read_csv(file)

if uploaded_file:
    df_uploaded = load_uploaded_data(uploaded_file)
    st.sidebar.success("File uploaded successfully!")

    st.subheader("Uploaded Document Preview")
    st.dataframe(df_uploaded.head(), use_container_width=True)
else:
    st.info("Upload new AI documents to scan and display.")

    # === Basic Risk Scoring === #
    forbidden_keywords = ["leak", "top secret", "internal use only", "confidential", "fake", "ignore policy"]

    def check_violations(text):
        found = [w for w in forbidden_keywords if w.lower() in str(text).lower()]
        return found

    df_uploaded["violations"] = df_uploaded["content"].apply(check_violations)
    df_uploaded["violation_count"] = df_uploaded["violations"].apply(len)

    def compute_risk(row):
        score = 50 if row.get("author_type", "AI") == "AI" else 0
        score += row["violation_count"] * 25
        return min(score, 100)

    df_uploaded["risk_score"] = df_uploaded.apply(compute_risk, axis=1)

    st.subheader("Risk Scored Documents")
    st.dataframe(df_uploaded[["doc_id", "author_type", "violations", "risk_score"]], use_container_width=True)

