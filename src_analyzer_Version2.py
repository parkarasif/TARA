import re
from .job_description_parser import extract_keywords

def analyze_resume(resume_text, jd_text):
    jd_keywords = extract_keywords(jd_text)
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    match_count = len(jd_keywords & resume_words)
    score = match_count / len(jd_keywords) * 100 if jd_keywords else 0

    feedback = []
    if score < 50:
        feedback.append("Consider adding more relevant keywords from the job description.")
    if "education" not in resume_text.lower():
        feedback.append("Missing 'Education' section.")
    if "experience" not in resume_text.lower():
        feedback.append("Missing 'Experience' section.")
    if "skills" not in resume_text.lower():
        feedback.append("Missing 'Skills' section.")

    return {
        "score": score,
        "matched_keywords": list(jd_keywords & resume_words),
        "total_keywords": len(jd_keywords),
        "feedback": feedback
    }