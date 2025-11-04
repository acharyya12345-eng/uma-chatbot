from flask import Flask, render_template, request, jsonify
import pdfplumber
from pathlib import Path

app = Flask(__name__)

# --- Update this if your CV filename is different
CV_FILENAME = "Resume ( Uma Gupta Acharyya ).pdf"

# Try to load the CV text (optional file)
def load_cv_text():
    p = Path(CV_FILENAME)
    if not p.exists():
        return ""
    text = ""
    with pdfplumber.open(str(p)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

cv_text = load_cv_text()

# Simple rule-based responder using CV fields (you can edit these replies)
def chatbot_response(user_input: str) -> str:
    u = user_input.lower()
    if "skill" in u or "skills" in u:
        return "I’m skilled in Excel, Power BI, SQL, Python, AI tools, and data visualization. (Source: CV)"
    if "education" in u or "study" in u:
        return "I hold an MSc and B.Ed, along with Data Analysis and Financial Literacy certifications. (Source: CV)"
    if "experience" in u or "work" in u:
        return "I’ve worked as a Freelance Data Analyst and Educator, building dashboards and training learners. (Source: CV)"
    if "achievement" in u or "achievements" in u:
        return "I’ve created 20+ dashboards, mentored 100+ students, cleared CTET, and launched Coddex Hub. (Source: CV)"
    if "project" in u or "projects" in u:
        return "Projects include Power BI sales dashboards, Excel automation, and Python-based data cleaning. (Source: CV)"
    if "certification" in u or "certifications" in u:
        return "Certifications: Data Analyst (IRA Skills), 2X Income Model, CTET, DCA. (Source: CV)"
    if "summary" in u or "profile" in u or "about" in u:
        return "I’m Uma Gupta Acharyya — educator, data analyst, and founder of Coddex Hub. (Source: CV)"
    # small attempt to use CV_text if user asked open question
    if len(cv_text) > 50 and any(word in u for word in ("cv", "resume", "details")):
        return "I have the CV loaded and can answer questions about skills, education, experience, projects, achievements, and certifications."
    return "I don't have that information in the CV. Please ask about skills, education, experience, projects, achievements, or certifications."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    reply = chatbot_response(message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Render expects host 0.0.0.0 and port 10000
    app.run(host="0.0.0.0", port=10000)
