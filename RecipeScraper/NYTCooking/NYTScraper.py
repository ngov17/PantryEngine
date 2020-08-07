from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from RecipeScraper import Recipe

URL = 'https://cooking.nytimes.com/topics/what-to-cook-this-week'
PARSER = 'html5lib'
DELAY = 10
HTML_FOLDER_PATH = './NYTCookingHTML/'


class NYTRecipe(Recipe):
    """
    Class for NYTCooking.
    """
    def __init__(self, link, driver):
        super(NYTRecipe, self).__init__(link, driver)
        self.title = None
        self.ingredients = []

    def scrape(self):
        pass

    def get_recipes_from_page(self, url=None):
        pass

    def get_recipe_neighbors(self):
        pass

