import json
import string
from math import log10
from tabulate import tabulate
import random

b = random.uniform(0, 1)
k1 = random.choice([1.2, 2])


def get_content(file_name):

    f = open(file_name)
    file = f.read()
    parsed_file = json.loads(file)
    return parsed_file


def search_query(query):
    words = sum([word.strip(string.punctuation).isalpha() for word in query.split()])
    spimi_index = get_content("files/inverted_index.json")
    postings_list = {}

    if words == 1:
        for c in string.punctuation:
            query = query.replace(c, "")
        if query in spimi_index:
            doc_ids = spimi_index.get(query)
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

        bm25_rankings[doc_id] = doc_score
        doc_score = 0

    return bm25_rankings


def compute_bm25_score(total_docs, doc_length_average, doc_length, doc_freq, term_freq):
    return log10((total_docs / doc_freq) * (term_freq * (k1 + 1)) / (k1 * ((1 - b) + b * (doc_length / doc_length_average)) + term_freq))


def get_ranking():
    query = "Drug company bankruptcies"
    results = search_query(query)
    if not results:
        print("\nYour query [", query, "] was not found in the index ")
    else:
        rankings = compute_rankings(query, results)
        sorted_rankings = sorted(rankings.items(), key=lambda item: item[1], reverse=True)
        print("\nRankings of the query [", query, "]\n")
        print(tabulate(sorted_rankings, headers=["Document ID", "Ranking"], numalign="left", floatfmt=".6f", tablefmt="github"))


get_ranking()
