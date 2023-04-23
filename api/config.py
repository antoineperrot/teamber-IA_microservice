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


path_dot_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

config = dotenv_values(path_dot_env)

# Check config content
required_fields = ["FLASK_API_KEY", "MODE"]
missing_fields_in_config = [field for field in required_fields if field not in config]

if len(missing_fields_in_config) != 0:
    raise MissingDotenvFieldsException(missing_fields_in_config)
