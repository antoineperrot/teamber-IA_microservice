"""
Module contenant les loggers
"""
import logging

file_handler = logging.FileHandler("logs.log", mode="w")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

root_logger = logging.getLogger("MY_API_REST")
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
