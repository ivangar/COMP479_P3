import json
import os.path
import string


def get_content():

    f = open("files/inverted_index.json")
    file = f.read()
    parsed_file = json.loads(file)
    return parsed_file


def search_query(query, operation="single"):
    words = sum([word.strip(string.punctuation).isalpha() for word in query.split()])
    naive_index = get_content()
    sorted_list = []

    if words == 1:
        if query in naive_index:
            doc_ids = naive_index.get(query)
            sorted_list = sorted(doc_ids)

    if words >= 2:
        postings_list = []
        doc_ids = []
        terms = query.split()
        for term in terms:
            postings = search_query(term)
            if not postings:
                continue
            else:
                postings_list.append(postings)
                print(postings)

        if operation == "intersection":
            doc_ids = set(postings_list[0]).intersection(*postings_list)

        if operation == "union":
            doc_ids = set().union(*postings_list)

        sorted_list = sorted(doc_ids)

    return sorted_list


def dump_results(query, postings, output_file):
    q = {query: postings}

    if os.path.isfile(output_file):
        f = open(output_file)
        file = f.read()
        sample_queries = json.loads(file)
        sample_queries.update(q)
        json.dump(sample_queries, open(output_file, "w", encoding="utf-8"), indent=3)
    else:
        json.dump(q, open(output_file, "w", encoding="utf-8"), indent=3)


def get_single_query():
    query = "the"
    postings = search_query(query)
    if not postings:
        print("Your query was not found in the index ")
    else:
        print("Your query was found in the following document IDs : ")
        print(*postings, sep="\n")
        dump_results(query, postings, "files/sampleQueries.json")


def get_intersection_query():
    query = "Cental Soya trction"
    postings = search_query(query, "intersection")
    if not postings:
        print("Your query was not found in the index ")
    else:
        print("Your query was found in the following document IDs : ")
        print(*postings, sep=", ")
        dump_results(query, postings, "files/sampleQueries.json")


def get_union_query():
    query = "ichi Fuju"
    postings = search_query(query, "union")
    if not postings:
        print("Your query was not found in the index ")
    else:
        print("Your query was found in the following document IDs : ")
        print(*postings, sep=", ")
        dump_results(query, postings, "files/sampleQueries.json")


# get_single_query()

get_intersection_query()

# get_union_query()
