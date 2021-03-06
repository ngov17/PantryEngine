from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from RecipeScraper import RecipeScraper
from TastyCo.TastyParser import TastyParser
from RecipeIndexer import RecipeIndexer

URL = 'https://tasty.co/'
PARSER = 'html5lib'
DELAY = 10
HTML_FOLDER_PATH = './TastyHTML/'


class TastyScraper(RecipeScraper):
    """
    Recipe subclass for tasty.co
    """

    def __init__(self, link, driver):
        super(TastyScraper, self).__init__(driver)
        # initialize the link variable as required:
        self.link = URL + link[len(URL):]
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
        link = URL + self.link[len(URL):]
        parser = TastyParser(self.html, link)
        # NOTE: we don't need this part as all TastyParser needs is the html file (as soup)
        # # Parse info about recipe
        self.ingredients = parser.parse_ingredients()
        self.title = parser.parse_title()
        # self.id = hash(self.title)
        # # Write html to local file
        # html_file_name = f'{link_suffix.replace("/", "_").lower()}'
        # write_html(html_file_name, self.html)
        # call our indexer whose init method indexes this particular html page based on parser
        # this essentially fills in the data into elastic search for this page
        # RecipeIndexer(parser)
        print(f'{self.title} with ingredients:\n{self.ingredients}')
        return self.html

    def get_recipes_from_page(self, url=None):
        """
        # TODO: Comments.
        :param url:
        :return:
        """
        if url is not None:
            soup = get_soup(url, driver=self.driver)
        elif self.html is None:
            self.scrape()
            soup = self.html
        else:
            soup = self.html

        all_urls = [attribute.get('href') for attribute in soup.find_all("a")]
        recipe_urls = [url for url in all_urls if _is_url_recipe(url)]
        return recipe_urls

    def get_recipe_neighbors(self):
        """
        # TODO: Comments.
        :return:
        """
        soup = self.html
        # Scrape class=recipe
        #   class = result__image-link href
        cards = soup.find_all("a", href=True)
        links = [a.get('href') for a in cards]
        to_return = []
        recipes = self.get_recipes_from_page()
        to_return.extend(recipes)
        # Iterate over all card links, and if the link is not a recipe,
        # visits the page and gets the recipes featured there.
        for link in links:
            # If it's not recipe, we scrape all of it for recipes.
            if _is_url_compilation(link):
                compilation_url = get_url(link)
                recipes_from_compilation = self.get_recipes_from_page(url=compilation_url)
                to_return.extend(recipes_from_compilation)
        return to_return


def get_url(url: str):
    """
    Gets actual url string from an href. Mostly to be used to get compilation URL from href.
    :param url: href value
    :return: url from value.
    """
    if 'tasty.co' in url:
        return url
    else:
        return 'https://tasty.co' + url

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
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'feed__items')))
        wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'related-recipes')))
    except TimeoutException:
        print(f"Driver timed out on {url}")
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

    return 'tasty.co/recipe/' in url


def _is_url_compilation(url):
    """
    :param url: String URL
    :return: Bool of whether URL points to compilation of recipes or not.
    """
    if url is None:
        return False

    return '/compilation/' in url
