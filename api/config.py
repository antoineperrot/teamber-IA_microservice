"""
Configuration of the server
"""
from dotenv import dotenv_values


class MissingDotenvFieldsException(Exception):
    """
    Exception raised when a value is missing from .env file
    """

    def __init__(self, missing_fields):
        self.missing_fields = missing_fields


config = dotenv_values(".env")

# Check config content
required_fields = ["FLASK_API_KEY", "MODE"]
missing_fields_in_config = [field for field in required_fields if field not in config]

if len(missing_fields_in_config) != 0:
    raise MissingDotenvFieldsException(missing_fields_in_config)
