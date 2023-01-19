"""Route du service task_assigner"""
from flask import jsonify, request, make_response, Blueprint

from api.controllers.task_assigner import task_assigner_controller
from api.tools import api_key_required


bp_task_assigner = Blueprint("routes_task_assigner", __name__)


@bp_task_assigner.route("/api/task_assigner", methods=["POST"])
@api_key_required
def task_assigner_route():
    """Route du service task_assigner"""
    json_file = request.get_json()
    return make_response(jsonify(task_assigner_controller(json_file)))
