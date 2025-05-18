from flask import Flask, render_template, request
from answer_engine import answer_question, load_ingested_chunks
import json

app = Flask(__name__)

# Load all chunks and get unique documents and sections
all_chunks = load_ingested_chunks()
all_documents = sorted(set(chunk.get("source", "Unknown") for chunk in all_chunks))
all_sections = sorted(set(chunk.get("section_title", "Unknown") for chunk in all_chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    keyword = ""
    section_filter = "All Sections"
    document_filter = "All"
    detailed = False

    if request.method == "POST":
        query = request.form.get("question", "")
        keyword = request.form.get("keyword", "")
        section_filter = request.form.get("section", "All Sections")
        document_filter = request.form.get("document", "All")
        detailed = bool(request.form.get("detailed"))

        results = answer_question(
            question=query,
            keyword=keyword,
            section=section_filter,
            document=document_filter,
            detailed=detailed
        )

    return render_template(
        "index.html",
        results=results,
        query=query,
        keyword=keyword,
        selected_section=section_filter,
        selected_document=document_filter,
        detailed=detailed,
        all_sections=["All Sections"] + all_sections,
        all_documents=["All"] + all_documents,
        result_count=len(results)
    )

if __name__ == "__main__":
    app.run(debug=True)
