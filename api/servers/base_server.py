"""
Base server for the API
"""
import time
import logging
from flask import Flask, make_response, jsonify, session, request
from werkzeug.exceptions import HTTPException

from api.config import config

from module.logger import root_logger

REQUEST_RECEIVED_TIME = "request_received_time"

app = Flask("API")
app.config["SECRET_KEY"] = config["FLASK_API_KEY"]
app.config["MODE"] = config["MODE"]
app.logger.setLevel(logging.DEBUG)


# Mode constant
PRODUCTION = "PRODUCTION"
DEV = "DEV"

if app.config["MODE"] == DEV:
    pass


# Import is not at the beginning of the file, because app should be declared before
# import routes ...

@app.errorhandler(Exception)
def errorhandler(error):
    """
    Custom error handler for readability
    """
    app.logger.error(error)
    if isinstance(error, HTTPException):
        return jsonify({"statusCode": error.code, "name": error.name, "description": error.description}), error.code
    # Unhandled error formatting
    return jsonify({"statusCode": 500, "name": "Internal Server Error", "description": str(error)}), 500


@app.before_request
def before_request():
    """
    Store the time we received the request for future use (request response time computation)
    """
    session[REQUEST_RECEIVED_TIME] = time.time()


@app.after_request
def after_request(response):
    """
    Computes and logs the response time
    :param response:
    :return:
    """
    duration = time.time() - session[REQUEST_RECEIVED_TIME]

    app.logger.info(
        f"Request answered : {request.remote_addr} : {request.full_path}"
        f" {request.method} -> {response.status} ({duration} s)"
    )

    return response


@app.route("/api/ping", methods=["GET"])
def ping_route():
    """
    Ping route
    """
    return make_response(jsonify("pong"), 200)
