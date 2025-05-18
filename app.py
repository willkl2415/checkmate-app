from flask import Flask, render_template, request
from answer_engine import answer_question, load_ingested_chunks

app = Flask(__name__)

# Load chunks once at startup
chunks = load_ingested_chunks()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    keyword = ""
    section = "All Sections"
    detailed = False
    num_results = 0
    document_filter = "All"

    # Get document titles and section titles
    document_titles = sorted(set(chunk.get("source", "Unknown") for chunk in chunks if chunk.get("source")))
    section_titles = sorted(set(chunk.get("section_title", "Unknown") for chunk in chunks if chunk.get("section_title")))

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        keyword = request.form.get("keyword", "").strip()
        section = request.form.get("section", "All Sections")
        detailed = request.form.get("detailed") == "on"
        document_filter = request.form.get("document", "All")

        results = answer_question(
            question=query,
            keyword=keyword,
            section=section,
            detailed=detailed,
            document=document_filter
        )
        num_results = len(results)

    return render_template("index.html",
                           results=results,
                           query=query,
                           keyword=keyword,
                           section=section,
                           detailed=detailed,
                           num_results=num_results,
                           section_options=section_titles,
                           document_filter=document_filter,
                           document_options=document_titles)

if __name__ == "__main__":
    app.run(debug=True)
