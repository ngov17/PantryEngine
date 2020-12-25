import threading
import time
import logging
import concurrent.futures
from asyncio import Queue
from typing import Type
from RecipeScraper import RecipeScraper
from selenium import webdriver
from elasticsearch import Elasticsearch
# import our scrapers
from TastyCo.TastyScraper import TastyScraper
from FoodNetwork.FoodNetworkScraper import FoodNetworkScraper
from GeneralRecipeSite.GeneralScraper import GeneralScraper


"""
method that implements our scraper via bfs
"""

def scraper_bfs(recipe_url, recipe_class: Type[RecipeScraper], _driver,
                       depth=5, max_recipes=25):
    """
    Starts at a recipe URL, and runs breadth-first-search on all the recipe URLs on the initial recipe's pages.
    Non-recursive.
    :param _driver: Selenium browser driver to parse dynamic pages.
    :param recipe_class: domain-dependent recipe class
    :param recipe_url - URL to a recipe or a page containing recipes.
    :param depth - max number of depth to traverse per layer of neighbors.
    :param max_recipes - max number of neighbors to parse before algorithm stops.
    :return: number of recipes successfully scraped
    """
    # Queue of recipe URLs
    recipe_queue = []
    # Set of visited URLs
    visited = set()
    # List of recipe objects.
    all_recipe_objects = []
    # Keep track of all recipes successfully scraped
    counter = 1

    # initialize our recipe_obj
    recipe_obj = recipe_class(url=recipe_url, driver=_driver)
    # scrape the first url
    if recipe_obj.scrape():
        print(f'-----------------------INDEXED---{counter}---------------------------')
        counter += 1
        all_recipe_objects.append(recipe_obj)
    else:
        print(f"FAIL {recipe_url}")
    # Get set of neighbors of recipe_URL and the URL itself.
    neighbors = set(recipe_obj.get_neighbor_urls())  # Returns set of URL strings
    # Get unvisited neighbors. Put into queue
    unvisited = set.difference(neighbors, visited)
    recipe_queue.extend(unvisited)

    for url in recipe_queue:
        time.sleep(0.1)
        # print(f'{str(counter)}: {url}')
        #  Remove from queue.
        recipe_queue.remove(url)
        #   Visit page and make recipe object.
        recipe_obj = recipe_class(url=url, driver=_driver)
        #   Scrape + save data.
        if recipe_obj.scrape():
            print(f'-----------------------INDEXED--{counter}-:{url}---------------------------')
            # increment counter
            counter += 1
            all_recipe_objects.append(recipe_obj)
        else:
            print(f"FAIL {url}")
        #   Add to visited.
        visited.add(url)

        # End the recursion if we reached max number of recipes we want to scrape.
        if len(all_recipe_objects) >= max_recipes:
            print("Max recipes reached.")
            break

        #   If depth > 0:
        #       Get neighbors, add neighbors to queue.
        #   Else do nothing.
        if depth > 0:
            neighbors_urls = set(recipe_obj.get_neighbor_urls())
            # print(f'NEIGHBORS: {str(counter)} {neighbors_urls}')
            not_visited_recipe_neighbors = set.difference(neighbors_urls, visited)
            recipe_queue.extend(list(not_visited_recipe_neighbors))
            # At this point, we add an entire horizontal layer of the tree to the queue, so we decrement depth.
            depth -= 1
        else:
            print("Max depth reached.")
            break
    # Close the driver
    _driver.quit()
    return len(all_recipe_objects)


"""
takes in url, recipe_class or [urls], recipe_class
"""
def scrape_concurrently(url, recipe_class:RecipeScraper, depth:int, max_recipes:int):
    if isinstance(url, str):
        scraper_bfs(url, recipe_class, depth, max_recipes)
    elif isinstance(url, list):
        threads = list()
        for index in range(len(url)):
            logging.info("Main    : create and start thread %d.", index)
            x = threading.Thread(target=scraper_bfs, args=(url[index], recipe_class, webdriver.Chrome('/Users/nishant/Downloads/chromedriver'),
                                                             depth, max_recipes))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)

# define our elastic search instance
es = Elasticsearch([
    {'host': 'localhost', 'port': 9200}
])

"""
 conf that customizes elastic's analyzer that configures how we want the ingredients in the recipe_index 
 to be tokenized, filtered, and normalized. Similarly, one for url_index
"""
recipe_index_conf = {
    "settings": {
        "analysis": {
            "analyzer": {
                "analyzer_ingredients": {
                    "type": "custom",
                    "tokenizer": "lowercase",
                    "filter": [
                        "stemmer",
                        "word_delimiter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "ingredients": {
                "type": "text",
                "analyzer": "analyzer_ingredients"
            }
        }
    }
}

url_index_conf = {
    "mappings": {
        "properties": {
            "url": {
                "type": "keyword"
            }
        }
    }

}



"""
function that takes in a tuple of (url, driver) or ([list of urls], driver) and concurrently runs the scraper
"""

# Create our indices: url_index and recipe_index. Log to console to ensure success.
print(es.indices.create("test_url_index", url_index_conf))
print(es.indices.create("test_recipe_index", recipe_index_conf))

# main:

if __name__ == '__main__':
    urls = [
        'https://www.foodnetwork.com/',
        'https://www.food.com/',
        'https://www.tasty.co/'
    ]

    scrape_concurrently(urls, GeneralScraper, depth=10000, max_recipes=1000)






#
# # define our drivers (specific to console)
# driver = webdriver.Chrome('/Users/nishant/Downloads/chromedriver')
# driver2 = webdriver.Chrome('/Users/nishant/Downloads/chromedriver')
# driver3 = webdriver.Chrome('/Users/nishant/Downloads/chromedriver')
# # driver = webdriver.Firefox()
# # 'https://tasty.co/compilation/warm-and-cheesy-garlic-breads'
# # 'https://tasty.co/recipe/one-whole-chicken-three-different-meals'
# # 'https://www.foodnetwork.com/recipes/food-network-kitchen/sweet-and-sour-glazed-shrimp-5288799'
# # https://tasty.co/topic/best-vegetarian
# # branch_through_bfs('https://tasty.co/recipe/one-whole-chicken-three-different-meals',
# # #                    recipe_class=GeneralScraper, _driver=driver, depth=10000, max_recipes=1000)
# # scraper_bfs('https://www.foodnetwork.com/recipes/food-network-kitchen/sweet-and-sour-glazed-shrimp-5288799',
#                    recipe_class=GeneralScraper, _driver=driver2, depth=10000, max_recipes=1000)
# # branch_through_bfs('https://www.food.com/',
# #                    recipe_class=GeneralScraper, _driver=driver3, depth=10000, max_recipes=1000)
# # branch_through_bfs('https://tasty.co/recipe/one-whole-chicken-three-different-meals',
# #                    recipe_class=TastyScraper, _driver=driver, depth=499, max_recipes=3)
# # print("MOVING ON TO low carb meals ")
# # branch_through_bfs('https://tasty.co/topic/baked-goods', recipe_class=RecipeTasty,
# #                    _driver=driver, depth=499, max_recipes=999)

