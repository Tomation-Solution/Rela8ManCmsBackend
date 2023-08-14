import jwt

from django.conf import settings
from datetime import datetime, timedelta

import random
import string


def generate_token(data):
    token = jwt.encode({"name": data.get("name", None), "email": data["email"],
                       "exp": datetime.utcnow() + timedelta(days=7)}, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms='HS256')
    return payload


def generate_unique_char(number: int = 10):
    "helps u generate random char that are unqiue"
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(number))
