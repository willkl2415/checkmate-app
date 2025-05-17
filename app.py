from flask import Flask, request, render_template
import os
from answer_engine import answer_question, get_available_sources

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    total_matches = 0
    source_list = get_available_sources()

    if request.method == 'POST':
        question = request.form['question']
        source_filter = request.form.get('source_filter', '')
        secondary_keyword = request.form.get('secondary_keyword', '')
        detailed_only = 'long_answers' in request.form

        results = answer_question(
            question,
            source=source_filter or None,
            secondary_keyword=secondary_keyword or None,
            detailed_only=detailed_only
        )
        total_matches = len(results)

    return render_template(
        'index.html',
        results=results,
        total_matches=total_matches,
        source_list=source_list
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
