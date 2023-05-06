"""Route du service planning_optimizer"""
from flask import jsonify, request, make_response, Blueprint
from api.controllers.planning_optimizer_controller import planning_optimizer_controller
from api.tools import api_key_required

bp_planning_optimizer = Blueprint("routes_planning_optimizer", __name__)


@bp_planning_optimizer.route("/api/planning_optimizer", methods=["POST"])
@api_key_required
def start_planning_optimizer():
    """Route du service planning_optimizer"""
    json_file = request.get_json()
    return make_response(jsonify(planning_optimizer_controller(json_file)))


