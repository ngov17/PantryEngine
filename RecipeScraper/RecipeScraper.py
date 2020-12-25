from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from validator_collection import validators


class RecipeScraper(ABC):
    """
    TODO: Comments.
    """
    def __init__(self, url,  driver):
        self.driver = driver
        try:
            self.url = validators.url(url)
            self.is_url = True
        except ValueError as exception:
            self.url = None
            self.is_url = False

    @abstractmethod
    def scrape(self):
        """
        This method scrapes the recipe: retrieves html using get_html, calls the parser and indexer
        The html soup object is only extracted only if get_html is not None
        :return a boolean indicating whether the recipe page has been indexed into elasticsearch
        """
        pass

    @abstractmethod
    def get_html(self, driver, url):
        """
        Only gets the HTML soup object from the page if is_recipe_url and is_url are true
        :return: the beautiful soup html object of the page ONLY if is_recipe(url) and is_url are true
                 If this is not the case, None is returned instead
        """
        pass

    @abstractmethod
    def is_recipe_url(self, url):
        """
        :return: boolean true if the url represents a recipe page, false otherwise
        """
        pass

    @abstractmethod
    def get_neighbor_urls(self):
        """
        :return a list of urls that are from the same website (or group of websites for a general scraper)
        """
        pass


