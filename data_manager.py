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
def get_single_question(cursor, id_):
    cursor.execute('''
                    SELECT message FROM question
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_question_id(cursor, id_):
    cursor.execute('''
                    SELECT question_id FROM answer
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    question = cursor.fetchone()
    print(question)
    return question['question_id']


@database_common.connection_handler
def get_answer_id(cursor, id_):
    cursor.execute('''
                    SELECT answer.id FROM answer
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    answer = cursor.fetchall()
    print(answer)
    return answer


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
