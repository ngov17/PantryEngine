from abc import ABC, abstractmethod
from typing import Type


class RecipeScraper(ABC):
    """
    TODO: Comments.
    """
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def scrape(self):
        """
        :return: html object (BeautifulSoup Object)
        """
        pass

    @abstractmethod
    def get_recipes_from_page(self, url=None):
        """
        :return: List of all recipe URLs directly linked to on page.
        """
        pass

    @abstractmethod
    def get_recipe_neighbors(self):
        """
        Scrapes all 'recipe neighbors' on a page, e.g. scrapes recipes on non-recipe pages that the page points to.
        For example, if a page links to multiple compilations, gets the recipes from those as direct recipe neighbors.
        :return: Set of neighboring recipe URLs as string
        """
        pass


