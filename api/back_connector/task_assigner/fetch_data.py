"""
Module de récupération des données auprès du BACK pour la fonctionnalité lib_task_assigner.
"""
import numpy as np
from pandas import DataFrame
from werkzeug.exceptions import UnprocessableEntity
from api.back_connector.tools import make_sql_request
from api.back_connector.task_assigner.requests import get_tasks_request, get_dispo_user_request,\
    get_matrice_competence_request, get_matrice_projet_request
from api.string_keys import *


def fetch_task_assigner_data_to_back(backend_url: str,
                                     backend_access_token: str,
                                     date_start: str,
                                     date_end: str,
                                     selected_users: list[int] | None) ->\
        tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:
    """
    Va chercher auprès du Back les données nécessaires à l'optimisation de l'assignation des tâches.

    :return df_prj:
    :return df_cmp:
    :return df_tsk:
    :return df_dsp:
    """

    # 1 récupère les taches
    data_tasks = make_sql_request(sql_query=get_tasks_request(date_start=date_start, date_end=date_end),
                                  url=backend_url,
                                  access_token=backend_access_token,
                                  request_name=TA_MY_KEY_TACHES_A_ASSIGNER)
    # clean df_tsk
    df_tsk = DataFrame(data_tasks)
    df_tsk.sort_values(by=[key_user_po, key_evenement, key_evenement_project, key_competence], inplace=True)
    df_tsk = df_tsk[[key_user_po, key_evenement, key_competence, key_evenement_project, key_duree_evenement,
                     key_evenement_date_debut, key_evenement_date_fin]]
    df_tsk.reset_index(inplace=True, drop=True)

    competences_requises = [int(val) for val in list(np.sort(np.unique(df_tsk[key_competence])))]
    # 2 récupère la matrice compétence pour les compétences requises par les taches

    data_cmp = make_sql_request(sql_query=get_matrice_competence_request(selected_competences=competences_requises),
                                url=backend_url,
                                access_token=backend_access_token,
                                request_name=TA_MY_KEY_MATRICE_COMPETENCE)

    df_cmp = (
        DataFrame(data_cmp)
        .reset_index(drop=True)
        .astype(int)
    )
    if len(df_cmp) == 0:
        raise UnprocessableEntity(description="Il n'existe aucun utilisateur compétent pour les tâches requises")
    df_cmp = df_cmp[[key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau]]
    df_cmp.sort_values(by=[key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau], inplace=True)
    df_cmp.reset_index(inplace=True, drop=True)

    sub_df_cmp = df_cmp.loc[df_cmp[key_emc_sfkarticle].isin(competences_requises)]
    # on garde uniquement les utilisateurs compétents dans les compétences demandées
    utilisateurs_ayant_les_competences_requises = [int(val) for val in list(np.sort(np.unique(sub_df_cmp[key_emc_sfkutilisateur])))]
    competences_requises_with_candidate_users = [int(val) for val in list(np.sort(np.unique(
        sub_df_cmp.loc[sub_df_cmp[key_emc_sfkutilisateur].isin(utilisateurs_ayant_les_competences_requises)][
            key_emc_sfkarticle])))]

    # raffinage du df_cmp
    df_cmp = df_cmp.loc[df_cmp[key_emc_sfkarticle].isin(competences_requises_with_candidate_users)]
    df_cmp.reset_index(drop=True, inplace=True)

    # raffinage du df_tsk
    doable_tasks_index = df_tsk[key_competence].isin(competences_requises_with_candidate_users)
    undoable_tasks = df_tsk.loc[~doable_tasks_index]
    df_tsk = df_tsk.loc[doable_tasks_index] # doable tasks

    if len(df_tsk) == 0:
        raise UnprocessableEntity(description="Aucun utilisateur n'est compétent pour réaliser les tâches demandées. "
                                              "Veillez à bien renseigner les compétences des utilisateurs.")

    df_tsk.reset_index(drop=True, inplace=True)
    undoable_tasks.reset_index(drop=True, inplace=True)

    # 3 récupère la matrice projet des utilisateurs candidats pour les taches
    data_prj = make_sql_request(sql_query=get_matrice_projet_request(selected_users=utilisateurs_ayant_les_competences_requises),
                                url=backend_url,
                                access_token=backend_access_token,
                                request_name=TA_MY_KEY_MATRICE_PROJET)

    df_prj = DataFrame(data_prj)


    # 4 récupère les dispos des utilisateurs candidats pour les taches

    data_dsp = make_sql_request(
        sql_query=get_dispo_user_request(selected_users=utilisateurs_ayant_les_competences_requises),
        url=backend_url,
        access_token=backend_access_token,
        request_name=TA_MY_KEY_DISPOS_UTILISATEURS)

    df_dsp = DataFrame(data_dsp)
    if len(df_dsp) == 0:
        raise UnprocessableEntity(description="Aucune donnée sur la disponibilité des utlisateurs n'a pu être récupérée")
    df_dsp.sort_values(by=[key_user])
    df_dsp.reset_index(inplace=True, drop=True)

    return df_prj, df_cmp, df_tsk, df_dsp, undoable_tasks
