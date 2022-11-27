from flask import jsonify

from api.servers.base_server import app
from api.data_fetcher import get_data_planning_optimizer
from api.tools import api_key_required


@app.route("/planning_optimizer/", methods=['GET'])
@api_key_required
def planning_optimizer(
    access_token: str,
    datein_isoformat: str,
    dateout_isoformat: str,
    priorite_projets: dict,
    url: str
):
    """Fonction d'optimisation des plannings utilisateurs

    Récupère les données (taches de 'utl' entre 'datein_isoformat' et 'dateout_isoformat', horaires de travail de 'utl')
    auprès du BACK-END Wandeed, et propose une planification intelligente des tâches pour l'utilisateur 'utl'.

    Arguments :

        access_token: str, token pour accéder à la BDD.

        datein_isoformat:  date de début au format ISO du sprint pour la sélection des tâches auprès du BACK

        dateout_isoformat: date de fin au format ISO du sprint pour la sélection des tâches auprès du BACK

        priorite_projets: dictionnaire de la forme {id_projet (int):niveau_priorite_projet (int)}.
        Niveau le plus important: 0.

        url: adresse URL de la base de données du BACK.

    Retourne :

        Un fichier json contenant une planification intelligente des tâches pour l'utilisateur 'utl'

    """

    data = get_data_planning_optimizer(
        access_token, datein_isoformat, dateout_isoformat, url)

    return jsonify(...)
