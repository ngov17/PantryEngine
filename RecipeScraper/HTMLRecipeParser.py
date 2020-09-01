from abc import ABC, abstractmethod
from typing import Type
from bs4 import BeautifulSoup

"""
Abstract class the defines the parser 
"""


class HTMLRecipeParser(ABC):
    """
    The constructor takes in a html file as string
    """

    def __init__(self, html: BeautifulSoup, url):
        """
        :param html: BeautifulSoup object of webpage
        """
        self.html = html
        self.url = url
        self.success = True

    """
    NOTE: REQUIRED indicates that the particular field being parsed is needed and failing to parse
          that field will result in success = False. NOT REQUIRED indicates the field being parsed is
          not essential and if data cannot be found in the html file success still remains True and 
          a dummy value will be returned for the filed (eg: an empty list, or empty string);
    """

    @abstractmethod
    def parse_html_string(self):
        """
        :returns the entire html file but in string format
        :REQUIRED.
        """
        pass

    @abstractmethod
    def parse_url_host(self):
        """
        :return the URL host. This is important as its unique and will represent the website
         id that represents each page for efficient parsing management if any changes occur
        :REQUIRED
        """
        pass

    @abstractmethod
    def parse_url(self):
        """
        :return the url from html
        :REQUIRED
        """
        pass

    @abstractmethod
    def parse_image_url(self):
        """
        :return the image url from html
        : NOT REQUIRED ( a dummy image will be filled instead)
        """
        pass

    @abstractmethod
    def parse_title(self):
        """
        :return the title from html
        : REQUIRED
        """
        pass

    @abstractmethod
    def parse_ingredients(self):
        """
        :return list of ingredients (in String) from html
        :REQUIRED
        """
        pass

    @abstractmethod
    def parse_steps(self):
        """
        :return list of steps to make the recipe
        :REQUIRED
        """
        pass

    @abstractmethod
    def parse_agg_rating(self):
        """
        :return a float between 0 and 1 representing the rating (will be displayed in an interactive manner)
        :NOT REQUIRED
        """
        pass

    @abstractmethod
    def parse_nutrition_info(self):
        """
        :return dict object containing key nutrition info like calories, protein, fat etc.
        :NOT REQUIRED
        """
        pass

    @abstractmethod
    def parse_author_name(self):
        """
        :return author's name as string
        :REQUIRED (for copyright purposes)
        """
        pass

    @abstractmethod
    def parse_reviews(self):
        """
        :return a list of reviews for nlp analysis (sentiment analysis and ratings analysis)
        NOT REQUIRED
        """
        pass

    @abstractmethod
    def parse_description(self):
        """
        :return the shorthand description of the recipe as string
        : NOT REQUIRED (try finding websites that have this, as it is really useful
                        info for further nlp analysis)
        """
        pass
