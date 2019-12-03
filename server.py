from flask import Flask, render_template, request, redirect, url_for

import connection
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def route_index():
    return render_template('index.html')


@app.route('/list', methods=['GET', 'POST'])
def list_questions():
    questions = data_manager.convert_unix_timestamp()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_a_question(question_id=int):
    items_with_id = []
    question = connection.get_csv_data('sample_data/question.csv')
    answers = connection.get_csv_data('sample_data/answer.csv')
    for i in answers:
        if i['question_id'] == question_id:
            items_with_id.append(i)
    print(items_with_id)
    return render_template('question.html', answers=items_with_id)


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'POST':
        question = {
            'id': data_manager.get_next_id(),
            'submission_time': data_manager.get_timestamp(),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': '-'
        }
        connection.add_question_to_file('sample_data/question.csv', question)
        return redirect('/list')
    return render_template('add-question.html')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )
