from elasticsearch import Elasticsearch
from urllib.parse import urlparse
"""
Note: This is a dummy file intended to delete all entries in order to repopulate them 
as we test the Scraper and Parser, including test query entries for items that have been 
indexed
"""

es = Elasticsearch([
    {'host': 'localhost', 'port': 9200}
])

query = {
    "query": {
        "match_all": {

        }
    }
}

# Uncomment below lines if data needs to be deleted  in order to re run scraper, parser
print(es.indices.delete("recipe_index"))
print(es.indices.delete("url_index"))
# print(es.get('recipe_index', 'T8EOVXQBFw4EsRIU7aXR'))
# result = es.search(query, "recipe_index")
# all_hits = result['hits']['hits']
#


# # see how many "hits" it returned using the len() function
# print("total hits using 'size' param:", len(result["hits"]["hits"]))
# # iterate the nested dictionaries inside the ["hits"]["hits"] list
# for num, doc in enumerate(all_hits):
#     print("DOC ID:", doc["_id"], "--->", doc, type(doc), "\n")
#
#     # Use 'iteritems()` instead of 'items()' if using Python 2
#     for key, value in doc.items():
#         print(key, "-->", value)
#
#
#     # print a few spaces between each doc for readability
#     print("\n\n")
