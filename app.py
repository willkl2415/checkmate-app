from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

# Collect unique document and section values
available_documents = sorted(set(chunk["document"] for chunk in chunks))
available_sections = sorted(set(chunk["section"] for chunk in chunks))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    selected_doc = "All documents"
    selected_section = "All sections"

    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        selected_doc = request.form.get("document", "All documents")
        selected_section = request.form.get("section", "All sections")

        for chunk in chunks:
            text = chunk["text"].lower()
            if query in text:
                if (selected_doc == "All documents" or chunk["document"] == selected_doc) and \
                   (selected_section == "All sections" or chunk["section"] == selected_section):
                    results.append(chunk)

    return render_template("index.html",
                           results=results,
                           query=query,
                           documents=available_documents,
                           sections=available_sections,
                           selected_doc=selected_doc,
                           selected_section=selected_section)

if __name__ == "__main__":
    app.run(debug=True)
