# generates an Anki deck of multiplication table from 2 to 20

import csv

csv_file = open('CSVs/mult_table.csv',
                'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)


def write_to_csv(a, b):

    question = f'{a} * {b}'

    answer = f'{a * b}'

    csv_writer.writerow([question, answer])


for i in range(2, 21):

    for j in range(i, 21):

        write_to_csv(i, j)
