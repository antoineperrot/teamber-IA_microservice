"""
Module de récupération des données auprès du BACK pour la fonctionnalité task_assigner.
"""
import pandas as pd
from api.back_connector.tools import make_sql_requests


def fetch_data(access_token: str, datein_isoformat: str, dateout_isoformat: str, url: str) -> dict:
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
            "select": ["utl_spkutilisateur", "int_sfkprojet"],
            "from": "lst_vprojet_utilisateur_py",
        },
        "dispos_utilisateurs": {
            "select": ["utl_spkutilisateur", "utl_sdispo"],
            "from": "lst_vdispo_py",
        },
        "matrice_competence": {
            "select": ["emc_sfkutilisateur", "emc_sfkarticle", "emc_sniveau"],
            "from": "lst_vcompetence_py",
        },
        "taches": {
            "select": [
                "evt_spkevenement",
                "evt_sfkprojet",
                "evt_dduree",
                "lgl_sfkligneparent",
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
                        "value": f"{datein_isoformat}",
                    },
                    {
                        "label": "evt_xdate_fin",
                        "field": "evt_xdate_fin",
                        "operator": "lessthan",
                        "type": "date",
                        "value": f"{dateout_isoformat}",
                    },
                    {
                        "label": "lgl_sfkligneparent",
                        "field": "lgl_sfkligneparent",
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

