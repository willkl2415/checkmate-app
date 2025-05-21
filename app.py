from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load chunks and exclude all Glossary results
with open("chunks.json", "r", encoding="utf-8") as f:
    raw_chunks = json.load(f)

# Completely exclude glossary content from results and filters
chunks = [
    chunk for chunk in raw_chunks
    if "glossary" not in chunk.get("heading", "").lower()
       and "glossary" not in chunk.get("content", "").lower()
]

# Pre-calculate available documents
available_documents = sorted(set(chunk.get("document", "") for chunk in chunks))


def get_valid_sections(document_name):
    """Return only sections with at least one chunk for the selected document."""
    section_counts = {}

    for chunk in chunks:
        if document_name and chunk.get("document", "") != document_name:
            continue
        heading = chunk.get("heading", "").strip()
        if heading:
            section_counts[heading] = section_counts.get(heading, 0) + 1

    return sorted([section for section, count in section_counts.items() if count > 0])


@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "").strip().lower()
    selected_document = request.form.get("document", "")
    selected_section = request.form.get("section", "")

    # Dynamically determine dropdown for valid headings
    available_sections = get_valid_sections(selected_document)

    # Build filtered results
    results = []
    for chunk in chunks:
        doc = chunk.get("document", "")
        heading = chunk.get("heading", "")
        content = chunk.get("content", "")

        if selected_document and doc != selected_document:
            continue
        if selected_section and heading != selected_section:
            continue
        if keyword and keyword not in content.lower():
            continue

        results.append({
            "document": doc,
            "section": heading,
            "text": content
        })

    return render_template("index.html",
                           results=results,
                           keyword=keyword,
                           available_documents=available_documents,
                           available_sections=available_sections,
                           selected_document=selected_document,
                           selected_section=selected_section)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
