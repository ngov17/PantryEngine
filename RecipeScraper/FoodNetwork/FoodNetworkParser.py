from HTMLRecipeParser import HTMLRecipeParser
from bs4 import BeautifulSoup
import json
import re


class FoodNetworkParser(HTMLRecipeParser):

    def __init__(self, html: BeautifulSoup, url: str):
        super(FoodNetworkParser, self).__init__(html, url)

    def parse_html_string(self):
        return self.html.prettify()

    def parse_url_host(self):
        return "https://www.foodnetwork.com/"

    def parse_url(self):
        return self.url

    def parse_image_url(self):
        image_url = self.html.find_all("img", {"class": "m-MediaBlock__a-Image a-Image"})
        if image_url:
            return image_url[0]["src"]
        else:
            # this is a default image
            return "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg"

    def parse_title(self):
        """
        :param soup: Soup of web page.
        :return: String of title of recipe from soup.
        """
        title = self.html.find_all("title")
        if title:
            return title[0].contents[0].split(" | ")[0]
        else:
            # set our success variable to False
            self.success = False
            # note: None gets converted to null in JSON and hence Elasticsearch
            return None

    def parse_ingredients(self):
        """
        :return: list of ingredients
        """
        ingredients_raw = self.html.find_all("p", {"class": "o-Ingredients__a-Ingredient"})
        if ingredients_raw:
            ingredients = []
            for ingredient in ingredients_raw:
                # use the regex module to remove '\xao' etc
                ingredient = re.sub('[^A-Za-z0-9]+', ' ', ingredient.contents[0])
                ingredient = ingredient.rstrip()
                ingredients.append(ingredient)
            return ingredients
        else:
            # set our success variable to failure and return NONE
            self.success = False
            return None

    def parse_steps(self):
        # initialize our steps array
        steps = []
        contents_list = self.html.find_all("li", {"class": "o-Method__m-Step"})
        if contents_list:
            for step in contents_list:
                # deal with escape sequences (\n, \xao etc)
                escapes = ''.join([chr(char) for char in range(1, 32)])  # makes a list of all escape sequences
                translator = str.maketrans('', '', escapes)  # configures the translator to remove escape sequences
                step = step.contents[0].translate(translator)
                # we use strip to remove trailing and leading whitespaces
                step = step.lstrip()
                step = step.rstrip()
                steps.append(step)
            return steps
        else:
            self.success = False
            return None

    def parse_agg_rating(self):
        rating: float
        contents_rating = self.html.find("span", {"class": "gig-rating-stars"})
        print(contents_rating['title'].split(" "))
        if contents_rating:
            try:
                # Convert the string into a float
                rating = float(contents_rating["title"].split(" ")[0])
                return rating
            except ValueError:
                # in this case theres a parsing error so we just return NONE and move on to the next recipe page
                print("PARSE INT EXCEPTION")
                return None
        else:
            return None

    def parse_nutrition_info(self):
        contents_list = self.html.find_all("script", {"type": "application/ld+json"})
        if contents_list:
            nutrition_list = json.loads(str(contents_list[0].contents[0]))
            if "nutrition" in nutrition_list:
                nutrition = nutrition_list["nutrition"]
                nutrition_info = {
                    "calories": nutrition["calories"],
                    "carbohydrates": nutrition["carbohydrateContent"],
                    "fat": nutrition["fatContent"],
                    "protein": nutrition["proteinContent"],
                    "sugar": nutrition["sugarContent"],
                    "fiber": nutrition["fiberContent"]
                }
                return nutrition_info
            else:
                return None
        else:
            return None

    def parse_author_name(self):
        contents_list = self.html.find_all("script", {"type": "application/ld+json"})
        if contents_list:
            author_list = json.loads(str(contents_list[0].contents[0]))
            if "author" in author_list:
                if len(author_list["author"]) == 1:
                    name = author_list["author"][0]["name"]
                    return name
                else:
                    return None
            else:
                self.success = False
                return None
        else:
            self.success = False
            return None

    def parse_reviews(self):
        reviews = []
        reviews_list = self.html.find_all("p", {"class": "tip-body"})
        if reviews_list:
            for review in reviews_list:
                reviews.append(review.contents)
            return reviews
        else:
            return reviews

    def parse_description(self):
        description = ""
        desc_list = self.html.find_all("meta", {"name": "description"})
        if desc_list:
            desc = desc_list[0]["content"]
            print(desc)
            return desc
        else:
            return None
