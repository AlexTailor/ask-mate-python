from flask import Flask, render_template, request, redirect, url_for
import data_manager
import hashing

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def route_index():
    last_five_questions = data_manager.get_last_five_questions()
    return render_template('index.html', last_five_questions=last_five_questions)


@app.route('/list')
def list_questions():
    questions = data_manager.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def display_a_question(question_id):
    question = data_manager.get_single_question(question_id)
    answer_id = []
    answers = data_manager.get_answers_for_questions(question_id)
    answercomments = []
    for answer in answers:
        answer_id.append(answer['id'])
    for id in answer_id:
        answercomments.append(data_manager.get_all_answer_comment(id))

    comments = data_manager.get_all_comment(question_id)
    return render_template('question.html', question_id=question_id, answer_id=answer_id, answers=answers,
                           question_message=question, comments=comments, answercomments=answercomments)


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


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id=int):
    if request.method == 'POST':
        message = request.form.get('message')
        time = data_manager.get_timestamp()
        data_manager.get_new_comment(question_id, message, time)
        return redirect(url_for("display_a_question", question_id=question_id))
    return render_template('new-comment.html')


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id=int):
    question_id = data_manager.get_question_id(answer_id)
    if request.method == 'POST':
        message = request.form.get('message')
        time = data_manager.get_timestamp()
        data_manager.get_new_answer_comment(answer_id, message, time)
        return redirect(url_for('display_a_question', question_id=question_id))
    return render_template('new-comment.html')


@app.route('/question/<question_id>/delete')
def delete_question(question_id=int):
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id=int):
    question_id = data_manager.get_question_id(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id=int):
    question_id = data_manager.get_question_id(answer_id)
    answer_message = data_manager.get_single_answer(answer_id)
    if request.method == 'POST':
        message = request.form.get('message')
        time = data_manager.get_timestamp()
        data_manager.edit_answer(time, answer_id, message)
        return redirect(url_for('display_a_question', question_id=question_id))
    return render_template('new-answer.html', answer_message=answer_message)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_phrase = request.args.get('search')
    questions = data_manager.search_function(search_phrase)
    return render_template('list.html', questions=questions)


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id=int):
    answer_id = data_manager.get_answer_id_from_comment(comment_id)
    question_id = data_manager.get_question_id(answer_id)

    data_manager.delete_comment(comment_id)
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id=int):
    answer_id = data_manager.get_answer_id_from_comment(comment_id)
    question_id = data_manager.get_question_id(answer_id)

    comment_message = data_manager.get_single_comment(comment_id)
    if request.method == 'POST':
        message = request.form.get('message')
        time = data_manager.get_timestamp()
        data_manager.edit_comment(time, comment_id, message)
        return redirect(url_for('display_a_question', question_id=question_id))
    return render_template('new-comment.html', comment_message=comment_message)


@app.route('/registration', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed = hashing.hash_password(password)
        time = data_manager.get_timestamp()
        data_manager.get_user_registration_data(username, hashed, time)
        return redirect('/list')
    return render_template('registration.html')


@app.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = data_manager.get_user_login_data(username)
        verification = hashing.verify_password(password, hashed_password)
    return render_template('index.html', verification=verification)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )
