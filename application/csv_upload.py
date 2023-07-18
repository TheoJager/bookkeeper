import csv

from tkinter import filedialog


def csv_to_records(path) -> list:
    list_of_dictionaries = []

    for row in csv.DictReader(open(path, 'r'), delimiter=';'):
        list_of_dictionaries.append({
            'mts_date': row['Transactiedatum'],
            'mts_amount': row['Transactiebedrag'],
            'mts_description': row['Omschrijving'],
            'mts_category': 0
        })

    return list_of_dictionaries


def open_csv_file():
    filename = filedialog.askopenfilename(title='Open CSV File', filetypes=[('CSV Files', '*.csv')])
    return csv_to_records(filename)
