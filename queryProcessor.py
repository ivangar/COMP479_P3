import json
import os.path


def challenge_queries():
    queries = ["pineapple", "Phillippines", "Brierley", "Chrysler"]
    for query in queries:
        postings = search_query(query)
        if not postings:
            continue
        dump_results(query, postings, "files/challengeQueries.json")


def search_query(query):
    f = open("files/naive_indexer.json")
    file = f.read()
    naive_index = json.loads(file)
    doc_ids = []
    lower_case = query.lower()

    for token in naive_index:
        if lower_case == token[0].lower():
            doc_ids.extend(token[1][1])

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


def get_query():
    print("please enter your query (only single term): ")
    query = input()
    terminate = False

    while not terminate:

        while not query or ' ' in query:
            print("please enter your query (only single term): ")
            query = input()

        postings = search_query(query)

        if not postings:
            print("Your query was not found in the index ")
        else:
            print("Your query was found in the following document IDs : ")
            print(*postings, sep=", ")
            dump_results(query, postings, "files/sampleQueries.json")

        print("Do you want to query again? (Y/N) ")
        answer = input()
        if answer.lower() == "n":
            terminate = True
        elif answer.lower() == "y":
            print("please enter your query (only single term): ")
            query = input()


challenge_queries()

get_query()
