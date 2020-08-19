from elasticsearch import Elasticsearch
from HTMLRecipeParser import HTMLRecipeParser


class RecipeIndexer:
    """
    Class that outlines how the parsed data is organized and indexed based on our data model
    """

    # define our elastic search instance
    es = Elasticsearch([
        {'host': 'localhost', 'port': 9200}
    ])

    """
     conf that customizes elastic's analyzer that configures how we want the ingredients in the recipe_index 
     to be tokenized, filtered, and normalized. Similarly, one for url_index
    """
    recipe_index_conf = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "analyzer_ingredients": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": [
                            "stemmer",
                            "word_delimiter"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "ingredients": {
                    "type": "text",
                    "analyzer": "analyzer_ingredients"
                }
            }
        }
    }

    url_index_conf = {
        "mappings": {
            "properties": {
                "url": {
                    "type": "keyword"
                }
            }
        }

    }

    # Create our indices: url_index and recipe_index. Log to console to ensure success.
    print(es.indices.create("url_index", url_index_conf))
    print(es.indices.create("recipe_index", recipe_index_conf))

    def __init__(self, html_parser_obj: HTMLRecipeParser):
        self.html_string = html_parser_obj.parse_html_string()
        self.url_host = html_parser_obj.parse_url_host()
        self.url = html_parser_obj.parse_url()
        self.title = html_parser_obj.parse_title()
        self.ingredients = html_parser_obj.parse_ingredients()

        query = {
            "query": {
                "match": {
                    "url": {
                        "query": self.url
                    }
                }
            }
        }
        result = self.es.search(query, "url_index")
        self.all_hits = result['hits']['hits']
        # call insert methods to populate the indices only if there are
        # no duplicates
        if (len(self.all_hits) == 0) and (len(self.ingredients) == 0):
            self.insert_url_index(self.url, self.url_host, self.html_string)
            self.insert_recipe_index(self.url, self.title, self.ingredients)

    def insert_url_index(self, url: str, url_host: str, html_string: str):
        """
        :inserts url, url_host, html_string into url_index
        """
        # construct the json object that represents the document
        _doc_url = {
            "url": url,
            "url_host": url_host,
            "html_string": html_string
        }

        # insert the document in the index and log if failed
        print(self.es.index("url_index", _doc_url))

    def insert_recipe_index(self, url: str, title: str, ingredients: [str]):
        """
        :inserts url, recipe, and its ingredients into recipe_index
        """
        _doc_recipe = {
            "url": url,
            "title": title,
            "ingredients": ingredients
        }

        # insert the document in the index and log if failed
        print(self.es.index("recipe_index", _doc_recipe))
