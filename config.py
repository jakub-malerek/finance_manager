import json


def load_item_categories(path="./categories.json"):
    try:
        with open(path, "r") as f:
            read_json = json.loads(f.read())
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "There was problem fetching the categories from categories.json.") from e
    except json.JSONDecodeError as e:
        raise Exception(
            "There was problem with the JSON file structure or syntax.") from e
    else:
        try:
            categories = read_json["categories"]
        except KeyError as e:
            raise KeyError(
                "Categories were not found in the categories.json file.")

    return categories


ITEM_CATEGORIES = load_item_categories()
