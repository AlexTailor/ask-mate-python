from datetime import datetime
from operator import itemgetter
import connection


def sort_by_date():
    questions = connection.get_csv_data('sample_data/question.csv')
    sorted_questions = sorted(questions, key=itemgetter('submission_time'), reverse=True)
    return sorted_questions


def convert_unix_timestamp():
    questions = sort_by_date()
    for question in questions:
        question['submission_time'] = (datetime.utcfromtimestamp(int(question['submission_time'])).strftime('%Y-%m-%d %H:%M:%S'))
    return questions
