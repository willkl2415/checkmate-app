from flask import Flask, render_template, request
import json
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

# Load the preprocessed chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    source_filter = "All"
    secondary_keyword = ""
    detailed = False

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        source_filter = request.form.get("source_filter", "All")
        secondary_keyword = request.form.get("secondary_keyword", "").strip()
        detailed = request.form.get("detailed") == "on"

        results = answer_question(
            chunks=chunks,
            query=query,
            source_filter=source_filter,
            secondary_keyword=secondary_keyword,
            detailed=detailed
        )

    sources = get_available_sources(chunks)
    return render_template("index.html", results=results, sources=sources, query=query,
                           source_filter=source_filter, secondary_keyword=secondary_keyword,
                           detailed=detailed)
