from flask import Flask, render_template, request
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    total_matches = 0

    if request.method == "POST":
        question = request.form["question"]
        source = request.form.get("source", "all")
        secondary = request.form.get("secondary", "")
        detailed = request.form.get("detailed") == "on"

        results = answer_question(
            question,
            source=source,
            secondary=secondary,
            detailed=detailed
        )
        total_matches = len(results)

    sources = get_available_sources()
    return render_template("index.html", results=results, total_matches=total_matches, sources=sources)

