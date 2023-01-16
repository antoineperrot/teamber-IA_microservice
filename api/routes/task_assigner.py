"""Route du service task_assigner"""
from flask import jsonify, request, make_response

from api.controllers.task_assigner import task_assigner_controller
from api.servers.base_server import app
from api.tools import api_key_required


@app.route("/api/task_assigner", methods=["GET"])
@api_key_required
def task_assigner_route():
    """Route du service task_assigner"""
    json_file = request.get_json()
    return make_response(jsonify(task_assigner_controller(json_file)))
