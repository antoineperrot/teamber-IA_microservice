"""
Tools for the api
"""
from flask import request, abort

from api.config import config
from functools import wraps


def api_key_required(func):
    """
    View decorator - require valid api key
    Extract api-key information from authorization header
    authorization header has the following form: Bearer key
    """

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        """wrapper"""
        if request.headers:
            auth_header = request.headers.get("Authorization", None)

            if not auth_header:
                abort(401, "Missing Authorization header")

            if "Bearer" not in auth_header:
                abort(401, "Missing Authorization header")

            api_key = auth_header.replace("Bearer ", "")

            if api_key != config["FLASK_API_KEY"]:
                abort(401, "Invalid api-key")

        return func(*args, **kwargs)

    return wrapper_function
