from flask import Flask, render_template, request
import json
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    question = ""
    keyword = ""
    selected_section = ""
    sources = get_available_sources(chunks)
    section_titles = sorted(list({chunk['heading'] for chunk in chunks}))

    if request.method == "POST":
        question = request.form.get("question", "")
        keyword = request.form.get("keyword", "")
        selected_section = request.form.get("section", "")

        results = answer_question(
            question=question,
            keyword=keyword,
            section=selected_section,
            chunks=chunks
        )

    return render_template(
        "index.html",
        results=results,
        question=question,
        keyword=keyword,
        selected_section=selected_section,
        sources=sources,
        section_titles=section_titles
    )

if __name__ == "__main__":
    app.run(debug=True)
