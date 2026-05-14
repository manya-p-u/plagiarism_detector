import os
from flask import Flask, render_template, request, send_file
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import PyPDF2
import docx
import csv

from modules.report_generator import generate_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================
# 📄 FILE READERS
# =========================

def read_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])


def read_csv(path):
    text = ""
    with open(path, newline='', encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            text += " ".join(row) + " "
    return text


def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text(path):
    ext = path.split('.')[-1].lower()

    if ext == "pdf":
        return read_pdf(path)
    elif ext == "docx":
        return read_docx(path)
    elif ext == "csv":
        return read_csv(path)
    else:
        return read_txt(path)


# =========================
# 🔍 SIMILARITY FUNCTION
# =========================

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)


def get_sentence_matches(text1, text2):
    sentences1 = text1.split('.')
    sentences2 = text2.split('.')

    matches = []

    for s1 in sentences1:
        for s2 in sentences2:
            if len(s1.strip()) > 20 and len(s2.strip()) > 20:
                score = calculate_similarity(s1, s2)
                if score > 30:
                    matches.append((s1.strip(), s2.strip(), score))

    return matches


# =========================
# 🧠 XAI SUGGESTION
# =========================

def generate_suggestion(score):
    if score > 70:
        return "High plagiarism detected. Rewrite content completely and add citations."
    elif score > 40:
        return "Moderate similarity. Try paraphrasing sentences and improve originality."
    else:
        return "Low plagiarism. Your content looks good."


# =========================
# 🌐 ROUTES
# =========================

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/check', methods=["POST"])
def check():
    files = request.files.getlist("files")

    if len(files) < 2:
        return "Please upload at least 2 files"

    file_paths = []

    # Save files
    for file in files:
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)
        file_paths.append(path)

    # Extract text
    texts = [extract_text(p) for p in file_paths]

    # Compare first two files
    text1, text2 = texts[0], texts[1]

    avg_score = calculate_similarity(text1, text2)

    matches_all = get_sentence_matches(text1, text2)

    suggestion = generate_suggestion(avg_score)

    # Generate PDF report
    pdf_path = os.path.join(REPORT_FOLDER, "report.pdf")
    generate_pdf(avg_score, matches_all, pdf_path)

    return render_template(
        "result.html",
        score=avg_score,
        matches=matches_all,
        suggestion=suggestion
    )


@app.route('/download')
def download():
    path = os.path.join(REPORT_FOLDER, "report.pdf")
    return send_file(path, as_attachment=True)


# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    print("🚀 Starting Flask App...")
    app.run(debug=True)