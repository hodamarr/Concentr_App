import random as r
import string


def __generate_code(k):
    """return 5 digit code"""
    return ''.join(r.choices(string.ascii_letters + string.digits, k=k))