from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
import re
import string
import json
import itertools


def generate_token_list():

    # load reuters files with the help of NLTK's PlaintextCorpusReader
    sgm_files = PlaintextCorpusReader("reuters", '.*\.sgm')
    token_list = []
    unsorted_token_list = open("files/unsorted_token_list.txt", 'w')  # use for pretty print the list

    for fileid in sgm_files.fileids():
        f = open("reuters" + '/' + fileid)
        sgm_file = f.read()
        parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')

        for document_text in parsed_sgm.find_all('reuters'):
            block_tokenizer(document_text, token_list, unsorted_token_list)

    with open("files/unsorted_token_list.json", mode="w", encoding="utf-8") as myFile:
        json.dump(token_list, myFile)


def block_tokenizer(document_text, token_list, unsorted_token_list):

    doc_id = int(document_text['newid'])
    doc_text = str(document_text.find('text'))
    raw = BeautifulSoup(doc_text, 'html.parser').get_text()
    raw = raw.replace("\u0002", '')
    raw = raw.replace("\u0003", '')
    for c in string.punctuation:
        raw = raw.replace(c, " ")
    tokens = word_tokenize(raw)
    for token in tokens:
        token_list.append((token, doc_id))
        print(json.dumps([token, doc_id]), file=unsorted_token_list)



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