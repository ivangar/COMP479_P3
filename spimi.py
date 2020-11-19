from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
import string
import json
from collections import defaultdict
from collections import OrderedDict
import os

block_size = 0
block = 0
total_docs = 0
total_tokens = 0
doc_lengths = {}
max_block_size = 500


def generate_token_list():
    global total_docs

    sgm_files = PlaintextCorpusReader("reuters", '.*\.sgm')
    hash_dict = defaultdict(list)

    for fileid in sgm_files.fileids():
        f = open("reuters" + '/' + fileid)
        sgm_file = f.read()
        parsed_sgm = BeautifulSoup(sgm_file, 'html.parser')

        for document_text in parsed_sgm.find_all('reuters'):
            spimi_invert(hash_dict, document_text)
            total_docs += 1

    generate_BM25_data()


def spimi_invert(hash_dict, document_text):
    global block_size
    global doc_lengths
    global total_tokens
    doc_id = int(document_text['newid'])
    doc_text = str(document_text.find('text'))
    raw = BeautifulSoup(doc_text, 'html.parser').get_text()
    raw = raw.replace("\u0002", '')
    raw = raw.replace("\u0003", '')
    for c in string.punctuation:
        raw = raw.replace(c, " ")
    tokens = word_tokenize(raw)

    for token in tokens:
        if block_size == max_block_size:
            write_block_to_disk(hash_dict)
            block_size = 0
        block_size += 1
        hash_dict[token].append(doc_id)

    if doc_id == 21578:
        write_block_to_disk(hash_dict)

    doc_lengths[doc_id] = len(tokens)
    total_tokens += len(tokens)


def write_block_to_disk(hash_dict):
    global block
    global max_block_size

    sorted_dict = OrderedDict(sorted(hash_dict.items()))
    file_name = "blocks/Block" + str(block) + ".json"
    with open(file_name, mode="w", encoding="utf-8") as myFile:
        json.dump(sorted_dict, myFile)
    block += 1
    hash_dict.clear()

    if block == 0:
        max_block_size = 500
    else:
        max_block_size = 10000


def merge_blocks():
    inverse_dict = {}
    files = [os.path.join("blocks/", f) for f in os.listdir("blocks")]
    files.sort(key=lambda x: os.path.getmtime(x))

    for filename in files:
        f = open(filename)
        file = f.read()
        d = json.loads(file)
        for k, v in d.items():
            inverse_dict.setdefault(k, []).extend(v)

    with open("files/inverted_index.json", mode="w", encoding="utf-8") as myFile:
        json.dump(inverse_dict, myFile)


def generate_BM25_data():
    length_average = total_tokens/total_docs
    bm25_dict = {"total_docs": total_docs, "length_average": length_average, "doc_lengths": doc_lengths}
    with open("files/bm25_data.json", mode="w", encoding="utf-8") as myFile:
        json.dump(bm25_dict, myFile)


generate_token_list()

merge_blocks()
