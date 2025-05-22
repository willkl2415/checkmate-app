from flask import Flask, render_template, request
import json
import re

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract all unique document names and section titles
documents = sorted(set(chunk["document"] for chunk in chunks))
sections = sorted(set(chunk["section"] for chunk in chunks if chunk["section"]))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    selected_document = "All documents"
    selected_section = "All sections"

    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        selected_document = request.form.get("document", "All documents")
        selected_section = request.form.get("section", "All sections")

        for chunk in chunks:
            text = chunk["text"].lower()
            doc_match = (selected_document == "All documents" or chunk["document"] == selected_document)
            section_match = (selected_section == "All sections" or chunk["section"] == selected_section)

            if query in text and doc_match and section_match:
                results.append(chunk)

    # Determine context-appropriate section options
    filtered_sections = sorted(set(
        chunk["section"]
        for chunk in chunks
        if (selected_document == "All documents" or chunk["document"] == selected_document)
    ))

    return render_template(
        "index.html",
        results=results,
        query=query,
        documents=["All documents"] + documents,
        sections=["All sections"] + filtered_sections,
        selected_document=selected_document,
        selected_section=selected_section
    )

if __name__ == "__main__":
    app.run(debug=True)
