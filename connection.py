# Common functions to read/write/append CSV files without feature specific knowledge.
# The layer that have access to any kind of long term data storage. In this case, we use CSV files,
# but later on we'll change this to SQL database. So in the future, we only need to change in this layer.

import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH2 = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'

def get_csv_data(question_id=None):
    questions = []
    with open(DATA_FILE_PATH, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = dict(row)
            questions.append(question)
            if question_id is not None and question_id == question['id']:
                return question
    return questions

def get_csv_data2(question_id=None):
    answers = []
    with open(DATA_FILE_PATH2, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            answer = dict(row)
            answers.append(answer)
            if question_id is not None and question_id == answer['id']:
                return answer
    return answers

