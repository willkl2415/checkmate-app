from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load parsed chunks with new structure
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract documents and headings
available_documents = sorted(set(chunk["document"] for chunk in chunks if "document" in chunk))
available_headings = sorted(set(chunk["heading"] for chunk in chunks if "heading" in chunk and chunk["heading"]))

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "")
    selected_document = request.form.get("document", "")
    selected_heading = request.form.get("section", "")  # form name remains 'section' for compatibility

    results = []
    if keyword:
        for chunk in chunks:
            text_match = keyword.lower() in chunk.get("content", "").lower()
            doc_match = (not selected_document or chunk.get("document") == selected_document)
            heading_match = (not selected_heading or chunk.get("heading") == selected_heading)

            if text_match and doc_match and heading_match:
                results.append({
                    "document": chunk.get("document", ""),
                    "section": chunk.get("heading", "No Heading"),
                    "text": chunk.get("content", "")
                })

    return render_template("index.html", results=results, keyword=keyword,
                           available_documents=available_documents,
                           available_sections=available_headings,
                           selected_document=selected_document,
                           selected_section=selected_heading)

# For local testing
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
