"""
Tools for the api
"""
from time import time
import logging
import sys
from flask import request, abort
import unittest
from functools import wraps
from pandas import DataFrame
from api.config import config
from api.string_keys import *


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


def timed_function(logger: logging.Logger):
    """
    Cette fonction permettra d'en décorer d'autre afin de les chronométrer, en faisant paraître les temps dans les logs.
    """

    def inner(func):
        """inner"""

        def wrapper_function(*args, **kwargs):
            """fonction wrapper"""
            t_start = time()
            return_args = func(*args, **kwargs)
            t_end = time()
            execution_time = t_end - t_start
            logger.info(f"Temps execution {func.__name__}: {execution_time:.4f}")
            return return_args

        return wrapper_function

    return inner


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        """set token et url"""
        self.commandline = True
        access_token = ""
        try:
            access_token = str(sys.argv[1])
            if "Bearer" not in access_token:
                self.commandline = False
        except IndexError:
            self.commandline = False
        self.access_token = access_token if self.commandline else config["TEST_TOKEN"]
        self.url = "https://antoine.api.wandeed.com/api/lst/search?offset=0&limit=500"


def get_defaults_horaires() -> DataFrame:
    """Retourne les horaires par défaut"""
    default_horaires = DataFrame({key_day_plage_horaire: [0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
                                  key_debut_plage_horaire: ["08:30", "13:30"] * 5,
                                  key_fin_plage_horaire: ["12:00", "17:30"] * 5})
    return default_horaires


def run_test_integration(test_integration: TestIntegration):
    """Run les tests d'intégration"""
    print(f"\n\n========= DEBUT DU TEST INTEGRATION =========")
    test_integration.setUp()
    object_methods = [method_name for method_name in dir(test_integration)
                      if callable(getattr(test_integration, method_name))]

    test_methods = list(filter(lambda name: name[:5] == "test_", object_methods))
    for i, test_method in enumerate(test_methods):
        success_msg = "SUCCESS"
        msg = ""
        try:
            exec(f"test_integration.{test_method}()")
        except AssertionError as a:
            success_msg = "FAIL"
            msg = str(a)

        print(f"TEST {i + 1} / {len(test_methods)} - {success_msg} - {test_method} {'-' + msg}")

    print("========= FIN DU TEST INTEGRATION =========")
    print("Si échec : avez vous bien mis les guillemets ?")
