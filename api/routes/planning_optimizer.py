from main import app, api_url
from api.data_fetcher import get_data_planning_optimizer
from api.tools import return_json


@app.get("/planning_optimizer/")
def planning_optimizer(
    access_token: str, datein_isoformat: str, dateout_isoformat: str, id_utl: int
):
    """Fonction d'optimisation des plannings utilisateurs

    Récupère les données (taches de 'utl' entre 'datein_isoformat' et 'dateout_isoformat', horaires de travail de 'utl')
    auprès du BACK-END Wandeed, et propose une planification intelligente des tâches pour l'utilisateur 'utl'.

    Arguments :

        access_token: str, token pour accéder à la BDD.

        datein_isoformat:  date de début au format ISO du sprint pour la sélection des tâches auprès du BACK

        dateout_isoformat: date de fin au format ISO du sprint pour la sélection des tâches auprès du BACK

    Retourne :

        Un fichier json contenant une planification intelligente des tâches pour l'utilisateur 'utl'

    """

    data = get_data_planning_optimizer(
        access_token, datein_isoformat, dateout_isoformat, id_utl, url=api_url
    )

    return return_json(...)
