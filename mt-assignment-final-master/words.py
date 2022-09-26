import os
import shutil
import requests
import multiprocessing as mp
from tqdm import tqdm
from bs4 import BeautifulSoup
from common import base_url, letter_list, link_folder_path


page_url = base_url+'/browse/letter/{letter}/page-{page_number}'
letter_links_folder_path = (link_folder_path+'/{letter_name}')


def worker(work_data):
    session = requests.Session()
    letter_name = work_data['letter']
    parent_folder = letter_links_folder_path.format(letter_name=letter_name)
    os.mkdir(parent_folder)
    for page_number in tqdm(range(int(work_data['page_count']))):
        fetch_letters(page_number, letter_name, parent_folder, session)


def fetch_letters(page_number, letter_name, parent_folder, session):
    file_path = '{parent_folder_name}/{page_number}.txt'.format(
        page_number=page_number+1, parent_folder_name=parent_folder)
    url = page_url.format(letter=letter_name, page_number=page_number+1)
    with open(file_path, 'w+') as file:
        page = session.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        entries = soup.find_all('td', {'class': 'english'})
        raw_links = [e.find('a') for e in entries]
        word_links = [(l.text, l['href']) for l in raw_links]
        [file.write(wl[1]+'\n') for wl in word_links]


def fetch_words_link():
    path = link_folder_path
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)
    p = mp.Pool(26)
    p.map(worker, letter_list)
    p.close()
    p.join()
