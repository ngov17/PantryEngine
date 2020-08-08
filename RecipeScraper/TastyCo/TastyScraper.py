from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from RecipeScraper import Recipe
from RecipeScraper.TastyCo.TastyParser import parse_tasty_ingredients, parse_tasty_title

URL = 'https://tasty.co/'
PARSER = 'html5lib'
DELAY = 10
HTML_FOLDER_PATH = './TastyHTML/'


class RecipeTasty(Recipe):
    """
    Recipe subclass for tasty.co
    """

    def __init__(self, link, driver):
        super(RecipeTasty, self).__init__(link, driver)
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
        # Parse info about recipe
        self.ingredients = parse_tasty_ingredients(soup=self.html)
        self.title = parse_tasty_title(soup=self.html)
        self.id = hash(self.title)
        # Write html to local file
        link_suffix = self.link[len(URL):]
        html_file_name = f'{link_suffix.replace("/", "_").lower()}'
        write_html(html_file_name, self.html)
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


def write_html(filename, soup):
    """
    Writes html to file.
    :param filename: file path to write html to.
    :param soup: Soup to write to file.
    :return:
    """

    # Note: This creates a new file or overwrites existing file if it already exist.
    with open(f"{HTML_FOLDER_PATH}{filename}.html", "w+", encoding='utf-8') as file:
        file.write(str(soup))
    return


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
