from flask import Flask, render_template, request
import json
from answer_engine import answer_question

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

available_documents = sorted(set(c["document"] for c in chunks))
available_sections = sorted(set(c["section"] for c in chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = ""
    selected_document = ""
    selected_section = ""
    results = []

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        selected_document = request.form.get("document", "")
        selected_section = request.form.get("section", "")
        results = answer_question(keyword, chunks, selected_document, selected_section)

    return render_template("index.html",
                           keyword=keyword,
                           selected_document=selected_document,
                           selected_section=selected_section,
                           results=results,
                           available_documents=available_documents,
                           available_sections=available_sections)

if __name__ == "__main__":
    app.run(debug=True)
