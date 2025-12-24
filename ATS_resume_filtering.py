import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="ATS Resume Screening", layout="centered")

# -------------------------------
# 🌌 NIGHT SKY BACKGROUND + STARS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #050514, #0b1030, #000000);
    color: white;
}
.block-container {
    background-color: rgba(10, 15, 40, 0.92);
    padding: 2.5rem;
    border-radius: 18px;
}
@keyframes twinkle {
    0% { opacity: 0.3; }
    50% { opacity: 0.9; }
    100% { opacity: 0.3; }
}
.star {
    position: fixed;
    width: 2px;
    height: 2px;
    background: white;
    border-radius: 50%;
    animation: twinkle 4s infinite ease-in-out;
}
.star:nth-child(1) { top: 12%; left: 18%; }
.star:nth-child(2) { top: 28%; left: 72%; animation-delay: 1s; }
.star:nth-child(3) { top: 48%; left: 45%; animation-delay: 2s; }
.star:nth-child(4) { top: 75%; left: 82%; animation-delay: 3s; }
.star:nth-child(5) { top: 62%; left: 14%; animation-delay: 1.5s; }
</style>

<div class="star"></div><div class="star"></div><div class="star"></div>
<div class="star"></div><div class="star"></div>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.markdown("<h1 style='text-align:center;'>🌟 ATS Resume Screening System 🌟</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Top 5 Resume Accuracy </h3>", unsafe_allow_html=True)

# -------------------------------
# LOAD EXCEL DATASET
# -------------------------------
job_dataset_path = r"C:\Users\Lenovo\Downloads\JobsDatasetProcessed.xlsx"
job_df = pd.read_excel(job_dataset_path)

# -------------------------------
# FILTER 10 DATA ANALYST ROLES
# -------------------------------
job_df["Job Title"] = job_df["Job Title"].astype(str)

analyst_roles = [
    title for title in job_df["Job Title"].unique()
    if "data analyst" in title.lower()
][:10]

# -------------------------------
# JOB ROLE SELECTION
# -------------------------------
st.subheader("🧑‍💼 Select Job Role")
selected_role = st.radio("Choose one role", analyst_roles)

# -------------------------------
# UPLOAD RESUMES
# -------------------------------
st.subheader("📂 Upload Resumes")
uploaded_resumes = st.file_uploader(
    "Upload resumes (any file type, multiple allowed)",
    accept_multiple_files=True
)

# -------------------------------
# SUBMIT BUTTON
# -------------------------------
submit = st.button("🚀 Submit for ATS Evaluation")

# -------------------------------
# SAFE TEXT EXTRACTION
# -------------------------------
def extract_text_safe(file):
    try:
        return file.read().decode("utf-8", errors="ignore").lower()
    except:
        return ""

# -------------------------------
# AFTER SUBMIT
# -------------------------------
if submit:

    if not uploaded_resumes:
        st.error("❌ Please upload at least one resume.")
        st.stop()

    # Extract skills for selected role
    role_df = job_df[job_df["Job Title"] == selected_role]

    skills = []
    for col in ["IT Skills", "Soft Skills"]:
        if col in role_df.columns:
            role_df[col] = role_df[col].fillna("")
            for val in role_df[col]:
                skills.extend(val.lower().split(","))

    skills = list(set([s.strip() for s in skills if s.strip()]))

    # -------------------------------
    # SCORE EACH RESUME
    # -------------------------------
    resume_scores = []

    for resume in uploaded_resumes:
        text = extract_text_safe(resume)
        score = sum(1 for s in skills if s in text) / len(skills) if skills else 0

        resume_scores.append({
            "Resume File": resume.name,
            "Accuracy (%)": round(score * 100, 2)
        })

    # -------------------------------
    # TOP 10 ONLY
    # -------------------------------
    top10 = sorted(resume_scores, key=lambda x: x["Accuracy (%)"], reverse=True)[:10]

    # -------------------------------
    # DISPLAY EACH SEPARATELY
    # -------------------------------
    st.subheader("📋 Top 5 Resume Accuracy")

    for i, r in enumerate(top10, start=1):
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 15px;
                margin-bottom: 12px;
                box-shadow: 0 0 15px rgba(0,255,255,0.25);
            ">
                <b>Rank {i}</b><br>
                📄 {r['Resume File']}<br>
                🎯 Accuracy: <span style="color:#00fff0;">{r['Accuracy (%)']}%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------
    # BAR CHART (TOP 10)
    # -------------------------------
    st.subheader("📈 Top 10 Resume Match Scores")

    scores = [r["Accuracy (%)"] / 100 for r in top10]

    fig, ax = plt.subplots()
    ax.bar(range(1, len(scores) + 1), scores)
    ax.set_xlabel("Top Ranked Resumes")
    ax.set_ylabel("Match Score")
    ax.set_title(f"Top 10 ATS Rankers – {selected_role}")

    st.pyplot(fig)





