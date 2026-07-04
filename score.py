import re


def analyze_resume(resume_text):
    """
    Analyze the resume and return:
    - ATS Score
    - Skills Found
    - Missing Skills
    - Recommended Job Role
    - Resume Suggestions
    """

    resume_text = resume_text.lower()

        # ----------------------------
    # Resume Section Checker
    # ----------------------------

    section_status = {
        "Education": "education" in resume_text,
        "Projects": "project" in resume_text,
        "Experience": "experience" in resume_text or "internship" in resume_text,
        "Skills": "skills" in resume_text,
        "Certifications": "certification" in resume_text or "certifications" in resume_text,
        "GitHub": "github" in resume_text,
        "LinkedIn": "linkedin" in resume_text
    }

    # ----------------------------
    # Technical Skills Database
    # ----------------------------
    required_skills = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "git",
        "github",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "streamlit",
        "flask",
        "docker",
        "linux",
        "opencv",
        "scikit-learn",
        "data analysis",
        "data science",
        "aws"
    ]

    skills_found = []
    missing_skills = []

    # ----------------------------
    # Skill Detection
    # ----------------------------
    for skill in required_skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, resume_text):
            skills_found.append(skill)
        else:
            missing_skills.append(skill)

    # ----------------------------
    # ATS Score Calculation
    # ----------------------------

    ats_score = 0

    # 1. Technical Skills (40 marks)
    skill_score = (len(skills_found) / len(required_skills)) * 40
    ats_score += skill_score

    # 2. Projects (15 marks)
    if "project" in resume_text:
        ats_score += 15

    # 3. Education (10 marks)
    if "education" in resume_text:
        ats_score += 10

    # 4. Experience / Internship (10 marks)
    if "experience" in resume_text or "internship" in resume_text:
        ats_score += 10

    # 5. Certifications (10 marks)
    if "certification" in resume_text or "certifications" in resume_text:
        ats_score += 10

    # 6. GitHub (5 marks)
    if "github" in resume_text:
        ats_score += 5

    # 7. LinkedIn (5 marks)
    if "linkedin" in resume_text:
        ats_score += 5

    # 8. Resume Length (5 marks)
    word_count = len(resume_text.split())
    
    if word_count >= 300:
        ats_score += 5
    elif word_count >= 200:
        ats_score += 3
    
    ats_score = min(round(ats_score), 100)

    # ----------------------------
    # Bonus ATS Points
    # ----------------------------
    if "projects" in resume_text:
        ats_score += 5

    if "education" in resume_text:
        ats_score += 5

    if "experience" in resume_text:
        ats_score += 5

    if "certification" in resume_text:
        ats_score += 5

    ats_score = min(ats_score, 100)

    # ----------------------------
    # Job Role Recommendation
    # ----------------------------
    if "tensorflow" in skills_found or "pytorch" in skills_found:
        recommended_role = "AI / Deep Learning Engineer"

    elif (
        "machine learning" in skills_found
        and "python" in skills_found
    ):
        recommended_role = "Machine Learning Engineer"

    elif (
        "python" in skills_found
        and "sql" in skills_found
        and "pandas" in skills_found
    ):
        recommended_role = "Data Analyst"

    elif (
        "html" in skills_found
        and "css" in skills_found
        and "javascript" in skills_found
    ):
        recommended_role = "Frontend Developer"

    elif (
        "react" in skills_found
        and "node.js" in skills_found
    ):
        recommended_role = "Full Stack Developer"

    elif (
        "docker" in skills_found
        and "linux" in skills_found
    ):
        recommended_role = "DevOps Engineer"

    elif (
        "opencv" in skills_found
        and "python" in skills_found
    ):
        recommended_role = "Computer Vision Engineer"

    else:
        recommended_role = "Software Developer"

    # ----------------------------
    # Resume Suggestions
    # ----------------------------
    suggestions = []

    if "github" not in resume_text:
        suggestions.append("Add your GitHub profile link.")

    if "linkedin" not in resume_text:
        suggestions.append("Add your LinkedIn profile link.")

    if "projects" not in resume_text:
        suggestions.append("Include at least 2-3 technical projects.")

    if "experience" not in resume_text:
        suggestions.append("Mention internships or relevant practical experience.")

    if "certification" not in resume_text:
        suggestions.append("Add relevant certifications.")

    if "education" not in resume_text:
        suggestions.append("Ensure the Education section is clearly visible.")

    if "skills" not in resume_text:
        suggestions.append("Create a dedicated Skills section.")

    if ats_score < 70:
        suggestions.append("Increase your ATS score by adding more relevant technical skills.")

    if len(skills_found) < 10:
        suggestions.append("Include more technologies relevant to your target job role.")

    if not suggestions:
        suggestions.append("Excellent! Your resume looks strong.")

    # ----------------------------
    # Return Results
    # ----------------------------
    return {
        "skills_found": skills_found,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "recommended_role": recommended_role,
        "suggestions": suggestions,
        "section_status": section_status
    }


# ==========================================================
# Job Description Matching
# ==========================================================

def calculate_job_match(resume_text, job_description):
    """
    Compare the resume against a job description
    and return a match percentage.
    """

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    # Extract words
    resume_words = set(re.findall(r"\b[a-zA-Z0-9.+#-]+\b", resume_text))
    jd_words = set(re.findall(r"\b[a-zA-Z0-9.+#-]+\b", job_description))

    # Ignore very short words
    jd_words = {word for word in jd_words if len(word) > 2}

    if len(jd_words) == 0:
        return 0

    matched_words = resume_words.intersection(jd_words)

    match_percentage = round(
        (len(matched_words) / len(jd_words)) * 100
    )

    return min(match_percentage, 100)