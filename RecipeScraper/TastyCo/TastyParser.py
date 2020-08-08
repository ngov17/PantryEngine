from RecipeScraper import HTMLRecipeParser
from bs4 import BeautifulSoup


class TastyParser(HTMLRecipeParser):

    def __init__(self, html: BeautifulSoup, url: str):
        super(TastyParser, self).__init__(html, url)

    def parse_html_string(self):
        soup: BeautifulSoup = self.html
        return soup.prettify()

    def parse_url_host(self):
        pass

    def parse_url(self):
        return self.url

    def parse_title(self):
        soup: BeautifulSoup = self.html
        return parse_tasty_title(soup)

    def parse_ingredient(self):
        soup: BeautifulSoup = self.html
        return parse_tasty_ingredients(soup)


def parse_tasty_ingredients(soup: BeautifulSoup):
    """
    :return: Dictionary of ingredients to quantities from soup.
    """
    ingredients_raw = soup.find_all("li", {"class": "ingredient"})
    # TODO: https://tasty.co/recipe/vegan-jalapeno-cornbread-ring breaks cause of nested
    #  statement in ingredients for bold part.
    ingredients = ["".join(ingredient_list.contents) for ingredient_list in ingredients_raw]
    # Construct a dictionary of ingredient -> quantity using both lists
    return ingredients


def parse_tasty_title(soup):
    """
    :param soup: Soup of web page.
    :return: String of title of recipe from soup.
    """

    initial = soup.find_all("h1", {"class": "recipe-name"})
    if len(initial) == 0:
        to_return = "No title"
    else:
        to_return = initial[0].contents[0]
    return to_return
