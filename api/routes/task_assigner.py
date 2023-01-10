from flask import jsonify, request, make_response

from api.controllers.task_assigner import task_assigner_controller
from api.servers.base_server import app
from api.tools import api_key_required


@app.route("/api/task_assigner", methods=["GET"])
@api_key_required
def task_assigner_route(
    backed_access_token: str,
    backend_url: str,
    date_start: str,
    date_end: str,
    curseur: float = 0.0,
    contrainte_etre_sur_projet: str = "de_preference",
    avantage_projet: float = 1.0,
):

    """
    Fonction d'optimisation de la répartition des tâches au sein d'un groupe de collaborateurs

    Récupère les données (taches, matrices_competence, dispo_utilisateurs, liste_des_participants par projet)
    dans le BACK-END Wandeed pour les dates indiquées et fournie une solution de répartition optimale des tâches
    entre les utilisateurs.

    Arguments :

        backed_access_token: str, token pour accéder à la BDD.

        backend_url: str, url du backend / BDD où récupérer les données utilisateurs

        date_start:  date de début au format ISO du sprint pour la sélection des tâches auprès du BACK

        date_end: date de fin au format ISO du sprint pour la sélection des tâches auprès du BACK

        curseur: float compris entre 0 et 1 (valeur par défaut 0). Pour une valeur de 0, l'algorithme tente de maximiser
        le niveau de compétence auquel est réalisé une heure de travail; à 1 il cherche à affecter la tâche à une
        personne "qui ne sait faire que cette tâche".

        contrainte_etre_sur_projet: str = "de_preference". Valeurs possibles {"oui","de_preference","non"} Si "oui",
        les tâches peuvent être affectées uniquement à des utilisateurs participants au projet auquel se réfère
        la tâche. Si "de_preference", l'agorithme préférera assigner la tache à quelqu'un qui est sur le projet par
        rapport à quelqu'un qui ne l'est pas, tout en ne l'interdisant pas. Sachant que l'utilité maximale d'assignation
        d'une tache à quelqu'un de parfaitement compétent est de 3 points, le paramètre "avantage_projet" fixé à 1 mais
        réglable permet d'influencer la solution. Si "non", une personne n'étant par sur un projet ne peut se voir
        attribuer des tâches de ce même projet.

        avantage_projet : float = 1.0: voir explication pour le paramètre contrainte_etre_sur_projet.

    Retourne :

        Un fichier json contenant une solution de répartition optimale des tâches entre les utilisateurs.

    """
    json_file = request.get_json()
    return make_response(jsonify(task_assigner_controller(json_file)))
