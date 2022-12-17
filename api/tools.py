"""
Tools for the api
"""
from flask import request, abort

from api.servers.base_server import app


def api_key_required(func):
    def wrapper_function(*args, **kwargs):
        if request.headers:
            auth_header = request.headers.get("Authorization", None)

            if not auth_header:
                abort(401, "Missing Authorization header")

            if "Bearer" not in auth_header:
                abort(401, "Missing Authorization header")

            api_key = auth_header.replace("Bearer ", "")

            if api_key != app.config["SECRET_KEY"]:
                abort(401, "Invalid api-key")

        return func(*args, **kwargs)

    return wrapper_function
