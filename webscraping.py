from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import requests


page = 'https://www.bbc.co.uk/food/recipes/avocado_pasta_with_peas_31700'
source = requests.get(url=page).text


def collect_page_data(url):
    url = source
    soup = BeautifulSoup(url, "html.parser")
    res = soup.find("script", {"type": "application/ld+json"})
    print(res)
    json_object = json.loads(res.contents[0])

    rate_count = json_object.get("aggregateRating").get("ratingCount")
    rate_value = json_object.get("aggregateRating").get("ratingValue")

    preptime = json_object.get("prepTime")
    preptime = int(preptime[2:-1])

    cooktime = json_object.get("cookTime")
    cooktime = int(cooktime[2:-1])

    total_time = cooktime + preptime
    total_time = str(total_time) + " minutes"

    recipe_instruction = json_object.get("recipeInstructions")
    print("recipe Instruction: {}".format(recipe_instruction))

    print("The total time for the recipe is {}".format(total_time))

    name = json_object.get("name")
    print("Name: {}".format(name))

    image = json_object.get("image")
    print("URL: {}".format(image))

    agg_rate = json_object.get("aggregateRating")
    print("{}".format(agg_rate))

    recipe_category = json_object.get("recipeCategory")
    print("Recipe category: {}".format(recipe_category))

    rec_cuisine = json_object.get("image")
    print("Recipe cuisine: {}".format(rec_cuisine))

    print("Recipe Ingredients")
    recipe_ingredients = json_object.get('recipeIngredient')
    print("{}".format(recipe_ingredients))


    print("Suitable for Diet")
    suitable_for_diet = json_object.get('suitableForDiet')
    print("{}".format(suitable_for_diet))

    subtree = soup.find_all(text=re.compile(r'window\.__reactInitialState__ = ({.*});'))
    # it mean we are finding all text after "window.__reactInitialState__ ="

    right_hand = subtree[0].strip()

    right_hand = right_hand.replace("window.__reactInitialState__ = ", "")
    right_hand = right_hand.replace(";", "")

    string = json.loads(right_hand)

    stagesWithoutLinks = string.get('recipeReducer').get('recipe').get('stagesWithoutLinks')[0]

    ingredients_list = []
    for i in stagesWithoutLinks.get('ingredients'):
        ingredients_list.append(i.get('foods')[0].get('title'))

    print(ingredients_list)

    print(page)
    pandas_list = {'title': [name],
            'total_time': [total_time],
            'image': [image],
            'ingredients': [ingredients_list],
            'rating_val': [rate_value],
            'rating_count': [rate_count],
            'category': [recipe_category],
            'cuisine': [rec_cuisine],
            'diet': [suitable_for_diet],
            'vegan': ["vegan"],
            'vegetarian': ["vegetarian"],
            'url': [page]
            }

    # creating a dataframe from dictionary
    df = pd.DataFrame(pandas_list)
    df.to_csv("work.csv")
    print(df)
    return df


collect_page_data(source)


