
from flask import Flask, render_template, request
from answer_engine import answer_question, get_available_sources
from ingest import load_ingested_chunks

app = Flask(__name__)
chunks = load_ingested_chunks()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    selected_source = "All"
    secondary_keyword = ""
    detailed_only = False

    if request.method == "POST":
        keyword = request.form["keyword"].strip()
        selected_source = request.form.get("source_filter", "All")
        secondary_keyword = request.form.get("secondary_keyword", "").strip()
        detailed_only = request.form.get("detailed_only") == "on"

        results = answer_question(
            keyword=keyword,
            selected_source=selected_source,
            secondary_keyword=secondary_keyword,
            chunks=chunks,
            detailed_only=detailed_only,
        )

    sources = get_available_sources(chunks)
    return render_template(
        "index.html",
        results=results,
        sources=sources,
        selected_source=selected_source,
        secondary_keyword=secondary_keyword,
        detailed_only=detailed_only
    )

if __name__ == "__main__":
    app.run(debug=True)
