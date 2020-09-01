from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from RecipeScraper import RecipeScraper
from FoodNetwork.FoodNetworkParser import FoodNetworkParser
from RecipeIndexer import RecipeIndexer

URL = 'https://foodnetwork.com/'
PARSER = 'html5lib'
DELAY = 10


class FoodNetworkScraper(RecipeScraper):
    """
    Recipe subclass for foodnetwork.com
    """

    def __init__(self, link, driver):
        super(FoodNetworkScraper, self).__init__(driver)
        self.link = link
        self.title: str
        self.title = None
        self.html: BeautifulSoup
        self.html = None
        self.visited = False
        self.id: str
        self.id = None
        self.ingredients = []

    def scrape(self):
        """
        TODO: Comments.
        :return:
        """
        # Scrape soup into self.html using link.
        self.html = get_soup(self.link, self.driver)
        # we parse and index each recipe as it is scraped in function scrape()
        # so we create instances of our parser
        parser = FoodNetworkParser(self.html, self.link)
        # call our indexer whose init method indexes this particular html page based on parser
        # this essentially fills in the data into elastic search for this page
        # RecipeIndexer(parser)
        print(parser.parse_image_url())
        print(parser.parse_title())
        print(parser.parse_ingredients())
        print(parser.parse_steps())
        print(parser.parse_agg_rating())
        return self.html

    def get_recipes_from_page(self, url=None):
        """
        # TODO: Comments.
        :param url:
        :return:
        """
        if url is not None:
            soup = get_soup(('https://' + url.replace('//', '')), driver=self.driver)
        elif self.html is None:
            self.scrape()
            soup = self.html
        else:
            soup = self.html

        all_urls = [attribute.get('href') for attribute in soup.find_all("a")]
        recipe_urls = [('https://' + url.replace('//', '')) for url in all_urls if _is_url_recipe(url)]
        print(recipe_urls)
        return recipe_urls

    def get_recipe_neighbors(self):
        """
        # TODO: Comments.
        :return:
        """
        soup = self.html
        # Scrape class=recipe
        #   class = result__image-link href
        links = [attribute.get('href') for attribute in soup.find_all("a")]
        print(links)
        to_return = []
        recipes = self.get_recipes_from_page()
        to_return.extend(recipes)
        # Iterate over all card links, and if the link is not a recipe,
        # visits the page and gets the recipes featured there.
        for link in links:
            # If it's not recipe, we scrape all of it for recipes.
            if _is_url_compilation(link):
                recipes_from_compilation = self.get_recipes_from_page(url=link)
                to_return.extend(recipes_from_compilation)
        print(to_return)
        return to_return


def get_soup(url, driver):
    """
    :param driver: Selenium driver in order to scrape dynamic pages.
    :param url: URL of page.
    :return: Soup from URL
    """
    # Open the URL using driver
    driver.get(url)
    # Wait object
    wait = WebDriverWait(driver, DELAY)
    # Scroll down to bottom for feed to load on website.
    driver.execute_script("window.scrollTo(0, 0.5 * document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait until specific elements are available
    try:
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'recipePage')))
        # Wait Until the ratings are ready to be parsed
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'gig-rating-star gig-rating-star-full')))
        print("SUCCESS")
    except TimeoutException:
        try:
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'photoGalleryPage')))
            print("SUCCESS")
        except TimeoutException:
            print(f"Driver timed out on {url}")
            pass
    # Create soup object
    soup = BeautifulSoup(driver.page_source, features=PARSER)
    return soup


def _is_url_recipe(url):
    """
    :param url: String URL
    :return: Bool of whether URL points to recipe or not.
    """
    if url is None:
        return False

    return ('foodnetwork.com/recipes' in url) and ('Print' not in url) \
           and ('photo' not in url) and ('facebook' not in url)


def _is_url_compilation(url):
    """
    :param url: String URL
    :return: Bool of whether URL points to compilation of recipes or not.
    """
    if url is None:
        return False

    return 'foodnetwork.com/recipes/photos/' in url
