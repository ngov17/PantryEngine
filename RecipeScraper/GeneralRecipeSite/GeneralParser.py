import re
from HTMLRecipeParser import HTMLRecipeParser
from bs4 import BeautifulSoup
import json
import pandas

"""
FUNCTIONS:
"""


def return_json(html: BeautifulSoup):
    json_objects = html.find_all("script", {"type": "application/ld+json"})
    if json_objects:
        for json_object in json_objects:
            json_object = json.loads(str(json_object.contents[0]))
            # this is the DataFrame object from pandas that normalizes the json into a flat table
            json_df = pandas.json_normalize(json_object)
            if '@type' in json_df:
                if 'Recipe' in json_df['@type'].values.tolist():
                    return json_df
        return None
    else:
        return None


class GeneralParser(HTMLRecipeParser):

    def __init__(self, html: BeautifulSoup, url: str):
        super(GeneralParser, self).__init__(html, url)
        # retrieve the json object from html
        self.json_df = return_json(self.html)
        # if our json is None, it means it wasn't successfully scraped so self.success = false:
        if self.json_df is None:
            self.success = False
        # call parse_title, parse_ingredients, and parse_steps to finalize value of self.success (REQUIRED)
        self.parse_title()
        self.parse_ingredients()
        self.parse_steps()
        self.parse_author_name()

    def parse_html_string(self):
        return self.html.prettify()

    def parse_url(self):
        return self.url

    def parse_image_url(self):
        if 'image' in self.json_df:
            image = self.json_df["image"].values.tolist()[0]
            if isinstance(image, str):
                return image
            if isinstance(image, list):
                return image[0]
            else:
                # default image
                return "https://thumbs.dreamstime.com/z/empty-wooden-dish-knife-fork-hands-top-view-empty-wooden" \
                       "-dish-knife-fork-hands-top-view-110667406.jpg "
        elif 'image.url' in self.json_df:
            return self.json_df["image.url"].values.tolist()[0]
        else:
            return "https://thumbs.dreamstime.com/z/empty-wooden-dish-knife-fork-hands-top-view-empty-wooden-dish" \
                   "-knife-fork-hands-top-view-110667406.jpg "

    def parse_title(self):
        """
        :param soup: Soup of web page.
        :return: String of title of recipe from soup.
        """
        try:
            if 'name' in self.json_df:
                if 'tasty' in self.url:
                    return self.json_df['name'].values.tolist()[0].rsplit(' ', 1)[0].rsplit(' ', 1)[0]
                else:
                    return self.json_df['name'].values.tolist()[0]

            else:
                # title is a required field
                self.success = False
                return None
        except TypeError:
            self.success = False
            return None

    def parse_ingredients(self):
        """
        :return: Dictionary of ingredients to quantities from soup.
        """
        try:
            if 'recipeIngredient' in self.json_df:
                for ing in self.json_df['recipeIngredient'].values.tolist()[0]:
                    # use the regex module to remove '\xao' etc
                    ing = re.sub('[^A-Za-z0-9]+', ' ', ing)
                    ing = " ".join(ing.split())
                return self.json_df['recipeIngredient'].values.tolist()[0]
            else:
                # ingredients is a required field
                self.success = False
                return None
        except TypeError:
            self.success = False
            return None

    def parse_steps(self):
        try:
            # initialize the steps array
            steps = []
            if 'recipeInstructions' in self.json_df:
                instructions = self.json_df['recipeInstructions'].values.tolist()[0]
                if instructions:
                    for instruction in instructions:
                        if 'text' in instruction:
                            # use the regex module to remove '\xao' etc
                            instruction = re.sub('[^A-Za-z0-9]+', ' ', instruction['text'])
                            instruction = " ".join(instruction.split())
                            steps.append(instruction)
                        else:
                            self.success = False
                            return None
                    return steps
                else:
                    # steps is a required field
                    self.success = False
                    return None
        except TypeError:
            self.success = False
            return None

    def parse_description(self):
        if 'description' in self.json_df:
            desc = self.json_df["description"].values.tolist()[0]
            if isinstance(desc, str):
                return desc
            else:
                return None
        else:
            return None

    def parse_total_time(self):
        if 'totalTime' in self.json_df:
            return self.json_df['totalTime'].values.tolist()[0]

        else:
            return None

    def parse_agg_rating(self):
        rating: float
        if 'aggregateRating.ratingValue' in self.json_df:
            rating = float(self.json_df['aggregateRating.ratingValue'].values.tolist()[0])
            # normalize rating to out of 5
            if rating > 5.0:
                return rating/20.0
            else:
                return rating
        else:
            return None

    def parse_nutrition_info(self):
        if 'nutrition.@type' in self.json_df:
            def insert_nutrition(field: str):
                if field in self.json_df:
                    return self.json_df[field].values.tolist()[0]
                else:
                    return None

            nutrition_info = {
                "calories": insert_nutrition(field="nutrition.calories"),
                "carbohydrates": insert_nutrition(field='nutrition.carbohydrateContent'),
                "fat": insert_nutrition(field='nutrition.fatContent'),
                "protein": insert_nutrition(field='nutrition.proteinContent'),
                "sugar": insert_nutrition(field='nutrition.sugarContent'),
                "fiber": insert_nutrition(field='nutrition.fiberContent')
            }
            return nutrition_info
        else:
            return None

    def parse_author_name(self):
        try:
            if 'author.name' in self.json_df:
                return self.json_df['author.name'].values.tolist()[0]
            elif 'author' in self.json_df:
                author = self.json_df['author'].values.tolist()[0][0]
                if isinstance(author, str):
                    return author
                else:
                    return author['name']
            else:
                # author is required:
                self.success = False
                return None
        except TypeError:
            self.success = False
            return None

    def parse_keywords(self):
        if 'keywords' in self.json_df:
            return self.json_df['keywords'].values.tolist()[0]
        else:
            return None

    def parse_recipe_cuisine(self):
        if 'recipeCuisine' in self.json_df:
            cuisine = self.json_df['recipeCuisine'].values.tolist()[0]
            if isinstance(cuisine, str):
                return cuisine
            elif isinstance(cuisine, list) and len(cuisine) > 0:
                return cuisine[0]
            else:
                return None

        else:
            return None

    def parse_recipe_category(self):
        if 'recipeCategory' in self.json_df:
            return self.json_df['recipeCategory'].values.tolist()[0]
        else:
            return None
