from flask import Flask, render_template, request
import PyPDF2
import spacy
import nltk
from nltk.corpus import stopwords

# Download NLTK resources (only needed once)
nltk.download('punkt')
nltk.download('punkt_tab')   # <-- added fix
nltk.download('stopwords')

# Create Flask app
app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# --- AI Detection Function ---
def detect_ai_text(text):
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    avg_sentence_len = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
    stopword_ratio = sum(1 for w in words if w.lower() in stop_words) / max(1, len(words))

    if avg_sentence_len > 25 and stopword_ratio < 0.35:
        return "⚠️ This resume looks AI‑generated."
    else:
        return "✅ This resume looks human‑written."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    if file and file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        ai_result = detect_ai_text(text)

        return render_template('result.html', text=text, entities=entities, ai_result=ai_result)

    return "No file uploaded!"

if __name__ == '__main__':
    app.run(debug=True)
