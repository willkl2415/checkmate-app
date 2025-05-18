from flask import Flask, render_template, request
import json
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

# Load chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    keyword = ""
    secondary_keyword = ""
    selected_source = ""
    detailed = False

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        secondary_keyword = request.form.get("secondary_keyword", "").strip()
        selected_source = request.form.get("source", "")
        detailed = bool(request.form.get("detailed"))

        filtered_chunks = [c for c in chunks if selected_source == "All" or c["source"] == selected_source]
        results = answer_question(
            query=keyword,
            chunks=filtered_chunks,
            secondary_keyword=secondary_keyword,
            detailed=detailed
        )

    sources = get_available_sources(chunks)
    return render_template("index.html", results=results, sources=sources)
