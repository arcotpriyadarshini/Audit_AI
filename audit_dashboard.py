import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load audit data
df = pd.read_csv("ai_audit_risk_report.csv")

# Sidebar filters
st.sidebar.title("Filters")
min_risk = st.sidebar.slider("Minimum Risk Score", 0, 100, 0)
author_filter = st.sidebar.selectbox("Show Content By", ["All", "AI Only", "Human Only"])

# Filter logic
filtered_df = df[df["risk_score"] >= min_risk]
if author_filter == "AI Only":
    filtered_df = filtered_df[filtered_df["generated_by"] == "AI"]
elif author_filter == "Human Only":
    filtered_df = filtered_df[filtered_df["generated_by"] == "Human"]

# Title
st.title("📋 AI Content Risk Audit Dashboard")

# Show total risk summary
avg_risk = filtered_df["risk_score"].mean()
st.metric("Average Risk Score", f"{avg_risk:.2f}")

# Show risk chart
st.subheader("Risk Scores by Document")
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(filtered_df["doc_id"], filtered_df["risk_score"], color="orange")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Show table
st.subheader("📄 Detailed Document Table")
st.dataframe(filtered_df[["doc_id", "generated_by", "ai_user_id", "risk_score", "violations"]])

# Export button
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered CSV", csv, "filtered_audit_report.csv", "text/csv")
# redeploy trigger
# redeploy trigger
