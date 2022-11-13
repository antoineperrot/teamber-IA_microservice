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


@app.get("/task_assigner/")
def task_assigner(
    access_token: str,
    datein_isoformat: str,
    dateout_isoformat: str,
    curseur: float = 0.0,
    contrainte_etre_sur_projet: str = "de_preference",
    avantage_projet: float = 1.0,
):
    """Fonction d'optimisation de la répartition des tâches au sein d'un groupe de collaborateurs

    Récupère les données (taches, matrices_competence, dispo_utilisateurs, liste_des_participants par projet)
    dans le BACK-END Wandeed pour les dates indiquées et fournie une solution de répartition optimale des tâches entre les utilisateurs.

    Arguments :

        access_token: str, token pour accéder à la BDD.

        datein_isoformat:  date de début au format ISO du sprint pour la sélection des tâches auprès du BACK

        dateout_isoformat: date de fin au format ISO du sprint pour la sélection des tâches auprès du BACK

        curseur: float compris entre 0 et 1 (valeur par défaut 0). Pour une valeur de 0, l'algorithme tente de maximiser le niveau de compétence auquel est réalisé une heure de travail; à 1 il cherche à affecter la tâche à une personne "qui ne sait faire que cette tâche".

        contrainte_etre_sur_projet: str = "de_preference". Valeurs possibles {"oui","de_preference","non"} Si "oui", les tâches peuvent être affectées uniquement à des utilisateurs participants au projet auquel se réfère la tâche.
        Si "de_preference", l'agorithme préférera assigner la tache à quelqu'un qui est sur le projet par rapport à quelqu'un qui ne l'est pas, tout en ne l'interdisant pas.
        Sachant que l'utilité maximale d'assignation d'une tache à quelqu'un de parfaitement compétent est de 3 points, le paramètre "avantage_projet" fixé à 1 mais réglable permet d'influencer la solution.
        Si "non", une personne n'étant par sur un projet ne peut se voir attribuer des tâches de ce même projet.

        avantage_projet : float = 1.0: voir explication pour le paramètre contrainte_etre_sur_projet.

    Retourne :

        Un fichier json contenant une solution de répartition optimale des tâches entre les utilisateurs.

    """
    HTTPException_check_parameters(
        datein_isoformat,
        dateout_isoformat,
        curseur,
        contrainte_etre_sur_projet,
        avantage_projet,
    )

    data = get_data_task_assigner(access_token, datein_isoformat, dateout_isoformat)
    df_prj, df_cmp, df_tsk, df_dsp = split_data(data)

    ## verification cohérence/qualité données
    HTTPException_check_coherence_data(df_prj, df_cmp, df_tsk, df_dsp)

    solution = solve(
        df_prj,
        df_cmp,
        df_tsk,
        df_dsp,
        curseur,
        contrainte_etre_sur_projet,
        avantage_projet,
    )
    out = {"validite_solution": validation_solution(solution), "solution": solution}

    return _return_json(out)


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
