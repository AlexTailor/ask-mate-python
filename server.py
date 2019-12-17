from flask import Flask, render_template, request, redirect, url_for

import connection
import data_manager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def route_index():
    return render_template('index.html')


@app.route('/list')
def list_questions():
    questions = data_manager.get_all_questions()
    print(questions)
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_a_question(question_id):
    answers = data_manager.get_answers_for_questions(question_id)
    question = data_manager.get_single_question(question_id)
    return render_template('question.html', question_id=question_id, answers=answers, question_message=question)


@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'POST':
        titles = request.form.get('title')
        messages = request.form.get('message')
        time = data_manager.get_timestamp()
        data_manager.get_new_question(time, titles, messages)
        return redirect('/list')

    elif request.method == 'GET':
        return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id=int):
    if request.method == 'POST':
        time = data_manager.get_timestamp()
        messages = request.form.get('message')
        data_manager.get_new_answer(time, question_id, messages)

        return redirect(url_for("display_a_question", question_id=question_id))
    return render_template('new-answer.html')


@app.route('/question/<question_id>/delete')
def delete_question(question_id=int):
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id=int):
    answers = connection.get_csv_data('sample_data/answer.csv')
    question_id = None
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer["question_id"]
            answers.remove(answer)
        connection.write_to_file('sample_data/answer.csv', DATA_HEADER2, answers)

    return redirect(url_for("display_a_question", question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
    )
