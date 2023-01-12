
import csv

with open('data-398-2018-08-30.csv', newline='', encoding='utf-8') as data_file:
    reader = csv.DictReader(data_file)
    data_list = []
    for row in reader:
        stop_dict = {'Name': row['Name'], 'Street': row['Street'], "District": row['District']}
        data_list.append(stop_dict)
