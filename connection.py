# Common functions to read/write/append CSV files without feature specific knowledge.
# The layer that have access to any kind of long term data storage. In this case, we use CSV files,
# but later on we'll change this to SQL database. So in the future, we only need to change in this layer.

import csv
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER2 = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_csv_data(file_location):
    datas = []
    with open(file_location, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = dict(row)
            datas.append(data)
    return datas


def add_question_to_file(file_location, data):
    with open(file_location, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER)
        writer.writerow(data)


def new_answer_to_file(file_location, data):
    with open(file_location, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=DATA_HEADER2)
        writer.writerow(data)
