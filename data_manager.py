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
        SELECT title FROM question
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
def get_single_comment(cursor, id_):
    cursor.execute('''
                    SELECT message FROM comment
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    comment = cursor.fetchone()
    return comment['message']


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
def get_answer_id_from_comment(cursor, id_):
    cursor.execute('''
                    SELECT answer_id FROM comment
                    WHERE id =%(id_)s;
                    ''',
                   {'id_': id_})
    comment = cursor.fetchone()
    if comment is not None:
        return comment['answer_id']


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
        SELECT answer.message, answer.id, question_id FROM answer
        INNER JOIN question ON answer.question_id = question.id
        WHERE question_id = %(id_)s;
    ''',
                   {'id_': id_})
    answers_with_question_id = cursor.fetchall()
    return answers_with_question_id


@database_common.connection_handler
def get_new_question(cursor, time, titles, messages, id_):
    cursor.execute('''
        INSERT INTO question   
        (submission_time, view_number, vote_number, title, message, user_id)
        VALUES (%(time)s, 0, 0, %(titles)s , %(messages)s, %(id_)s);
    ''',
                   {'time': time,
                    'titles': titles,
                    'messages': messages,
                    'id_': id_})


@database_common.connection_handler
def get_new_answer(cursor, time, question_id, messages, id_):
    cursor.execute('''
        INSERT INTO answer   
        (submission_time, vote_number, question_id, message, user_id)
        VALUES (%(time)s, 0, %(question_id)s , %(messages)s, %(id_)s);
    ''',
                   {'time': time,
                    'question_id': question_id,
                    'messages': messages,
                    'id_': id_})


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
def edit_comment(cursor, time, id_, message):
    cursor.execute('''
        UPDATE comment   
        SET message = %(message)s, submission_time = %(time)s
        WHERE id = %(id_)s;
    ''',
                   {'time': time,
                    'id_': id_,
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
def delete_comment(cursor, id_):
    cursor.execute('''
        DELETE FROM comment
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
def get_new_comment(cursor, question_id, message, time, id_):
    cursor.execute('''
        INSERT INTO comment   
        (question_id, message, submission_time, user_id)
        VALUES (%(question_id)s , %(messages)s, %(time)s, %(id_)s);
    ''',
                   {'question_id': question_id,
                    'messages': message,
                    'time': time,
                    'id_': id_})


@database_common.connection_handler
def get_new_answer_comment(cursor, answer_id, message, time, id_):
    cursor.execute('''
        INSERT INTO comment   
        (answer_id, message, submission_time, user_id)
        VALUES (%(answer_id)s , %(messages)s, %(time)s, %(id_)s);
    ''',
                   {'answer_id': answer_id,
                    'messages': message,
                    'time': time,
                    'id_': id_})


@database_common.connection_handler
def search_function(cursor, keyword):
    cursor.execute('''
        SELECT * FROM question
        WHERE lower(title) LIKE lower(%(keyword)s) OR lower(message) LIKE lower(%(keyword)s);
    ''',
                   {'keyword': f'%{keyword}%'})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def get_user_registration_data(cursor, username, hashed, time):
    cursor.execute('''
        INSERT INTO user_list (user_name, password, registration_time, reputation)
        VALUES (%(username)s , %(hashed)s, %(time)s, 0);
    ''',
                   {'username': username,
                    'hashed': hashed,
                    'time': time})


@database_common.connection_handler
def get_user_login_data(cursor, username):
    cursor.execute('''
           SELECT password FROM user_list
           WHERE user_name LIKE %(username)s
       ''',
                   {'username': username})
    crypted_password = cursor.fetchone()
    return crypted_password


@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute('''
        SELECT id FROM user_list
        WHERE user_name = %(username)s;
        
    ''',
                   {'username': username})
    user_id = cursor.fetchone()
    return user_id['id']


@database_common.connection_handler
def get_user_id_from_answer(cursor, id_):
    cursor.execute('''
        SELECT user_id FROM answer
        WHERE id = %(id_)s;

    ''',
                   {'id_': id_})
    user_id = cursor.fetchone()
    return user_id['id']


@database_common.connection_handler
def get_user_questions(cursor, id_):
    cursor.execute(''' 
    SELECT id, title FROM question
    WHERE user_id = %(id_)s;
    ''',
                   {'id_': id_})
    userquestions = cursor.fetchall()
    return userquestions


@database_common.connection_handler
def get_user_answers(cursor, id_):
    cursor.execute('''
    SELECT question.id, question.title
    FROM question
    JOIN answer
    ON question.id = answer.question_id
    WHERE answer.user_id = %(id_)s
    GROUP BY question.id, question.title, answer.user_id
    ;
    ''',
                   {'id_': id_})
    useranswers = cursor.fetchall()
    return useranswers


@database_common.connection_handler
def get_user_comments(cursor, id_):
    cursor.execute('''
    SELECT question.id, question.title
    FROM question
    JOIN comment
    ON question.id = comment.question_id
    WHERE comment.user_id = %(id_)s
    GROUP BY question.id, question.title, comment.user_id
    ;
    ''',
                   {'id_': id_})
    usercomments = cursor.fetchall()
    return usercomments


@database_common.connection_handler
def get_reputation(cursor, id_):
    cursor.execute(''' 
    SELECT reputation FROM user_list
    WHERE id = %(id_)s;
    ''',
                   {'id_': id_})
    reputation = cursor.fetchone()
    return reputation['reputation']


@database_common.connection_handler
def get_all_users(cursor):
    cursor.execute(''' 
    SELECT * FROM user_list;
    ''')
    all_users = cursor.fetchall()
    return all_users


# @database_common.connection_handler
# def increase_reputation_on_accepting_answer(cursor, accepted_answer):
#     cursor.execute('''
#     INSERT INTO user_list (reputation)
#     VALUES (reputation + accepted_answer);
#     ''',
#                    {'accepted_answer': accepted_answer})
#     reputation = cursor.fetchall()
#     return reputation
