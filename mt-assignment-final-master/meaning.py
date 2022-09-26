import json
import os
import shutil
from typing import ChainMap
import pandas as pd
import requests
import multiprocessing as mp
from tqdm import tqdm
from bs4 import BeautifulSoup
from common import link_folder_path, get_subfolders, base_url, get_subfiles, meanings_folder_path


def write_to_json(object, file_path):
    with open(file_path+".json", "w+", encoding='utf-8') as outfile:
        json.dump(object, outfile, indent=4, ensure_ascii=False)


def get_words_url(file):
    with open(file['path']) as file:
        lines = [line.strip() for line in file.readlines()]
        return lines


def fetch_meaning_from_url(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    word_english = soup.find('td', {'class': 't_english t_data'}).text
    word_types = [w_type.text for w_type in soup.find_all('td', {'class': 't_type t_data'})]
    word_japaneses = [w_jap.text for w_jap in soup.find_all('td', {'class': 't_japanese t_data'})]
    word_hiraganas = [w_hir.text for w_hir in soup.find_all('td', {'class': 't_hiragana t_data'})]
    word_pronunciations = [w_pro.text for w_pro in soup.find_all('td', {'class': 't_pronunciation t_data'})]
    word_examples = [(w_ex.find('dt').text, w_ex.find('dd').text)
                     for w_ex in soup.find_all('td', {'class': 't_sentence t_data'})]
    word_array = [{'type': wt, 'japanese': wj, 'hirangana': wh, 'pronunciation': wp, 'example_eng': we[0], 'example_jap':we[1]}
                  for wt, wj, wh, wp, we in zip(word_types, word_japaneses, word_hiraganas, word_pronunciations, word_examples)]
    word_object = {word_english: word_array}
    return word_object


def worker(words_folder):
    session = requests.Session()
    words_folder_path = words_folder["path"]
    words_folder_name = words_folder["name"]
    files = get_subfiles(words_folder_path)

    parent_folder = meanings_folder_path+"/" + words_folder_name
    os.mkdir(parent_folder)
    for file in tqdm(files):
        words_url = get_words_url(file)
        meanings = {}
        for url in words_url:
            meaning = fetch_meaning_from_url(base_url+url, session)
            meanings.update(meaning)
        write_to_json(meanings, parent_folder+"/"+file['name'])


def fetch_meanings():
    path = meanings_folder_path
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
    p = mp.Pool(26)
    words_folders = get_subfolders(link_folder_path)
    p.map(worker, words_folders)
    p.close()
    p.join()


def read_meaning_json_file(words_folders):
    files = get_subfiles(words_folders['path'])
    meanings = []
    for file in files:
        with open(file['path'], encoding='utf-8') as opened_file:
            meaning = json.loads(opened_file.read())
            meanings.append(meaning)

    meanings = dict(ChainMap(*meanings))

    write_to_json(object=meanings, file_path=words_folders['path']+"/merged")

    return meanings


def merge_meanings():
    p = mp.Pool(26)
    words_folders = get_subfolders(meanings_folder_path)
    meanings = p.map(read_meaning_json_file, words_folders)
    merged_meanings = dict(ChainMap(*meanings))
    write_to_json(object=merged_meanings,
                  file_path=meanings_folder_path+"/merged")
    p.close()
    p.join()
    return merged_meanings