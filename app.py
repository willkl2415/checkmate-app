from flask import Flask, request, render_template
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
    document_filter = "All"
    section_filter = "All"
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        document_filter = request.form.get("document_filter", "All")
        section_filter = request.form.get("section_filter", "All")

        results = answer_question(
            chunks=chunks,
            query=query,
            keyword="",
            source_filter=document_filter,
            section_filter=section_filter,
            detailed=True
        )

    return render_template(
        "index.html",
        results=results,
        result_count=len(results),
        query=query,
        available_documents=available_documents,
        available_sections=available_sections,
        document_filter=document_filter,
        section_filter=section_filter
    )

if __name__ == "__main__":
    app.run(debug=True)
