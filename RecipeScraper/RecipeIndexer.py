from HTMLRecipeParser import HTMLRecipeParser
from elasticsearch import Elasticsearch


class RecipeIndexer:
    """
    Class that outlines how the parsed data is organized and indexed based on our data model
    """
    # define our elastic search instance
    es = Elasticsearch([
        {'host': 'localhost', 'port': 9200}
    ])

    def __init__(self, html_parser_obj: HTMLRecipeParser):
        self.html_string = html_parser_obj.parse_html_string()
        self.url_host = html_parser_obj.parse_url_host()
        self.url = html_parser_obj.parse_url()
        self.image_url = html_parser_obj.parse_image_url()
        self.title = html_parser_obj.parse_title()
        self.ingredients = html_parser_obj.parse_ingredients()
        self.success = html_parser_obj.success
        self.steps = html_parser_obj.parse_steps()
        self.desc = html_parser_obj.parse_description()
        self.rating = html_parser_obj.parse_agg_rating()
        self.nutrition_info = html_parser_obj.parse_nutrition_info()
        self.author_name = html_parser_obj.parse_author_name()
        self.reviews = html_parser_obj.parse_reviews()

        query = {
            "query": {
                "match": {
                    "url": {
                        "query": self.url
                    }
                }
            }
        }
        # log for errors
        print(self.success)
        result = self.es.search(query, "url_index")
        self.all_hits = result['hits']['hits']
        # call insert methods to populate the indices only if there are
        # no duplicates
        if (len(self.all_hits) == 0) and self.success:
            self.insert_url_index(self.url, self.url_host, self.html_string)
            self.insert_recipe_index(self.url, self.image_url, self.title, self.ingredients, self.steps, self.desc,
                                     self.rating, self.nutrition_info, self.author_name)
        else:
            if len(self.all_hits) > 0:
                print("RECIPE ALREADY IN DATABASE. CRALWER MOVING ON")
            else:
                print("One or more fields are not parsable")

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

    def insert_recipe_index(self, url: str, image_url: str, title: str, ingredients: [str], steps: [str], desc: str,
                            rating: int, nutrition_info: dict, author_name: str):
        """
        :inserts url, recipe, and its ingredients into recipe_index
        """
        _doc_recipe = {
            "url": url,
            "image_url": image_url,
            "title": title,
            "ingredients": ingredients,
            "steps": steps,
            "description": desc,
            "rating": rating,
            "nutrition_info": nutrition_info,
            "author_name": author_name
        }

        # insert the document in the index and log if failed
        print(self.es.index("recipe_index", _doc_recipe))
