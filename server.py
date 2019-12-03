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
    question = connection.get_csv_data('sample_data/question.csv', question_id)
    answers = connection.get_csv_data('sample_data/answer.csv', question_id)
    print(answers)
    return render_template('question.html', id = question["id"] , question_title = question["title"],
                           answer = answers["message"])


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    return render_template('add-question.html')


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )
