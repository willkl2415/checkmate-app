from flask import Flask, render_template, request
import json
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

# Load chunks from JSON file
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    keyword = ""
    secondary_keyword = ""
    selected_source = "All"
    detailed_only = False

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        keyword = request.form.get("keyword", "").strip()
        secondary_keyword = request.form.get("secondary_keyword", "").strip()
        selected_source = request.form.get("source", "All")
        detailed_only = request.form.get("detailed_only") == "on"

        filtered_chunks = chunks
        if selected_source != "All":
            filtered_chunks = [chunk for chunk in chunks if chunk["source"] == selected_source]

        results = answer_question(
            query=query,
            chunks=filtered_chunks,
            keyword=keyword,
            secondary_keyword=secondary_keyword,
            detailed_only=detailed_only
        )

    sources = get_available_sources(chunks)
    return render_template("index.html", results=results, sources=sources, query=query,
                           keyword=keyword, secondary_keyword=secondary_keyword,
                           selected_source=selected_source, detailed_only=detailed_only)

if __name__ == "__main__":
    app.run(debug=True)
