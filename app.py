from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load chunks from the JSON file
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract all available documents and sections (renamed headings)
available_documents = sorted(set(chunk.get("document", "Unknown Document") for chunk in chunks))
available_sections = sorted(set(chunk.get("heading", "No Heading") for chunk in chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "").lower()
    selected_document = request.form.get("document", "")
    selected_section = request.form.get("section", "")

    results = []
    if keyword:
        for chunk in chunks:
            content = chunk.get("content", "").lower()
            doc_match = (not selected_document or chunk.get("document") == selected_document)
            section_match = (not selected_section or chunk.get("heading") == selected_section)
            if keyword in content and doc_match and section_match:
                results.append({
                    "document": chunk.get("document", ""),
                    "section": chunk.get("heading", "No Heading"),
                    "text": chunk.get("content", "")
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
