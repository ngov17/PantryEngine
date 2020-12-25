from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from RecipeScraper import RecipeScraper
from GeneralRecipeSite.GeneralParser import GeneralParser
from RecipeIndexer import RecipeIndexer
from urllib.parse import urlparse

PARSER = 'html5lib'
DELAY = 10

"""
FUNCTIONS
"""


def wait_method(driver):
    """
    This function describes the wait method required by wait.until in get_html
    Defines the expected condition for how long the selenium driver should wait
        in get_html in General Scraper
    """
    all_scripts = driver.find_elements_by_css_selector('script[type="application/ld+json"]')
    return not len(all_scripts) == 0


class GeneralScraper(RecipeScraper):
    def __init__(self, url, driver):
        super(GeneralScraper, self).__init__(url, driver)
        self.html = self.get_html(self.driver, self.url)

    def is_recipe_url(self, url: str):
        # true if the url meets the criteria for the set of websites
        return ((url.startswith('https://tasty.co/'))
                or (url.startswith('https://www.foodnetwork.com/'))
                or (url.startswith('https://www.food.com/'))) \
               and (('recipe' in url)
                    or ('compilation' in url)
                    or ('package' in url)
                    or ('photo' in url)
                    or ('topic' in url)
                    or ('idea' in url)
                    or ('collection' in url))

    def get_html(self, driver, url):
        if self.is_url:
            # Open the URL using driver
            driver.get(url)
            # Wait object
            wait = WebDriverWait(driver, DELAY)
            # Scroll down to bottom for feed to load on website.
            driver.execute_script("window.scrollTo(0, 0.5 * document.body.scrollHeight);")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait until specific elements are available
            try:
                wait.until(wait_method)
            except TimeoutException:
                print(f"Driver timed out on {url}")
            # Create soup object
            soup = BeautifulSoup(driver.page_source, features=PARSER)
            return soup
        else:
            return None

    def scrape(self):
        if self.html is not None:
            # call parser and indexer on self.html
            parser = GeneralParser(self.html, self.url)
            # index the recipe if parser.success
            if parser.success:
                print(parser.parse_description())
                indexer = RecipeIndexer(parser)
                return indexer.is_indexed
            else:
                return False
        else:
            return False

    def get_neighbor_urls(self):
        if self.html is not None:
            all_urls = [attribute.get('href') for attribute in self.html.find_all("a")]
            neighbor_urls = []
            print(all_urls)
            for url in all_urls:
                if url is not None:
                    # normalize the urls
                    # 1: if it starts with '/', its mostly relative:
                    if 'http' not in url and url.startswith('//'):
                        url = 'https:' + url
                    elif url.startswith('/'):
                        url = 'https://' + urlparse(self.url).hostname + "/" + url
                    # only add url if it is a recipe or compilation url
                    if self.is_recipe_url(url):
                        neighbor_urls.append(url)
            return neighbor_urls
        else:
            return []
