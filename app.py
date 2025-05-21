from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load parsed chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract unique documents and sections (safely check for 'section')
available_documents = sorted(set(chunk["document"] for chunk in chunks if "document" in chunk))
available_sections = sorted(set(chunk["section"] for chunk in chunks if "section" in chunk and chunk["section"]))

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "")
    selected_document = request.form.get("document", "")
    selected_section = request.form.get("section", "")

    results = []
    if keyword:
        for chunk in chunks:
            text_match = keyword.lower() in chunk.get("text", "").lower()
            document_match = (not selected_document or chunk.get("document") == selected_document)
            section_match = (not selected_section or chunk.get("section") == selected_section)

            if text_match and document_match and section_match:
                results.append(chunk)

    return render_template("index.html", results=results, keyword=keyword,
                           available_documents=available_documents,
                           available_sections=available_sections,
                           selected_document=selected_document,
                           selected_section=selected_section)

# Only used when running locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
