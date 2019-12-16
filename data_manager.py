from datetime import datetime
import time
from operator import itemgetter

import psycopg2

import connection
import database_common


def sort_by_date():
    questions = connection.get_csv_data('sample_data/question.csv')
    sorted_questions = sorted(questions, key=itemgetter('submission_time'), reverse=True)
    return sorted_questions
    # return render_template('list.html', questions=questions)


def convert_unix_timestamp():
    questions = sort_by_date()
    for question in questions:
        question['submission_time'] = (
            datetime.utcfromtimestamp(int(question['submission_time'])).strftime('%Y-%m-%d %H:%M:%S'))
    return questions


def get_timestamp():
    return int(time.time())


def get_next_id(file_name):
    data = connection.get_csv_data(file_name)
    return int(data[-1]['id']) + 1


@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
        SELECT * FROM question
    ''')
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_all_answers(cursor):
    cursor.execute('''
        SELECT * FROM answer
    ''')
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_answers_for_questions(cursor):
    cursor.execute('''
        SELECT answer.message FROM answer
        INNER JOIN question ON answer.question_id = question.id
    ''')
    answers_with_question_id = cursor.fetchall()
    return answers_with_question_id
