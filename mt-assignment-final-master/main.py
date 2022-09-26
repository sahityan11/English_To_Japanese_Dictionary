from common import csv_to_excel, json_to_csv_generator, meanings_folder_path
from words import fetch_words_link
from meaning import merge_meanings, fetch_meanings


json_file_path = meanings_folder_path+'/merged.json'
csv_file_path = 'english_to_japanease.csv'
excel_file_path = 'english_to_japanease.xlsx'

if __name__ == '__main__':
    print('(*) Fetching word links')
    # fetch_words_link()
    print('(+) Done\n(*) Fetching word meanings')
    # fetch_meanings()
    print('(+) Done\n(*) Merging word meanings')
    data = merge_meanings()
    print('(+) Done\n(*) Generating CSV from JSON')
    json_to_csv_generator(json_file_path, csv_file_path)
    print('(+) Done\n(*) Generating XLSX from CSV')
    csv_to_excel(csv_file_path, excel_file_path)
    print('(+) Done')