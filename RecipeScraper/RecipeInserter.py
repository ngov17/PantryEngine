from elasticsearch import Elasticsearch
import hashlib
from HTMLRecipeParser import HTMLRecipeParser

"""
Class that decribes what fields will be added to what indexes in our data model (data_models)
"""
class RecipeInserter:

    """
    Takes in exactly the fields we need based on our data model. T
    """
    def __init__(self, HTMLParserObject ):
        """
        TODO: write intializer according to parser methods in HTMLRecipeParser
        """

    def insert_url_index(self):
        """
        :inserts into url index
        """
        pass


    def insert_recipe_index(self):
        """
        :inserts into index
        """
        pass

    def insert_ingredients_index(self):
        """
        :inserts into index
        """
        pass
