"""
Configuration of the server
"""
import os
from dotenv import dotenv_values


class MissingDotenvFieldsException(Exception):
    """
    Exception raised when a value is missing from .env file
    """

    def __init__(self, missing_fields):
        self.missing_fields = missing_fields


config = dotenv_values(".env")

# Check config content
required_fields = ["FLASK_API_KEY", "MODE", "LAST_TEST_FILES_PATH"]
missing_fields_in_config = [field for field in required_fields if field not in config]

#if not os.path.exists(config["LAST_TEST_FILES_PATH"]):
#    os.mkdir(config["LAST_TEST_FILES_PATH"])

if len(missing_fields_in_config) != 0:
    raise MissingDotenvFieldsException(missing_fields_in_config)
