uploaded_file = st.sidebar.file_uploader("Upload a JSON or CSV file", type=["json", "csv"])

if uploaded_file:
    # Load uploaded file
    def load_uploaded_data(file):
        if file.name.endswith(".json"):
            raw = json.load(file)
            return pd.DataFrame(raw)
        else:
            return pd.read_csv(file)

    df_uploaded = load_uploaded_data(uploaded_file)

    # Display preview
    st.subheader(" Uploaded Document Preview")
    st.dataframe(df_uploaded.head(), use_container_width=True)

    #  Risk scoring logic goes *here*, inside the if-block:
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

    # Show risk results
    st.subheader("Risk Scored Documents")
    st.dataframe(df_uploaded[["doc_id", "author_type", "violations", "risk_score"]], use_container_width=True)
