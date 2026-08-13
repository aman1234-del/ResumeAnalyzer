import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Render! Your Resume Analyzer is running."

# Example route for file upload (adjust if you already have one)
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]
    return f"Uploaded: {file.filename}"

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
