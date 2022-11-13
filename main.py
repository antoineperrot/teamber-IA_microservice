from fastapi import FastAPI, HTTPException
import requests
from my_module.test_task_assigner import *

api_url = "https://teamber.api.wandeed.com/api/lst/search?offset=0&limit=500"

# Instanciation de l'app
app = FastAPI()





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
