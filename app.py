from flask import Flask, request, render_template
from answer_engine import answer_question, get_available_sections
from ingest import load_ingested_chunks

app = Flask(__name__)
chunks = load_ingested_chunks()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    selected_section = "All Sections"
    if request.method == "POST":
        question = request.form.get("question", "")
        keyword = request.form.get("keyword", "")
        selected_section = request.form.get("section", "All Sections")
        results = answer_question(question, keyword, selected_section, chunks)
    sections = get_available_sections(chunks)
    return render_template("index.html", results=results, sections=sections, selected_section=selected_section)

if __name__ == "__main__":
    app.run(debug=True)
