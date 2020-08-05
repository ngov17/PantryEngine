import time
from typing import Type
from Recipe import Recipe
from TastyScraper import RecipeTasty
from selenium import webdriver


def branch_through_bfs(recipe_url, recipe_class: Type[Recipe], _driver,
                       depth=5, max_recipes=25):
    """
    Starts at a recipe URL, and runs breadth-first-search on all the recipe URLs on the initial recipe's pages.
    Non-recursive.
    :param _driver: Selenium browser driver to parse dynamic pages.
    :param recipe_class: domain-dependent recipe class
    :param recipe_url - URL to a recipe or a page containing recipes.
    :param depth - max number of depth to traverse per layer of neighbors.
    :param max_recipes - max number of neighbors to parse before algorithm stops.
    :return:
    """
    # Queue of recipe URLs
    recipe_queue = []
    # Set of visited URLs
    visited = set()
    # List that contains lists of URLs explored at each layer.
    layered_exploration = []
    # List of recipe objects.
    all_recipe_objects = []

    # Get set of neighbors of recipe_URL and the URL itself.
    recipe_obj = recipe_class(link=recipe_url, driver=_driver)
    recipe_obj.scrape()
    neighbors = set(recipe_obj.get_recipes_from_page())  # Returns set of URL strings
    # Get unvisited neighbors. Put into queue
    unvisited = set.difference(neighbors, visited)
    recipe_queue.extend(unvisited)
    layered_exploration.append(unvisited)
    # For each unvisited neighbor in queue:
    counter = 0
    for url in recipe_queue:
        time.sleep(0.1)
        print(f'{counter}: {url}')
        counter += 1
        #   Remove from queue.
        recipe_queue.remove(url)
        #   Visit page and make recipe object.
        recipe_obj = recipe_class(link=url, driver=_driver)
        #   Scrape + save data.
        recipe_obj.scrape()
        all_recipe_objects.append(recipe_obj)
        #   Add to visited.
        visited.add(url)

        # End the recursion if we reached max number of recipes we want to scrape.
        if len(all_recipe_objects) >= max_recipes:
            print("Max recipes reached.")
            break

        #   If depth > 0:
        #       Get neighbors, add neighbors to queue.
        #   Else do nothing.
        if depth >= 0:
            neighbors_urls = set(recipe_obj.get_recipe_neighbors())
            print(f'Neighbor URLs: {neighbors_urls}')
            not_visited_recipe_neighbors = set.difference(neighbors_urls, visited)
            recipe_queue.extend(list(not_visited_recipe_neighbors))
            layered_exploration.append(list(not_visited_recipe_neighbors))
            # At this point, we add an entire horizontal layer of the tree to the queue, so we decrement depth.
            depth -= 1
        else:
            print("Max depth reached.")
    # Close the driver
    _driver.quit()
    return all_recipe_objects


driver = webdriver.Firefox()
obj = branch_through_bfs('https://tasty.co/recipe/one-pan-honey-lime-chicken', recipe_class=RecipeTasty,
                         _driver=driver, depth=8, max_recipes=75)
print(obj)
