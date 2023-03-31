"""
Tools for the api
"""
from flask import request, abort
import unittest
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


def run_test_inte(test_instance: unittest.TestCase):
    """Run les tests d'intégration"""
    test_instance.setUp()
    object_methods = [method_name for method_name in dir(test_instance)
                      if callable(getattr(test_instance, method_name))]

    test_methods = list(filter(lambda name: name[:5] == "test_", object_methods))
    for i, test_method in enumerate(test_methods):
        success = True
        msg = ""
        try:
            exec(f"test_instance.{test_method}()")
        except AssertionError as a:
            success = False
            msg = str(a)

        print(f"TEST {i + 1} / {len(test_methods)} success : {success} - {test_method} - {msg}")
