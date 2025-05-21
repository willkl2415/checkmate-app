from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load parsed chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Extract unique documents and sections
available_documents = sorted(set(chunk["document"] for chunk in chunks))
available_sections = sorted(set(chunk["section"] for chunk in chunks if chunk["section"]))

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "")
    selected_document = request.form.get("document", "")
    selected_section = request.form.get("section", "")

    results = []
    if keyword:
        for chunk in chunks:
            if keyword.lower() in chunk["text"].lower():
                if (not selected_document or chunk["document"] == selected_document) and \
                   (not selected_section or chunk["section"] == selected_section):
                    results.append(chunk)

    return render_template("index.html", results=results, keyword=keyword,
                           available_documents=available_documents,
                           available_sections=available_sections,
                           selected_document=selected_document,
                           selected_section=selected_section)

# Only used when running locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
