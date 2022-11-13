from fastapi import FastAPI, HTTPException
import requests
from my_module.test_task_assigner import *

api_url = "https://teamber.api.wandeed.com/api/lst/search?offset=0&limit=500"

# Instanciation de l'app
app = FastAPI()


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




#
# @app.get("/test_task_assigner_with_random_data/")
# def test_task_assigner_with_random_data(curseur:float = 0.0, contrainte_etre_sur_projet: str = 'de_preference', avantage_projet : float = 1.0):
#     """
#     teste la fonction task_assigner(...) avec des données générées aléatoirement et de manière cohérente (propose un grand panel de possibilitées pour la situation des entreprises: surchargées, sous-effectif, sous-chargées, correctes, peu de projets, bcp de projets ...).
#     """
#     df_prj, df_cmp, df_tsk, df_dsp = mock_coherent_data()
#     ## verification cohérence/qualité données ??
#     solution = solve(df_prj, df_cmp, df_tsk, df_dsp,
#                     curseur, contrainte_etre_sur_projet, avantage_projet)
#     out = {
#         "validite_solution" : validation_solution(solution),
#         'solution':solution
#     }
#     return _return_json(out)
#
#
# @app.get('/test_task_assigner/')
# def endpoint_test_task_assigner():
#     test_task_assigner_on_synthetic_data()
#
#
#
