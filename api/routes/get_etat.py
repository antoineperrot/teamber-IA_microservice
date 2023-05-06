"""Route pour récupérer un état de calcul"""
from flask import jsonify, make_response, Blueprint, request
from werkzeug.exceptions import UnprocessableEntity

from api.tools import api_key_required
from api.models import cache

bp_get_etat = Blueprint("get_etat_calcul", __name__)


@bp_get_etat.route("/api/get_etat", methods=["GET"])
@api_key_required
def get_etat_planning_optimizer():
    """Route permettant de récupérer un état de calcul"""
    identifiant = request.args.get('identifiant', type=int)
    if identifiant is None:
        return UnprocessableEntity(description="Veuillez renseigner le champ 'identifiant' (integer)")
    status = cache.get_status(calcul_id=identifiant)
    if status is None:
        return UnprocessableEntity(description="L'identifiant ne correspond à aucun etat dans le cache")
    return make_response(jsonify(status))
