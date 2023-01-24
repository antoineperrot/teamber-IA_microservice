"""Route pour récupérer un état de calcul"""
from flask import jsonify, make_response, Blueprint
from api.tools import api_key_required
from api.models import cache

bp_get_etat = Blueprint("get_etat_calcul", __name__)


@bp_get_etat.route("/api/get_etat/<int:identifiant>", methods=["GET"])
@api_key_required
def get_etat_planning_optimizer(identifiant: int):
    """Route permettant de récupérer un état de calcul"""
    return make_response(jsonify(cache.get_status(calcul_id=identifiant)))
