from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load the structured chunks.json file
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Build document and section dropdown options
available_documents = sorted(set(chunk.get("document", "") for chunk in chunks))
available_sections = sorted(set(chunk.get("heading", "") for chunk in chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    keyword = request.form.get("keyword", "").strip().lower()
    selected_document = request.form.get("document", "")
    selected_section = request.form.get("section", "")

    results = []
    if keyword:
        for chunk in chunks:
            content = chunk.get("content", "").lower()
            document = chunk.get("document", "")
            heading = chunk.get("heading", "")

            # Match logic
            if keyword in content:
                if (not selected_document or selected_document == document) and \
                   (not selected_section or selected_section == heading):
                    results.append({
                        "document": document,
                        "section": heading,
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
