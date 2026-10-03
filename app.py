import streamlit as st
from extractor import extract_text_from_pdf
from analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and paste a job description to see how well they match.")

uploaded_file = st.file_uploader("Upload resume (PDF)", type="pdf")
job_description = st.text_area("Paste the job description", height=200)

if st.button("Analyze"):
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)

        if result is None:
            st.error("Something went wrong. Please try again.")
        else:
            st.metric("Match score", f"{result['match_score']}/100")
            st.progress(result["match_score"] / 100)
            st.write(result["summary"])

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Skills matched")
                for item in result["skills_matched"]:
                    st.write(f"- {item}")
            with col2:
                st.subheader("❌ Skills missing")
                for item in result["skills_missing"]:
                    st.write(f"- {item}")

            st.subheader("📉 Experience gaps")
            for item in result["experience_gaps"]:
                st.write(f"- {item}")

            st.subheader("💡 Recommended improvements")
            for item in result["recommended_improvements"]:
                st.write(f"- {item}")