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