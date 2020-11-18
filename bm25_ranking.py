import json
import os.path
import string
from math import log10


def get_content(file_name):

    f = open(file_name)
    file = f.read()
    parsed_file = json.loads(file)
    return parsed_file


def search_query(query):
    words = sum([word.strip(string.punctuation).isalpha() for word in query.split()])
    naive_index = get_content("files/inverted_index.json")
    postings_list = {}

    if words == 1:
        if query in naive_index:
            doc_ids = naive_index.get(query)
            postings_list[query] = doc_ids

    if words >= 2:
        terms = query.split()
        for term in terms:
            postings = search_query(term)
            if not postings:
                continue
            else:
                postings_list.update(postings)

    return postings_list


def compute_rankings(query, results):
    terms = query.split()
    bm25_data = get_content("files/bm25_data.json")
    total_docs = bm25_data["total_docs"]
    doc_length_average = bm25_data["length_average"]
    doc_lengths = bm25_data["doc_lengths"]
    doc_ids = set().union(*list(results.values()))
    doc_score = 0
    bm25_rankings = {}

    for doc_id in doc_ids:
        doc_length = doc_lengths[str(doc_id)]

        for term in terms:
            if term in results:
                doc_freq = len(results[term])
                term_freq = results[term].count(doc_id)
                if term_freq > 0:
                    doc_score += compute_bm25_score(total_docs, doc_length_average, doc_length, doc_freq, term_freq)

        print("Doc Id ", doc_id, " score ", doc_score)
        bm25_rankings[doc_id] = doc_score
        doc_score = 0

    return bm25_rankings


def compute_bm25_score(total_docs, doc_length_average, doc_length, doc_freq, term_freq):
    k1 = 0.5
    b = 0.5
    upper = (term_freq * (k1 + 1))
    below = (k1 * ((1 - b) + b * (doc_length / doc_length_average)) + term_freq)
    score = log10((total_docs / doc_freq) * upper / below)
    return score


def get_ranking():
    query = "Jimmy Carter"
    results = search_query(query)
    if not results:
        print("Your query was not found in the index ")
    else:
        print("Your query was found in the following document IDs : ")
        print(results)
        rankings = compute_rankings(query, results)


get_ranking()
