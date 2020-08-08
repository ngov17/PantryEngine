from abc import ABC, abstractmethod
from typing import Type
impor

class HTMLRecipeParser:

    """
    The constructor takes in a html file as string
    """
    def __init__(self, html):
        self.html = html

    @abstractmethod
    def parse_html_string(self):
        """
        :returns the entire html file but in string format
        """
        pass

    @abstractmethod
    def parse_URL_host(self):
        """
        :return the URL host. This is important as its unique and will represent the website
         id that represents each page for efficient parsing management if any changes occur
        """
        pass

    @abstractmethod
    def parse_URL(self):
        """
        :return the title from html
        """
        pass

    @abstractmethod
    def parse_title(self):
        """
        :return the title from html
        """
        pass

    @abstractmethod
    def parse_ingredients(self):
        """
        :return list of ingredients (in String) from html
        """
        pass
