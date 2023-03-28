"""
Module de récupération des données auprès du BACK pour la fonctionnalité task_assigner.
"""
from pandas import DataFrame

from api.back_connector.tools import make_sql_requests
from api.back_connector.task_assigner.requests import get_tasks_request, get_dispo_user_request,\
    get_matrice_competence_request, get_matrice_projet_request
from api.loggers import logger_task_assigner


def fetch_task_assigner_data_to_back(backend_url: str,
                                     backend_access_token: str,
                                     date_start: str,
                                     date_end: str) ->\
        tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Va chercher auprès du Back les données nécessaires à l'optimisation de l'assignation des tâches.

    TODO: à compléter

    :return df_prj:

    :return df_cmp:

    :return df_tsk:

    :return df_dsp:

    """
    sql_queries = {
        "matrice_projet": get_matrice_projet_request(),
        "dispos_utilisateurs": get_dispo_user_request(),
        "matrice_competence": get_matrice_competence_request(),
        "taches": get_tasks_request(date_start=date_start, date_end=date_end),
    }

    logger_task_assigner.debug(sql_queries)
    data = make_sql_requests(sql_queries=sql_queries,
                             url=backend_url,
                             access_token=backend_access_token)

    # recuperation matrice_projet
    df_prj = DataFrame(data["matrice_projet"])
    # recuperation matrice_competence : on oublie les compétences pour lesquels les utl sont indéfinis
    df_cmp = (
        DataFrame(data["matrice_competence"])
        .dropna()
        .reset_index(drop=True)
        .astype(int)
    )
    # recuperation des taches à assigner :
    df_tsk = DataFrame(data["taches"])
    # recuperation des disponibilites utl :
    df_dsp = DataFrame(data["dispos_utilisateurs"])

    return df_prj, df_cmp, df_tsk, df_dsp
