from flask import Flask, render_template, request
import json
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

# Load chunks.json at startup
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    total_matches = 0
    sources = get_available_sources(chunks)

    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        source = request.form.get("source", "")
        secondary_keyword = request.form.get("secondary_keyword", "")
        detailed = request.form.get("detailed") == "on"

        results = answer_question(
            keyword=keyword,
            source=source,
            secondary_keyword=secondary_keyword,
            detailed=detailed,
            chunks=chunks
        )
        total_matches = len(results)

    return render_template(
        "index.html",
        results=results,
        total_matches=total_matches,
        sources=sources
    )

if __name__ == "__main__":
    app.run(debug=True)
