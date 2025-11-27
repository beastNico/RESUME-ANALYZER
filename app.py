from __future__ import annotations
import os
import tempfile
from typing import Any, Dict
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

from jamaibase import JamAI, types as t

# Configuration
PROJECT_ID = "proj_8cf411be8a957d4e10762d59"
PAT = "jamai_pat_c1373fd30208e46d1cef780b6878e4a0172784ab514621a5"
TABLE_ID = "Resume_Analyzer"
RESUME_COL = "resume"
JOB_DESC_COL = "job_description"

OUT_COLUMNS = [
    "fit_score",
    "question_gen",
    "summary",
    "profile",
    "summary_malay",
]

# Session state initialization
if "results" not in st.session_state:
    st.session_state.results = None

if "history" not in st.session_state:
    st.session_state.history = []

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    .reset-button {
        display: flex;
        justify-content: flex-end;
        margin: 1.5rem 0;
    }
    .stButton>button[kind="primary"] {
        background-color: #1E88E5 !important;
        border-color: #1E88E5 !important;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #1565C0 !important;
        border-color: #1565C0 !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .fit-score-container {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    .fit-score {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    .section-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
    }
    div[data-testid="stExpander"] {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def get_client() -> JamAI:
    return JamAI(project_id=PROJECT_ID, token=PAT)

client = get_client()

def _upload_file(client: JamAI, uploaded_file) -> str | None:
    if not uploaded_file:
        return None
    suffix = os.path.splitext(uploaded_file.name)[1] or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        resp = client.file.upload_file(tmp_path)
        return getattr(resp, "uri", None)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

def _safe_text(cell: Any) -> str:
    try:
        return getattr(cell, "text", "") or ""
    except Exception:
        return ""

def run_resume_analyzer(client: JamAI, resume_uri: str, job_desc: str) -> Dict[str, str]:
    req = t.MultiRowAddRequest(
        table_id=TABLE_ID,
        data=[{RESUME_COL: resume_uri, JOB_DESC_COL: job_desc}],
        stream=False,
    )
    res = client.table.add_table_rows(t.TableType.ACTION, req)
    row0 = res.rows[0]
    results = {}
    for col in OUT_COLUMNS:
        results[col] = _safe_text(row0.columns.get(col))
    return results

st.markdown("""
<div class="main-header">
    <h1>📄 HR Assist</h1>
    <p>🎯 Smart Job Description Matching & Intelligent Resume Scoring</p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([6, 1])
with col_right:
    translate_enabled = st.toggle("🌐 English ⇄ Malay", value=False, key='translate_toggle')

with st.sidebar:
    st.markdown("### 📜 Analysis History")
    st.markdown("---")
    
    if not st.session_state.history:
        st.info("📭 No resumes analyzed yet. Start by uploading a resume!")
    else:
        st.success(f"✅ **{len(st.session_state.history)}** resume(s) analyzed")
        st.markdown("---")
        
        for idx, item in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"🔍 **{item['filename'][:30]}{'...' if len(item['filename']) > 30 else ''}**"):
                st.markdown(f"**⭐ Fit Score:** `{item['fit_score']}`")
                st.markdown(f"**👤 Profile:**")
                st.write(item["profile"])

st.markdown('<div class="reset-button">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    if st.button("🔄 Analyze New Resume", type="primary", use_container_width=True):
        st.session_state.results = None
        st.session_state.reset_counter += 1
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 📥 Upload & Configure")
left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### 📤 Resume Upload")
    resume_file = st.file_uploader(
        "Select candidate's resume file",
        type=["doc", "docx", "pdf"],
        key=f"resume_file_{st.session_state.reset_counter}",
        help="Supported formats: DOC, DOCX, PDF"
    )
    if resume_file:
        st.success(f"✅ File loaded: **{resume_file.name}**")

with right:
    st.markdown("#### 📄 Job Description")
    job_desc = st.text_area(
        "Paste the job description here",
        key=f"jd_{st.session_state.reset_counter}",
        height=200,
        placeholder="Enter the complete job description including requirements, responsibilities, and qualifications...",
        help="Provide detailed job description for better analysis"
    )

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    analyze_button = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

if analyze_button:
    if not resume_file or not job_desc.strip():
        st.error("⚠️ Please upload a resume **AND** enter the job description to proceed.")
    else:
        with st.spinner("🔍 Analyzing resume... Please wait..."):
            try:
                resume_uri = _upload_file(client, resume_file)
                results = run_resume_analyzer(client, resume_uri, job_desc)
                results["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                results["filename"] = resume_file.name
                st.session_state.results = results
                st.session_state.history.append(results)
                st.success("✅ Analysis completed successfully!")
            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {str(e)}")

if st.session_state.results:
    results = st.session_state.results

    if st.session_state.translate_toggle:
        summary_title = "📝 Ringkasan Eksekutif (Bahasa Melayu)"
        summary_content = results["summary_malay"] if results.get("summary_malay") else "Malay summary is not available in the results."
    else:
        summary_title = "📝 Executive Summary (English)"
        summary_content = results["summary"]

    st.markdown("---")
    st.markdown("## 📊 Analysis Results")

    st.markdown(f"""
    <div class="fit-score-container">
        <h2 style="margin: 0; color: #333;">✅ Overall Candidate Fit Score</h2>
        <div class="fit-score">{results['fit_score']}</div>
        <p style="color: #666; font-size: 1.1rem;">Based on AI-powered resume analysis</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 Detailed Analysis")

    with st.container():
        st.markdown("#### 👤 Candidate Profile")
        st.info(results["profile"])

    with st.container():
        st.markdown(f"#### {summary_title}")
        st.success(summary_content)

    with st.container():
        st.markdown("#### ❓ Suggested Interview Questions")
        st.warning(results["question_gen"])

    st.markdown("---")
    st.markdown("### 💾 Export Results")
    
    report_text = f"""
====== AI RESUME ANALYSIS REPORT ======

File: {results['filename']}
Generated: {results['timestamp']}

Fit Score: {results['fit_score']}

Candidate Profile:
{results['profile']}

Executive Summary (English):
{results['summary']}

Executive Summary (Malay):
{results.get('summary_malay', 'N/A')}

Suggested Interview Questions:
{results['question_gen']}
"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Full Report",
            data=report_text,
            file_name=f"resume_analysis_{results['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Powered by AI • Made with ❤️ using Streamlit & JamAI</p>
</div>
""", unsafe_allow_html=True)
