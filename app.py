import html
import streamlit as st
from extractor import extract_text_from_pdf
from analyzer import analyze_resume

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("""
<style>
.hero {text-align:center; padding: 1rem 0 1.5rem 0;}
.hero h1 {font-size: 2.6rem; margin-bottom: 0.2rem;}
.hero p {color: #9aa4b2; font-size: 1.05rem;}
.card {background:#1A1F2B; border-radius:14px; padding:1.2rem 1.4rem; margin-bottom:1rem;}
.card h4 {margin-top:0;}
.score-ring {width:170px; height:170px; border-radius:50%;
    display:flex; align-items:center; justify-content:center; margin:0 auto;}
.score-inner {width:132px; height:132px; border-radius:50%; background:#1A1F2B;
    display:flex; flex-direction:column; align-items:center; justify-content:center;}
.score-num {font-size:2.5rem; font-weight:700; line-height:1;}
.score-label {color:#9aa4b2; font-size:0.8rem;}
.chip {display:inline-block; padding:6px 14px; margin:4px 6px 4px 0;
    border-radius:999px; font-size:0.9rem;}
.chip-green {background:rgba(34,197,94,0.15); color:#4ade80; border:1px solid rgba(34,197,94,0.4);}
.chip-red {background:rgba(239,68,68,0.15); color:#f87171; border:1px solid rgba(239,68,68,0.4);}
</style>
""", unsafe_allow_html=True)


def chips(items, css_class):
    if not items:
        return "<span style='color:#9aa4b2'>None</span>"
    return "".join(
        f'<span class="chip {css_class}">{html.escape(i)}</span>' for i in items
    )


def score_color(score):
    if score >= 75:
        return "#22c55e"
    if score >= 50:
        return "#f59e0b"
    return "#ef4444"


# ---------- Sidebar ----------
with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Upload your resume (PDF)\n"
        "2. Paste a job description\n"
        "3. Click **Analyze**\n"
        "4. Get score, skill gaps and improvements"
    )
    st.divider()
    st.caption("Built with Python, Streamlit and Gemini API")

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>📄 AI Resume Analyzer</h1>
        <p>See how well your resume matches a job, and how to improve it.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Inputs ----------
left, right = st.columns(2)
with left:
    uploaded_file = st.file_uploader("Upload resume (PDF)", type="pdf")
with right:
    job_description = st.text_area("Paste the job description", height=180)

analyze = st.button("🔍 Analyze", type="primary", use_container_width=True)

# ---------- Results ----------
if analyze:
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            result = analyze_resume(resume_text, job_description)

        if result is None:
            st.error("The AI service is busy right now. Please try again in a minute.")
        else:
            st.divider()
            score = result["match_score"]
            color = score_color(score)

            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(
                    f"""
                    <div class="card">
                      <div class="score-ring"
                           style="background: conic-gradient({color} {score}%, #2a3040 0);">
                        <div class="score-inner">
                          <span class="score-num" style="color:{color}">{score}</span>
                          <span class="score-label">out of 100</span>
                        </div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""
                    <div class="card">
                      <h4>Overall assessment</h4>
                      <p>{html.escape(result["summary"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            s1, s2 = st.columns(2)
            with s1:
                st.markdown(
                    f'<div class="card"><h4>✅ Skills matched</h4>'
                    f'{chips(result["skills_matched"], "chip-green")}</div>',
                    unsafe_allow_html=True,
                )
            with s2:
                st.markdown(
                    f'<div class="card"><h4>❌ Skills missing</h4>'
                    f'{chips(result["skills_missing"], "chip-red")}</div>',
                    unsafe_allow_html=True,
                )

            tab1, tab2 = st.tabs(["📉 Experience gaps", "💡 Recommended improvements"])
            with tab1:
                for item in result["experience_gaps"]:
                    st.markdown(f"- {item}")
            with tab2:
                for item in result["recommended_improvements"]:
                    st.markdown(f"- {item}")