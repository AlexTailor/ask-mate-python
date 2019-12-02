# Common functions to read/write/append CSV files without feature specific knowledge.
# The layer that have access to any kind of long term data storage. In this case, we use CSV files,
# but later on we'll change this to SQL database. So in the future, we only need to change in this layer.

import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'


def get_csv_data():
    questions = []
    with open(DATA_FILE_PATH, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = dict(row)
            questions.append(question)
    return questions

