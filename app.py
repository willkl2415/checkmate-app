from flask import Flask, render_template, request
import json
from answer_engine import answer_question

app = Flask(__name__)

# Load chunks from file once on startup
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Get list of unique documents
def get_available_documents():
    return sorted(set(chunk["document"] for chunk in chunks))

# Get list of unique sections for a selected document
def get_sections_for_document(document_name):
    return sorted(set(
        chunk["section"] for chunk in chunks
        if chunk["document"] == document_name
    ))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    keyword = ""
    document_filter = "All"
    section_filter = "All"
    show_detailed = False

    available_documents = get_available_documents()
    available_sections = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        keyword = request.form.get("keyword", "").strip()
        document_filter = request.form.get("document_filter", "All")
        section_filter = request.form.get("section_filter", "All")
        show_detailed = request.form.get("show_detailed") == "on"

        results = answer_question(
            chunks,
            query=query,
            keyword=keyword,
            document_filter=document_filter,
            section_filter=section_filter,
            detailed=show_detailed,
        )

    if document_filter != "All":
        available_sections = get_sections_for_document(document_filter)

    return render_template(
        "index.html",
        results=results,
        query=query,
        keyword=keyword,
        document_filter=document_filter,
        section_filter=section_filter,
        show_detailed=show_detailed,
        available_documents=available_documents,
        available_sections=available_sections,
        result_count=len(results)
    )

if __name__ == "__main__":
    app.run(debug=True)
