from HTMLRecipeParser import HTMLRecipeParser
from bs4 import BeautifulSoup
import json


class TastyParser(HTMLRecipeParser):

    def __init__(self, html: BeautifulSoup, url: str):
        super(TastyParser, self).__init__(html, url)

    def parse_html_string(self):
        return self.html.prettify()

    def parse_url_host(self):
        return "https://tasty.co/"

    def parse_url(self):
        return self.url

    def parse_image_url(self):
        image_url = self.html.find("meta", property="og:image")
        if image_url:
            return image_url["content"]
        else:
            # this is a default image
            return "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2018/12/Shakshuka-19.jpg"

    def parse_title(self):
        """
        :param soup: Soup of web page.
        :return: String of title of recipe from soup.
        """
        initial = self.html.find_all("h1", {"class": "recipe-name"})
        if len(initial) == 0:
            # set our success variable to False
            self.success = False
            # note: None gets converted to null in JSON and hence Elasticsearch
            return None
        else:
            to_return = initial[0].contents[0]
            return to_return

    def parse_ingredients(self):
        """
        :return: Dictionary of ingredients to quantities from soup.
        """
        ingredients_raw = self.html.find_all("li", {"class": "ingredient"})
        print(ingredients_raw)
        if ingredients_raw:
            ingredients = []
            for ingredient_list in ingredients_raw:
                if not ingredient_list.find("span"):
                    ingredients.append("".join(ingredient_list.contents))
            if len(ingredients) == 0:
                self.success = False
                return None
            else:
                return ingredients
        else:
            # set our success variable to failure and return an empty list
            self.success = False
            return None

    def parse_steps(self):
        # initialize our steps array
        steps = []
        contents_list = self.html.find_all("script", {"type": "application/ld+json"})
        if contents_list:
            steps_list = json.loads(str(contents_list[0].contents[0]))
            if "recipeInstructions" in steps_list:
                for step in steps_list["recipeInstructions"]:
                    steps.append(step["text"])
                return steps
            else:
                self.success = False
                return None
        else:
            self.success = False
            return None

    def parse_agg_rating(self):
        rating: float
        contents_list = self.html.find_all("script", {"type": "application/ld+json"})
        if contents_list:
            rating_list = json.loads(str(contents_list[0].contents[0]))
            if "aggregateRating" in rating_list:
                rating = int(rating_list["aggregateRating"]["ratingValue"])
                return rating/20.0
            else:
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
