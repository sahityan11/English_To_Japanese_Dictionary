import csv
import json
import os
import pandas as pd
from tqdm.std import tqdm


base_url = 'https://japanesedictionary.org'
letter_list = ({'letter': 'a', 'page_count': 38}, {'letter': 'b', 'page_count': 25}, {'letter': 'c', 'page_count': 46}, {'letter': 'd', 'page_count': 25}, {
    'letter': 'e', 'page_count': 19}, {'letter': 'f', 'page_count': 21}, {'letter': 'g', 'page_count': 15}, {'letter': 'h', 'page_count': 17}, {'letter': 'i', 'page_count': 22}, {'letter': 'j', 'page_count': 4}, {'letter': 'k', 'page_count': 3}, {'letter': 'l', 'page_count': 14}, {'letter': 'm', 'page_count': 23}, {'letter': 'n', 'page_count': 9}, {'letter': 'o', 'page_count': 10}, {'letter': 'p', 'page_count': 38}, {'letter': 'q', 'page_count': 3}, {'letter': 'r', 'page_count': 21}, {'letter': 's', 'page_count': 51}, {'letter': 't', 'page_count': 24}, {'letter': 'u', 'page_count': 5}, {'letter': 'v', 'page_count': 8}, {'letter': 'w', 'page_count': 12}, {'letter': 'x', 'page_count': 1}, {'letter': 'y', 'page_count': 2}, {'letter': 'z', 'page_count': 1})
link_folder_path = 'links'
meanings_folder_path = "meanings"


def csv_to_excel(csv_file_path, excel_file_path):
    df = pd.read_csv(csv_file_path, sep="|")
    df = df.sort_values(by=['english'], ascending=True)
    df.to_excel(excel_file_path, index=False)


def get_subfolders(path):
    list_subfolders_path = [
        {'path': f.path, "name": f.name} for f in os.scandir(path) if f.is_dir()]
    return list_subfolders_path


def get_subfiles(path):
    list_subfiles_path = [
        {'path': f.path, 'name': f.name.split('.')[0]} for f in os.scandir(path) if f.is_file()]
    return list_subfiles_path


def json_to_csv_generator(json_file_path, csv_file_path):
    with open(json_file_path, 'r', encoding='utf8') as file_json:
        word_objects = json.load(file_json)
        hindi_concept_pair = get_english_word_hindi_concept(
            "H_concept-to-mrs-rels.dat")
        hindi_words = hindi_concept_pair['hindi_words']
        english_words = hindi_concept_pair['english_words']
        english_hindi_mapping = generate_english_hindi_map(
            hindi_words, english_words)

        with open(csv_file_path, 'w', encoding='utf8') as file_csv:
            field_names = ['english', 'hindi', 'type', 'pronunciation']
            writer = csv.DictWriter(
                file_csv, delimiter='|', fieldnames=field_names)
            writer.writeheader()

            english_hindi_pronounciation = dict(english_hindi_mapping)
            for hindi_english_word in english_hindi_mapping:
                # hindi_word = hindi_english_word.split("#")[1]
                pos = hindi_english_word.split("#")[0].split("_")[1]
                english_word = hindi_english_word.split("#")[0].split("_")[0]
                if english_word in word_objects:
                    word_definition = word_objects[english_word.split("#")[0]]
                    for element in word_definition:
                        if element['type'] == pos:
                            if hindi_english_word in english_hindi_pronounciation:
                                english_hindi_pronounciation[hindi_english_word].append(
                                    element['pronunciation'])
                            else:
                                english_hindi_pronounciation[hindi_english_word] = [
                                    element['pronunciation']]

            hindi_word_count = {}
            english_word_count = {}

            for word, pronunciation in tqdm(english_hindi_pronounciation.items()):
                hindi_word = word.split("#")[1]
                pos = word.split("#")[0].split("_")[1]
                english_word = word.split("#")[0].split("_")[0]
                concated_pronunciation = ''
                for element in pronunciation:
                    concated_pronunciation = concated_pronunciation+element+','
                concated_pronunciation = concated_pronunciation[:-1]

                if hindi_word in hindi_word_count:
                    hindi_word_count[hindi_word] += 1
                else:
                    hindi_word_count[hindi_word] = 1

                if english_word in english_word_count:
                    english_word_count[english_word] += 1
                else:
                    english_word_count[english_word] = 1

                writer.writerow({'english': english_word+'_'+str(english_word_count[english_word]), 'hindi': hindi_word+'_'+str(
                    hindi_word_count[hindi_word]), 'type': pos, 'pronunciation': concated_pronunciation})


def generate_english_hindi_map(hindi_words, english_words):
    english_hindi_mapping = {}
    for word, hindi_meanings in english_words.items():
        for i, hindi_word in enumerate(hindi_meanings):
            english_hindi_mapping[word+"#"+hindi_word] = []
    for word, english_meanings in hindi_words.items():
        for i, english_word in enumerate(english_meanings):
            english_hindi_mapping[english_word+"#"+word] = []
    return english_hindi_mapping


def get_english_word_hindi_concept(h_concept_file_path):
    with open(h_concept_file_path, 'r') as file:
        english_words = {}
        hindi_words = {}
        for index, line in enumerate(file):
            h_concept = line.rstrip()
            try:
                h_concept = h_concept.split()
                hindi_word = h_concept[1].split('_')[0]
                english_word = h_concept[2].split('_')[0]
                pos = h_concept[3].split('_')[2]
                english_word_pos = english_word+"_"+extractPos(pos)
                if english_word_pos in english_words:
                    english_words[english_word_pos].append(hindi_word)
                else:
                    english_words[english_word_pos] = [hindi_word]
                if hindi_word in hindi_words:
                    hindi_words[hindi_word].append(english_word_pos)
                else:
                    hindi_words[hindi_word] = [english_word_pos]
            except:
                pass
                # print("skipping line number:", index+1,
                #       h_concept, " not able to parse")

        return {'hindi_words': hindi_words, 'english_words': english_words}


def extractPos(pos):
    if pos == 'v':
        return "verb"
    elif pos == 'a':
        return "adjective"
    elif pos == 'n':
        return "noun"
    elif pos == 'x':
        return "noun"
    elif pos == 'c':
        return "noun"
    elif pos == 'of':
        return "noun"
    elif pos == 'u':
        return "noun"
    elif pos == 'q':
        return "noun"
    elif pos == 'p':
        return "preposition"
    else:
        return ""
