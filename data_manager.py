from datetime import datetime
import database_common


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@database_common.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
        SELECT * FROM question;
    ''')
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_last_five_questions(cursor):
    cursor.execute('''
        SELECT message FROM question
        ORDER BY submission_time DESC
        LIMIT 5;
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
def get_single_answer(cursor, id_):
    cursor.execute('''
                    SELECT message FROM answer
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    answer = cursor.fetchone()
    return answer['message']


@database_common.connection_handler
def get_question_id(cursor, id_):
    cursor.execute('''
                    SELECT answer.question_id FROM answer
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    question = cursor.fetchone()
    if question is not None:
        return question['question_id']


@database_common.connection_handler
def get_answer_id(cursor, id_):
    cursor.execute('''
                    SELECT id FROM answer
                    WHERE question_id =%(id_)s;
                    ''',
                   {'id_': id_})
    answer = cursor.fetchone()
    if answer is not None:
        return answer['id']


@database_common.connection_handler
def get_answer_ids(cursor, id_):
    cursor.execute('''
                    SELECT id FROM answer
                    WHERE question_id =%(id_)s;
                    ''',
                   {'id_': id_})
    answer = cursor.fetchall()
    if answer is not None:
        return answer['id']


@database_common.connection_handler
def get_answers_for_questions(cursor, id_):
    cursor.execute('''
        SELECT answer.message, answer.id FROM answer
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
def get_new_answer(cursor, time, question_id, messages):
    cursor.execute('''
        INSERT INTO answer   
        (submission_time, vote_number, question_id, message)
        VALUES (%(time)s, 0, %(question_id)s , %(messages)s);
    ''',
                   {'time': time,
                    'question_id': question_id,
                    'messages': messages})


@database_common.connection_handler
def edit_answer(cursor, time, answer_id, message):
    cursor.execute('''
        UPDATE answer   
        SET message = %(message)s, submission_time = %(time)s
        WHERE id = %(answer_id)s;
    ''',
                   {'time': time,
                    'answer_id': answer_id,
                    'message': message})


@database_common.connection_handler
def delete_question(cursor, id_):
    cursor.execute('''
        DELETE FROM question
        WHERE id = %(id_)s;
    ''',
                   {'id_': id_})


@database_common.connection_handler
def delete_answer(cursor, id_):
    cursor.execute('''
        DELETE FROM answer
        WHERE id = %(id_)s;
    ''',
                   {'id_': id_})


@database_common.connection_handler
def get_all_comment(cursor, id_):
    cursor.execute("""
        SELECT * FROM comment
        WHERE question_id = %(id_)s     
    """,
                   {'id_': id_})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def get_all_answer_comment(cursor, id_):
    cursor.execute("""
        SELECT * FROM comment
        WHERE answer_id = %(id_)s
    """,
                   {'id_': id_})
    return cursor.fetchall()


@database_common.connection_handler
def get_new_comment(cursor, question_id, message, time):
    cursor.execute('''
        INSERT INTO comment   
        (question_id, message, submission_time)
        VALUES (%(question_id)s , %(messages)s, %(time)s);
    ''',
                   {'question_id': question_id,
                    'messages': message,
                    'time': time})


@database_common.connection_handler
def get_new_answer_comment(cursor, answer_id, message, time):
    cursor.execute('''
        INSERT INTO comment   
        (answer_id, message, submission_time)
        VALUES (%(answer_id)s , %(messages)s, %(time)s);
    ''',
                   {'answer_id': answer_id,
                    'messages': message,
                    'time': time})


@database_common.connection_handler
def search_function(cursor, keyword):
    cursor.execute('''
        SELECT * FROM question
        WHERE title LIKE %(keyword)s OR message LIKE %(keyword)s;
    ''',
                   {'keyword': f'%{keyword}%'})
    questions = cursor.fetchall()
    return questions
