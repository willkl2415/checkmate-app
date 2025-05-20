from flask import Flask, render_template, request
import json
from answer_engine import answer_question

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

documents = sorted(set(chunk["document"] for chunk in chunks))
headings = sorted(set(chunk["heading"] for chunk in chunks if "Glossary" not in chunk["heading"]))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    selected_document = ""
    selected_heading = ""
    show_detailed = False

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        selected_document = request.form.get("filter_document", "")
        selected_heading = request.form.get("filter_heading", "")
        show_detailed = bool(request.form.get("show_detailed"))

        if query:
            results = answer_question(query, selected_document, selected_heading, show_detailed)

    return render_template(
        "index.html",
        results=results,
        request=request,
        documents=documents,
        headings=headings,
        selected_document=selected_document,
        selected_heading=selected_heading,
        show_detailed=show_detailed
    )

if __name__ == "__main__":
    app.run(debug=True)
