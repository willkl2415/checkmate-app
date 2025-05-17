from flask import Flask, request, render_template
import os
from answer_engine import answer_question

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    total_matches = 0
    if request.method == 'POST':
        question = request.form['question']
        source_filter = request.form.get('source_filter', '')
        secondary_keyword = request.form.get('secondary_keyword', '')
        min_length = 80 if 'long_answers' in request.form else 0

        results, total_matches = answer_question(
            question,
            source_filter=source_filter,
            secondary_keyword=secondary_keyword,
            min_length=min_length
        )

    return render_template('index.html', results=results, total_matches=total_matches)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
