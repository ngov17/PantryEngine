from abc import ABC, abstractmethod
from typing import Type


class Recipe:
    """
    TODO
    """
    def __init__(self, link, driver):
        self.link = link
        self.driver = driver

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def get_recipes_from_page(self, url=None):
        """
        :return: List of all recipe URL on page.
        """
        pass

    @staticmethod
    def get_recipe_neighbors():
        """
        From a URL, scrapes all recipes on the cards on the page.
        If a card does not point to a recipe, visits the page and extracts
        all the recipes there.
        :return: Set of neighboring recipe URLs as string
        """
        pass


