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