# TARA
Helping Website for Talent Acquistion Recruitment Assistance
ats-resume-analyzer/
├── README.md
├── LICENSE
├── requirements.txt
├── src/
│   ├── main.py
│   ├── resume_parser.py
│   ├── analyzer.py
│   ├── job_description_parser.py
│   ├── utils.py
│   └── templates/
├── tests/
│   ├── test_parser.py
│   ├── test_analyzer.py
│   └── sample_resumes/
├── .github/
│   └── workflows/
│       └── ci.yml
└── web/
    ├── app.py (Flask/FastAPI)
    └── static/
    import sys
from resume_parser import parse_resume
from analyzer import analyze_resume

def main(resume_path, jd_path):
    resume_text = parse_resume(resume_path)
    jd_text = open(jd_path).read()
    report = analyze_resume(resume_text, jd_text)
    print(report)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    import re

def extract_keywords(jd_text):
    # Simple extraction: words longer than 2 letters, not common stopwords
    stopwords = {'the', 'and', 'for', 'with', 'you', 'are', 'this', 'that', 'from', 'will', 'have', 'your', 'our'}
    words = re.findall(r'\b[a-zA-Z]{3,}\b', jd_text.lower())
    keywords = set(w for w in words if w not in stopwords)
    return keywords
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
    import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx', 'txt'}

def secure_filename(filename):
    return os.path.basename(filename)
    import sys
from resume_parser import parse_resume
from analyzer import analyze_resume

def main(resume_path, jd_path):
    resume_text = parse_resume(resume_path)
    jd_text = open(jd_path).read()
    report = analyze_resume(resume_text, jd_text)
    print(report)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    from flask import Flask, render_template, request, redirect, url_for, flash
import os
from src.resume_parser import parse_resume
from src.analyzer import analyze_resume

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        resume = request.files.get("resume")
        jobdesc = request.files.get("jobdesc")
        if not resume or not jobdesc:
            flash("Both files are required.")
            return redirect(request.url)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jobdesc.filename)
        resume.save(resume_path)
        jobdesc.save(jd_path)
        try:
            resume_text = parse_resume(resume_path)
            jd_text = open(jd_path, encoding='utf-8').read()
            report = analyze_resume(resume_text, jd_text)
            return render_template("result.html", report=report)
        except Exception as e:
            flash("Error processing files: " + str(e))
            return redirect(request.url)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
<!doctype html>
<html>
<head>
  <title>ATS Resume Analyzer</title>
</head>
<body>
  <h1>ATS Resume Analyzer</h1>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul>
        {% for message in messages %}
          <li style="color:red;">{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  <form method="post" enctype="multipart/form-data">
    <label for="resume">Upload Resume (PDF/DOCX/TXT):</label><br>
    <input type="file" name="resume" required><br><br>
    <label for="jobdesc">Upload Job Description (TXT):</label><br>
    <input type="file" name="jobdesc" required><br><br>
    <input type="submit" value="Analyze">
  </form>
</body>
</html>
