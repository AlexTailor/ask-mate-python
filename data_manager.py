from datetime import datetime
import connection
import database_common


def get_timestamp():
    return (datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def get_next_id(file_name):
    data = connection.get_csv_data(file_name)
    return int(data[-1]['id']) + 1


@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
        SELECT * FROM question;
    ''')
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_single_question(cursor, id_):
    cursor.execute('''
                    SELECT message FROM question
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_all_answers(cursor):
    cursor.execute('''
        SELECT * FROM answer;
    ''')
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_answers_for_questions(cursor, id_):
    cursor.execute('''
        SELECT answer.message FROM answer
        INNER JOIN question ON answer.question_id = question.id
        WHERE question_id = %(id_)s;
    ''',
                   {'id_': id_})
    answers_with_question_id = cursor.fetchall()
    return answers_with_question_id


@database_common.connection_handler
def get_new_question(cursor, time, titles, messages):
    cursor.execute('''
        INSERT INTO question   
        (submission_time, view_number, vote_number, title, message)
        VALUES (%(time)s, 0, 0, %(titles)s , %(messages)s);
    ''',
                   {'time': time,
                    'titles': titles,
                    'messages': messages})


@database_common.connection_handler
def delete_question(cursor, id_):
    cursor.execute('''
        DELETE FROM question
        WHERE id = %(id_)s;
    ''',
                   {'id_': id_})
