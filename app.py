import streamlit as st
import plotly.express as px

from resume_utils import extract_text_from_pdf
from score import analyze_resume, calculate_job_match

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.title("📄 AI Resume Analyzer")

st.markdown("""
Analyze your resume and compare it with a Job Description.

### Features

- 📊 ATS Score
- 🎯 Job Match Score
- ✅ Skills Found
- ❌ Missing Skills
- 💼 Recommended Job Role
- 💡 Resume Suggestions
- 📈 Skill Distribution Chart
""")

st.divider()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("About")

st.sidebar.info("""
This application helps you:

✅ Analyze your Resume

✅ Calculate ATS Score

✅ Compare with Job Description

✅ Suggest Improvements

✅ Recommend Job Role
""")

# -------------------------------------------------------
# Upload Resume
# -------------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload Resume (PDF)",
    type=["pdf"]
)

# -------------------------------------------------------
# Job Description
# -------------------------------------------------------

job_description = st.text_area(
    "📋 Paste Job Description (Optional)",
    height=200,
    placeholder="Paste the Job Description here..."
)

# -------------------------------------------------------
# Analyze Button
# -------------------------------------------------------

if uploaded_file is not None:

    if st.button("🚀 Analyze Resume", use_container_width=True):

        with st.spinner("Analyzing Resume..."):

            resume_text = extract_text_from_pdf(uploaded_file)

            if resume_text:

                result = analyze_resume(resume_text)

                # --------------------------------------------
                # Job Match
                # --------------------------------------------

                if job_description.strip():

                    match_score = calculate_job_match(
                        resume_text,
                        job_description
                    )

                else:

                    match_score = None

                # --------------------------------------------
                # Dashboard
                # --------------------------------------------

                st.subheader("📊 Resume Dashboard")

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric(
                        "ATS Score",
                        f"{result['ats_score']}%"
                    )

                with c2:
                    st.metric(
                        "Skills Found",
                        len(result["skills_found"])
                    )

                with c3:
                    st.metric(
                        "Missing Skills",
                        len(result["missing_skills"])
                    )

                with c4:

                    if match_score is not None:
                        st.metric(
                            "Job Match",
                            f"{match_score}%"
                        )
                    else:
                        st.metric(
                            "Job Match",
                            "N/A"
                        )

                st.metric(
                    "Total Skills Checked",
                    len(result["skills_found"]) + len(result["missing_skills"])
                )        

                import plotly.graph_objects as go
                
                gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=result["ats_score"],
                        title={"text": "ATS Score"},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "green"},
                            "steps": [
                                {"range": [0, 40], "color": "#ff4d4d"},
                                {"range": [40, 70], "color": "#ffcc00"},
                                {"range": [70, 100], "color": "#00cc66"},
                            ],
                        
                        },
                    )
                )
                
                st.plotly_chart(gauge, use_container_width=True)
                
                # --------------------------------------------
                # Skills
                # --------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("✅ Skills Found")

                    if result["skills_found"]:

                        for skill in result["skills_found"]:
                            st.success(skill.title())

                    else:

                        st.info("No matching skills found.")

                with col2:

                    st.subheader("❌ Missing Skills")

                    if result["missing_skills"]:

                        for skill in result["missing_skills"]:
                            st.warning(skill.title())

                    else:

                        st.success("No Missing Skills.")

                st.divider()

                # --------------------------------------------
                # Skill Distribution Chart
                # --------------------------------------------

                chart_data = {
                    "Category": [
                        "Skills Found",
                        "Missing Skills"
                    ],
                    "Count": [
                        len(result["skills_found"]),
                        len(result["missing_skills"])
                    ]
                }

                fig = px.pie(
                    chart_data,
                    names="Category",
                    values="Count",
                    title="Skill Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.divider()

                # --------------------------------------------
                # Recommended Role
                # --------------------------------------------

                st.subheader("💼 Recommended Job Role")

                st.success(result["recommended_role"])

                st.divider()

                                # --------------------------------------------
                # Suggestions
                # --------------------------------------------

                st.subheader("💡 Resume Improvement Suggestions")

                for suggestion in result["suggestions"]:
                    st.info(suggestion)

                st.divider()
                
                st.subheader("📑 Resume Section Checker")
                status = result["section_status"]
                col1, col2 = st.columns(2)
                items = list(status.items())
                mid = (len(items) + 1) // 2
                with col1:
                    for section, present in items[:mid]:
                        if present:
                            st.success(f"✅ {section}")
                        else:
                            st.error(f"❌ {section}")
                with col2:
                    for section, present in items[mid:]:
                        if present:
                            st.success(f"✅ {section}")
                        else:
                            st.error(f"❌ {section}")
   
                st.divider()

                report = f"""
                AI RESUME ANALYSIS REPORT
                
                ====================================
                
                ATS Score: {result['ats_score']}%
                
                Recommended Role:
                {result['recommended_role']}
                
                ------------------------------------
                
                Skills Found:
                {', '.join(result['skills_found'])}
                
                ------------------------------------

                Missing Skills:
                {', '.join(result['missing_skills'])}
                
                ------------------------------------
                
                Suggestions:
                
                """
                
                for suggestion in result["suggestions"]:
                    report += f"• {suggestion}\n"
                    
                report += "\n------------------------------------\n"
                
                report += "Resume Sections\n\n"
                
                for section, status in result["section_status"].items():
                    symbol = "✓" if status else "✗"
                    report += f"{symbol} {section}\n"
                    
                st.download_button(
                    label="⬇ Download Resume Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
