import os
from flask import Flask, request, render_template, jsonify
import nltk
import spacy
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Download NLTK resources
nltk.download('punkt')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# --- Simple AI vs Human Resume Detector ---
# For demo purposes, we train a tiny classifier with sample data
sample_texts = [
    "I am a highly motivated individual with experience in software development and problem solving.",  # human
    "This resume was generated using advanced AI language models to optimize keyword density and ATS scoring.",  # AI
]
sample_labels = [0, 1]  # 0 = human, 1 = AI

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(sample_texts)
clf = LogisticRegression()
clf.fit(X, sample_labels)

@app.route("/")
def home():
    return "Resume Analyzer is running on Render!"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Tokenize with NLTK
    tokens = nltk.word_tokenize(text)

    # Named Entity Recognition with spaCy
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # AI vs Human detection
    X_test = vectorizer.transform([text])
    prediction = clf.predict(X_test)[0]
    result = "AI-generated" if prediction == 1 else "Human-written"

    return jsonify({
        "filename": file.filename,
        "tokens_count": len(tokens),
        "entities": entities,
        "ai_detection": result
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
