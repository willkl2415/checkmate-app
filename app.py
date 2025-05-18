from flask import Flask, render_template, request
import json
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    selected_source = ""
    query = ""
    secondary_keyword = ""

    if request.method == "POST":
        selected_source = request.form.get("source", "")
        query = request.form.get("query", "")
        secondary_keyword = request.form.get("secondary_keyword", "")

        filtered_chunks = [chunk for chunk in chunks if chunk["source"] == selected_source] if selected_source else chunks
        results = answer_question(filtered_chunks, query, secondary_keyword)

    sources = get_available_sources()
    return render_template("index.html", results=results, sources=sources, selected_source=selected_source, query=query, secondary_keyword=secondary_keyword)

if __name__ == "__main__":
    app.run(debug=True)
