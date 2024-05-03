from datetime import datetime


def string_has_numbers(input_string):
    """
    Check if a string contains any numbers.

    Args:
        input_string (str): The string to check.

    Returns:
        bool: True if the string contains numbers, False otherwise.
    """
    return any(char.isdigit() for char in input_string)


def string_has_special_characters(input_string):
    """
    Check if a string contains special characters.

    Args:
        input_string (str): The string to be checked.

    Returns:
        bool: True if the string contains special characters, False otherwise.
    """
    return any(not c.isalnum() for c in input_string)


def validate_date(date_input):
    """
    Validates the format of a date string.

    Args:
        date_input (str): The date string to be validated.

    Raises:
        ValueError: If the date string is not in the format 'YYYY-mm-dd'.

    Returns:
        None
    """
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Invalid date format. Date should be in the format 'YYYY-mm-dd'.")


def get_attributes_and_values(obj):
    """
    Retrieves the attributes and their corresponding values of an object.

    Args:
        obj: The object to retrieve attributes from.

    Returns:
        A dictionary containing the attributes and their values.

    """
    attributes = {}
    for attr in dir(obj):
        # If attribute has no preceding "__" or "_" it means it is not magic attribute or private attribute name
        if not attr.startswith("__") and not attr.startswith("_"):
            try:
                value = getattr(obj, attr)
                # "callable" returns True is given attribue is an callable, so function for example
                if not callable(value):
                    attributes[attr] = value
            except AttributeError:
                continue
    return attributes


if __name__ == "__main__":
    print(string_has_special_characters("Hello!"))
    print(string_has_special_characters("Hello"))
    print(string_has_special_characters("Hello@#$@#"))
