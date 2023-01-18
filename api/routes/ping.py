"""Routes ping"""
from flask import jsonify, make_response, Blueprint
from api.tools import api_key_required


bp_ping = Blueprint("routes_ping", __name__)


@bp_ping.route("/api/ping", methods=["GET"])
def ping_route():
    """
    Ping route
    """
    return make_response(jsonify("pong"), 200)


@bp_ping.route("/api/ping_secure", methods=["GET"])
@api_key_required
def ping_route_secure():
    """
    Ping route
    """
    return make_response(jsonify("ping_secure"), 200)
