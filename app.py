from flask import Flask, render_template, request
import json
from answer_engine import answer_question

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

available_documents = sorted(set(chunk["document"] for chunk in chunks))
available_sections = sorted(set(chunk["section"] for chunk in chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    selected_document = ""
    selected_section = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        selected_document = request.form.get("document", "")
        selected_section = request.form.get("section", "")

        results = answer_question(
            keyword=query,
            chunks=chunks,
            selected_document=selected_document,
            selected_section=selected_section
        )

    return render_template("index.html",
                           query=query,
                           selected_document=selected_document,
                           selected_section=selected_section,
                           results=results,
                           available_documents=available_documents,
                           available_sections=available_sections)

if __name__ == "__main__":
    app.run(debug=True)
