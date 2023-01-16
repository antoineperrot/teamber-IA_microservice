"""Route du service planning_optimizer"""
from flask import jsonify, request, make_response

from api.controllers.planning_optimizer import planning_optimizer_controller
from api.servers.base_server import app
from api.tools import api_key_required


@app.route("/api/planning_optimizer", methods=["POST"])
@api_key_required
def planning_optimizer_route():
    """Route du service planning_optimizer"""
    json_file = request.get_json()
    return make_response(jsonify(planning_optimizer_controller(json_file)))
