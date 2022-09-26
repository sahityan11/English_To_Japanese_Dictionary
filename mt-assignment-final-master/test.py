import os
import requests
import csv
import json
from bs4 import BeautifulSoup


# url_page = 'https://japanesedictionary.org/browse/letter/a/page-2'
# session = requests.Session()
# page = session.get(url_page)
# soup = BeautifulSoup(page.content, 'html.parser')
# entries = soup.find_all('td', {'class': 'english'})
# raw_links = [e.find('a') for e in entries]
# word_links = [(l.text, l['href']) for l in raw_links]
# print(word_links)

# {
#     "bald": [{
#         "type": "enm",
#         "Japanese": ""
#     }, {
#         "type": "enm",
#         "Japanese": ""
#     }],
#     "ball": {
#         "type": "enm",
#         "Japanese": ""
#     }
# }

# session = requests.Session()
# url_pages = ['https://japanesedictionary.org/translate-english/argue',
        # 'https://japanesedictionary.org/translate-english/dry', 'https://japanesedictionary.org/translate-english/yes']
# word_objects = dict()
# for url in url_pages:
    # page = session.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup)
    # word_english = soup.find('td', {'class': 't_english t_data'}).text
    # word_types = [w_type.text for w_type in soup.find_all('td', {'class': 't_type t_data'})]
    # word_japaneses = [w_jap.text for w_jap in soup.find_all('td', {'class': 't_japanese t_data'})]
    # word_hiraganas = [w_hir.text for w_hir in soup.find_all('td', {'class': 't_hiragana t_data'})]
    # word_pronunciations = [w_pro.text for w_pro in soup.find_all('td', {'class': 't_pronunciation t_data'})]
    # word_examples = [(w_ex.find('dt').text, w_ex.find('dd').text)
                     # for w_ex in soup.find_all('td', {'class': 't_sentence t_data'})]
    # word_array = [{'type': wt, 'japanese': wj, 'hirangana': wh, 'pronunciation': wp, 'example_eng': we[0], 'example_jap':we[1]}
                  # for wt, wj, wh, wp, we in zip(word_types, word_japaneses, word_hiraganas, word_pronunciations, word_examples)]
    # word_object = {word_english: word_array}
    # word_objects.update(word_object)

# print(word_objects)
# with open('sample.json', 'w', encoding='utf-8') as outfile:
    # json.dump(word_objects, outfile, indent=4, ensure_ascii=False)


with open('sample.json', 'r', encoding='utf8') as file_json:
    word_objects = json.load(file_json)
    with open('combined.csv', 'w', encoding='utf8') as file_csv:
        field_names = ['english', 'type', 'japanese', 'hirangana', 'pronunciation', 'example_eng', 'example_jap']
        writer = csv.DictWriter(file_csv, delimiter='|', fieldnames=field_names)
        writer.writeheader()
        for word, word_definitions in word_objects.items():
            [writer.writerow({'english': word.replace(' ', '-')+'_'+str(i+1), 'type': wd['type'], 'japanese': wd['japanese'], 'hirangana': wd['hirangana'],
            'pronunciation': wd['pronunciation'],  'example_eng': wd['example_eng'], 'example_jap': wd['example_jap']}) for i, wd in enumerate(word_definitions)]
                  
            
            
