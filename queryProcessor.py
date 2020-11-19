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
    spimi_index = get_content()
    sorted_list = []

    if words == 1:
        for c in string.punctuation:
            query = query.replace(c, "")
        if query in spimi_index:
            doc_ids = spimi_index.get(query)
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


def dump_postings(query, postings):
    if not postings:
        print("Your query [", query, "] was not found in the index ")
    else:
        print("Your query [", query, "] was found in the following document IDs : ")
        print(*postings, sep="\n")
        dump_results(query, postings, "files/sampleQueries.json")


def sample_queries():
    # Search for a single term query
    postings = search_query("George", "single")
    dump_postings("George", postings)

    # a) This sentence should return all the documents that contain any query term
    postings = search_query("Democrats' welfare and healthcare reform policies", "union")
    dump_postings("Democrats' welfare and healthcare reform policies", postings)

    # c) George Bush is a full name, so it should intersect both query results (AND)
    postings = search_query("George Bush", "intersection")
    dump_postings("George Bush", postings)

    # b) This sentence should return results with any of it's terms (OR)
    postings = search_query("Drug company bankruptcies", "union")
    dump_postings("Drug company bankruptcies", postings)


sample_queries()


