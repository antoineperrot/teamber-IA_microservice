"""
Module de récupération des données auprès du BACK pour la fonctionnalité task_assigner.
"""
import pandas as pd

from api.back_connector.tools import make_sql_requests
from api.string_keys import *


def fetch_task_assigner_data_to_back(access_token: str, date_start: str, date_end: str, url: str) -> dict:
    """
    Va chercher auprès du Back les données nécessaires à l'optimisation de l'assignation des tâches.

    TODO: à compléter

    :return df_prj:

    :return df_cmp:

    :return df_tsk:

    :return df_dsp:

    """
    sql_queries = {
        "matrice_projet": {
            "select": [key_user, key_project],
            "from": "lst_vprojet_utilisateur_py",
        },
        "dispos_utilisateurs": {
            "select": [key_user, key_user_dispo],
            "from": "lst_vdispo_py",
        },
        "matrice_competence": {
            "select": [key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau],
            "from": "lst_vcompetence_py",
        },
        "taches": {
            "select": [
                key_evenement,
                key_evenement_project,
                key_duree_evenement,
                key_competence,
            ],
            "from": "lst_vevenement_py",
            "where": {
                "condition": "and",
                "rules": [
                    {
                        "label": "evt_xdate_debut",
                        "field": "evt_xdate_debut",
                        "operator": "greaterthan",
                        "type": "date",
                        "value": f"{date_start}",
                    },
                    {
                        "label": "evt_xdate_fin",
                        "field": "evt_xdate_fin",
                        "operator": "lessthan",
                        "type": "date",
                        "value": f"{date_end}",
                    },
                    {
                        "label": key_competence,
                        "field": key_competence,
                        "operator": "isnotnull",
                        "type": "integer",
                        "value": "none",
                    },
                ],
            },
        },
    }

    data = make_sql_requests(sql_queries, url, access_token)

    # recuperation matrice_projet
    df_prj = pd.DataFrame(data["matrice_projet"])
    # recuperation matrice_competence : on oublie les compétences pour lesquels les utl sont indéfinis
    df_cmp = (
        pd.DataFrame(data["matrice_competence"])
        .dropna()
        .reset_index(drop=True)
        .astype(int)
    )
    # recuperation des taches à assigner :
    df_tsk = pd.DataFrame(data["taches"])
    # recuperation des disponibilites utl :
    df_dsp = pd.DataFrame(data["dispos_utilisateurs"])

    return df_prj, df_cmp, df_tsk, df_dsp
