from flask import jsonify

from api.servers.base_server import app
from api.tools import api_key_required

from api.controllers.planning_optimizer import check_parameters
from api.back_connector.planning_optimizer import fetch_data


@app.route("/planning_optimizer/", methods=['GET'])
@api_key_required
def planning_optimizer(url: str,
                       access_token: str,
                       date_start: str,
                       date_end: str,
                       priorites_projets: dict,
                       duree_min_morceau: float = 1.0):
    """Fonction d'optimisation des plannings utilisateurs

    Récupère les données (taches de 'utl' entre 'date_start' et 'date_end', horaires de travail de 'utl')
    auprès du BACK-END Wandeed, et propose une planification intelligente des tâches pour l'utilisateur 'utl'.

    Arguments :

        access_token: str, token pour accéder à la BDD.

        date_start:  date de début au format ISO du sprint pour la sélection des tâches auprès du BACK

        date_end: date de fin au format ISO du sprint pour la sélection des tâches auprès du BACK

        priorites_projets: dictionnaire de la forme {id_projet (int):niveau_priorite_projet (int)}.
        Niveau le plus important: 0.

        url: adresse URL de la base de données du BACK.

    Retourne :

        Un fichier json contenant une planification intelligente des tâches pour l'utilisateur 'utl'

    """
    check_parameters(date_start, date_end, priorites_projets)

    imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires =\
        fetch_data(url, access_token, date_start, date_end, priorites_projets)

    from api.services.planning_optimizer import optimize_plannings
    optimized_planning = optimize_plannings(imperatifs,
                                            horaires,
                                            taches,
                                            date_start,
                                            date_end,
                                            duree_min_morceau)

    return jsonify(optimized_planning)
