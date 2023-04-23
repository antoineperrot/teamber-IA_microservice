"""
Module de récupération des données auprès du BACK pour la fonctionnalité task_assigner.
"""
from pandas import DataFrame
from werkzeug.exceptions import UnprocessableEntity
from api.back_connector.tools import make_sql_requests
from api.back_connector.task_assigner.requests import get_tasks_request, get_dispo_user_request,\
    get_matrice_competence_request, get_matrice_projet_request
from api.loggers import logger_task_assigner
from api.string_keys import *


def fetch_task_assigner_data_to_back(backend_url: str,
                                     backend_access_token: str,
                                     date_start: str,
                                     date_end: str,
                                     selected_users: list[int] | None) ->\
        tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Va chercher auprès du Back les données nécessaires à l'optimisation de l'assignation des tâches.

    :return df_prj:
    :return df_cmp:
    :return df_tsk:
    :return df_dsp:
    """
    sql_queries = {
        TA_MY_KEY_MATRICE_PROJET: get_matrice_projet_request(selected_users=selected_users),
        TA_MY_KEY_DISPOS_UTILISATEURS: get_dispo_user_request(selected_users=selected_users),
        TA_MY_KEY_MATRICE_COMPETENCE: get_matrice_competence_request(selected_users=selected_users),
        TA_MY_KEY_TACHES_A_ASSIGNER: get_tasks_request(date_start=date_start, date_end=date_end),
    }

    data = make_sql_requests(sql_queries=sql_queries,
                             url=backend_url,
                             access_token=backend_access_token)

    # premier check des données
    for required_data_key in TA_REQUIRED_KEYS:
        if len(data[required_data_key]) == 0:
            raise UnprocessableEntity(description=TA_missing_data_msg[required_data_key])

    # recuperation matrice_projet
    df_prj = DataFrame(data[TA_MY_KEY_MATRICE_PROJET])

    # recuperation matrice_competence : on oublie les compétences pour lesquels les utl sont indéfinis
    df_cmp = (
        DataFrame(data[TA_MY_KEY_MATRICE_COMPETENCE])
        .reset_index(drop=True)
        .astype(int)
    )
    df_cmp = df_cmp[[key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau]]
    df_cmp.sort_values(by=[key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau], inplace=True)
    df_cmp.reset_index(inplace=True, drop=True)

    # recuperation des taches à assigner :
    df_tsk = DataFrame(data[TA_MY_KEY_TACHES_A_ASSIGNER])
    df_tsk.sort_values(by=[key_user_po, key_evenement, key_evenement_project, key_competence], inplace=True)
    df_tsk = df_tsk[[key_user_po, key_evenement, key_competence, key_evenement_project, key_duree_evenement,
                     key_evenement_date_debut, key_evenement_date_fin]]
    df_tsk.reset_index(inplace=True, drop=True)

    # recuperation des disponibilites utl :
    df_dsp = DataFrame(data[TA_MY_KEY_DISPOS_UTILISATEURS])
    df_dsp.sort_values(by=[key_user_po])
    df_dsp.reset_index(inplace=True, drop=True)
    return df_prj, df_cmp, df_tsk, df_dsp
