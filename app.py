from flask import Flask, render_template, request
import json
import os
from answer_engine import answer_question
from ingest import load_ingested_chunks, get_available_sources, get_available_sections

app = Flask(__name__)

CHUNKS_FILE = "chunks.json"
chunks = []

if os.path.exists(CHUNKS_FILE):
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    total_results = 0
    query = ""
    keyword = ""
    selected_doc = "All"
    selected_section = "All"
    detailed = False

    documents = get_available_sources(chunks)
    sections = get_available_sections(chunks)

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        keyword = request.form.get("keyword", "").strip()
        selected_doc = request.form.get("document", "All")
        selected_section = request.form.get("section", "All")
        detailed = request.form.get("detailed") == "on"

        results = answer_question(
            chunks,
            query=query,
            keyword=keyword,
            document_filter=selected_doc,
            section_filter=selected_section,
            detailed=detailed,
        )
        total_results = len(results)

    return render_template(
        "index.html",
        results=results,
        total_results=total_results,
        query=query,
        keyword=keyword,
        documents=documents,
        sections=sections.get(selected_doc, []),
        selected_doc=selected_doc,
        selected_section=selected_section,
        detailed=detailed,
    )


if __name__ == "__main__":
    app.run(debug=True)
