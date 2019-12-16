# Common functions to read/write/append CSV files without feature specific knowledge.
# The layer that have access to any kind of long term data storage. In this case, we use CSV files,
# but later on we'll change this to SQL database. So in the future, we only need to change in this layer.

import csv


def get_csv_data(file_location):
    datas = []
    with open(file_location, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data = dict(row)
            datas.append(data)
    return datas


def add_to_file(file_location, header, data):
    with open(file_location, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerow(data)


def write_to_file(file_location, header,data):
    with open(file_location, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def update_question(file_location, data):
    add_to_file(file_location, data)
