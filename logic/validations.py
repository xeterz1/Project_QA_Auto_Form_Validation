def Age_validation(age):
    """
    Validates that the input value is a valid age between 0 and 120.
    """
    try:
        age = int(age)
    except ValueError:
        raise ValueError("Age must be a number")

    if age < 0 or age > 120:
        raise ValueError("Invalid age: must be between 0 and 120")

def Name_validation(value):
    """
    Validates that the input value is a valid name.
    """
    if not value or not value.replace(" ", "").isalpha():
        raise ValueError("Invalid name: must contain only alphabetic characters and spaces")

    if len(value) > 50:
        raise ValueError("Invalid name: must not exceed 50 characters")
    elif len(value) < 2:
        raise ValueError("Invalid name: must be at least 2 characters long")

def Email_validation(value):
    """
    Validates that the input value is a valid email address.
    """
    import re
    if not isinstance(value, str):
        raise TypeError("Email must be a string")
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValueError("Invalid email address")  