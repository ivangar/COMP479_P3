from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
import re
import string
import json
import itertools
from collections import defaultdict


block_size = 0


def generate_token_list():

    # load reuters files with the help of NLTK's PlaintextCorpusReader
    sgm_files = PlaintextCorpusReader("test", '.*\.sgm')
    hash_dict = defaultdict(list)

    for fileid in sgm_files.fileids():
        f = open("test" + '/' + fileid)
        sgm_file = f.read()
        parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')

        for document_text in parsed_sgm.find_all('reuters'):
            spimi_invert(hash_dict, document_text)

    with open("files/unsorted_token_list.json", mode="w", encoding="utf-8") as myFile:
        json.dump(hash_dict, myFile)


def spimi_invert(hash_dict, document_text):

    global block_size
    doc_id = int(document_text['newid'])
    doc_text = str(document_text.find('text'))
    raw = BeautifulSoup(doc_text, 'html.parser').get_text()
    raw = raw.replace("\u0002", '')
    raw = raw.replace("\u0003", '')
    for c in string.punctuation:
        raw = raw.replace(c, " ")
    tokens = word_tokenize(raw)
    for token in tokens:
        if block_size == 500:
            block_size = 0
            #sort terms in dict, write block to file BlockX
            #clean hash_dict, increment file number by 1
            #Continue parsing tokens
        block_size += 1
        hash_dict[token].append(doc_id)


#Use this helper function to test a small amount of data
def test_token_list():

    # load reuters files with the help of NLTK's PlaintextCorpusReader
    sgm_files = PlaintextCorpusReader("reuters", '.*\.sgm')
    token_list = []

    f = open("reuters/reut2-000.sgm")
    sgm_file = f.read()
    parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')
    unsorted_token_list = open("files/unsorted_token_list.txt", 'w') #use for pretty print the list

    for document_text in parsed_sgm.find_all('reuters'):
        doc_id = int(document_text['newid'])
        if doc_id > 4:
            continue
        doc_text = str(document_text.find('text'))
        raw = BeautifulSoup(doc_text, 'html.parser').get_text()
        raw = raw.replace("\u0002", '')
        raw = raw.replace("\u0003", '')
        for c in string.punctuation:
            raw = raw.replace(c, " ")
        raw = re.sub(r"\d", "", raw)
        tokens = word_tokenize(raw)
        for token in tokens:
            token_list.append((token, doc_id))
            print(json.dumps([token, doc_id]), file=unsorted_token_list)

    with open("files/unsorted_token_list.json", mode="w", encoding="utf-8") as myFile:
        json.dump(token_list, myFile)


generate_token_list()

#test_token_list()