from nltk import word_tokenize
from bs4 import BeautifulSoup
from nltk.corpus import PlaintextCorpusReader
import string
import json
from collections import defaultdict
from collections import OrderedDict
import collections
import os

block_size = 0
block = 0


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
            write_block_to_disk(hash_dict)
            block_size = 0
        block_size += 1
        hash_dict[token].append(doc_id)

    if doc_id == 21578:
        write_block_to_disk(hash_dict)


# sort terms in dict, write block to file BlockX
# clear hash_dict, increment file number by 1
def write_block_to_disk(hash_dict):
    global block
    sorted_dict = OrderedDict(sorted(hash_dict.items()))
    # file_name = "blocks/Block" + str(block) + ".json"
    file_name = "testBlocks/Block" + str(block) + ".json"
    with open(file_name, mode="w", encoding="utf-8") as myFile:
        json.dump(sorted_dict, myFile)
    block += 1
    hash_dict.clear()


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


#generate_token_list()

merge_blocks()
