# Common functions to read/write/append CSV files without feature specific knowledge.
# The layer that have access to any kind of long term data storage. In this case, we use CSV files,
# but later on we'll change this to SQL database. So in the future, we only need to change in this layer.

import csv

def get_csv_data(file_location, question_id=None):
    datas = []
    with open(file_location, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = dict(row)
            datas.append(data)
            if question_id is not None and question_id == data['id']:
                return data
    return datas