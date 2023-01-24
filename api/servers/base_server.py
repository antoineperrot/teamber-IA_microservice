"""
Base server for the API
"""
import logging
import time
import traceback
from flask import Flask, jsonify, session, request
from api.loggers import root_logger
from werkzeug.exceptions import HTTPException
from api.config import config
from api.custom_json_encoder import CustomJsonEncoder
from api.routes.task_assigner import bp_task_assigner
from api.routes.planning_optimizer import bp_planning_optimizer
from api.routes.get_etat import bp_get_etat
from api.routes.ping import bp_ping


REQUEST_RECEIVED_TIME = "request_received_time"

app = Flask("API")
app.config["SECRET_KEY"] = config["FLASK_API_KEY"]
app.config["MODE"] = config["MODE"]
app.json_encoder = CustomJsonEncoder
app.logger.setLevel(logging.DEBUG)
app.register_blueprint(bp_task_assigner)
app.register_blueprint(bp_planning_optimizer)
app.register_blueprint(bp_get_etat)
app.register_blueprint(bp_ping)


@app.errorhandler(Exception)
def errorhandler(error):
    """
    Custom error handler for readability
    """
    app.logger.error(error)

    app.logger.error("error traceback:\n" + traceback.format_exc())
    if isinstance(error, HTTPException):
        return (
            jsonify(
                {
                    "statusCode": error.code,
                    "name": error.name,
                    "description": error.description,
                }
            ),
            error.code,
        )
    # Unhandled error formatting
    return (
        jsonify(
            {
                "statusCode": 500,
                "name": "Internal Server Error",
                "description": str(error),
            }
        ),
        500,
    )


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


if __name__ == "__main__":
    app.logger.info("Routes are imported")
    root_logger.error("ICI")
    app.run(host=config["FLASK_HOST"],
            port=config["FLASK_PORT"],
            debug=config["FLASK_DEBUG"])
