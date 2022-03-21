import re


regex = r"^[\'\w+\.\+_-]+@[A-Za-z0-9\_.-]+\.[a-zA-Z]*$"


def email_validator(email):
    if not email:
        return False
    if re.fullmatch(regex, email):
        return True
    return False


def password_validator(password):
    if 18 < len(password) < 6:
        return False
    return True
