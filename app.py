from flask import Flask, render_template, request
from answer_engine import answer_question
import json

app = Flask(__name__)

# Load preprocessed chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

def get_available_sources(chunks):
    return list(sorted(set(chunk["source"] for chunk in chunks)))

def get_available_sections(chunks):
    return list(sorted(set(chunk.get("section", "Unsectioned") for chunk in chunks)))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    keyword = ""
    selected_section = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        keyword = request.form.get("keyword", "").strip().lower()
        selected_section = request.form.get("section", "")

        results = answer_question(query, keyword, chunks)

        if selected_section:
            results = [
                r for r in results
                if r["section"].lower() == selected_section.lower()
            ]

    sources = get_available_sources(chunks)
    sections = get_available_sections(chunks)
    result_count = len(results)

    return render_template(
        "index.html",
        results=results,
        query=query,
        keyword=keyword,
        sources=sources,
        sections=sections,
        selected_section=selected_section,
        result_count=result_count,
    )

if __name__ == "__main__":
    app.run(debug=True)
