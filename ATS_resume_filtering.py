import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score


st.set_page_config(page_title="ATS Resume Screening System")
st.title("📄 ATS Resume Shortlisting System (Excel Path Based)")
st.write("Resumes are screened using skills extracted from the job dataset.")

job_dataset_path = "C:\Users\Lenovo\Downloads\JobsDatasetProcessed.xlsx"
job_df = pd.read_excel(job_dataset_path)

st.subheader("📄 Upload Resume Files")
uploaded_resumes = st.file_uploader("Upload multiple resumes (ALL file types allowed)",accept_multiple_files=True)

results = []
if uploaded_resumes:
    skills = []

    for col in ["IT Skills", "Soft Skills"]:
        if col in job_df.columns:
            job_df[col] = job_df[col].dropna().astype(str)
            for skill_list in job_df[col]:
                skills.extend(skill_list.lower().split(","))

    skills = list(set([s.strip() for s in skills]))

    st.subheader("🧠 Skills Used for ATS Matching")
    st.write(", ".join(skills))

    st.subheader("📊 ATS Screening Results")

    for resume in uploaded_resumes:
        text = resume.read().decode("utf-8").lower()

        matched_skills = [s for s in skills if s in text]
        match_score = len(matched_skills) / len(skills)

        shortlisted = 1 if match_score >= 0.4 else 0

        results.append({
            "Resume Name": resume.name,
            "Matched Skills": len(matched_skills),
            "Match Score": round(match_score, 2),
            "Shortlisted (1=Yes, 0=No)": shortlisted
        })

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    st.subheader("✅ Upload Ground Truth (Optional)")
    st.write("CSV format: resume_name, selected (1 or 0)")

    gt_file = st.file_uploader("Upload Ground Truth CSV", type="csv")

    if gt_file:
        gt_df = pd.read_csv(gt_file)

        merged = result_df.merge(
            gt_df,
            left_on="Resume Name",
            right_on="resume_name"
        )

        acc = accuracy_score(
            merged["selected"],
            merged["Shortlisted (1=Yes, 0=No)"]
        )

        st.success(f"🎯 ATS Accuracy: {acc * 100:.2f}%")

  
    st.subheader("📈 Resume Match Score Visualization")
    fig, ax = plt.subplots()
    ax.bar(result_df["Resume Name"], result_df["Match Score"])
    ax.axhline(0.4)
    ax.set_xlabel("Resumes")
    ax.set_ylabel("Match Score")
    ax.set_title("ATS Resume Match Scores")
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("Please upload resume files to start ATS screening.")
