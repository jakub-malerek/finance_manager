from datetime import datetime


def string_has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def string_has_special_characters(input_string):
    return any(not c.isalnum() for c in input_string)


def validate_date(date_input):
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Invalid date format. Date should be in the format 'YYYY-mm-dd'.")


if __name__ == "__main__":
    print(string_has_special_characters("Hello!"))
    print(string_has_special_characters("Hello"))
    print(string_has_special_characters("Hello@#$@#"))
