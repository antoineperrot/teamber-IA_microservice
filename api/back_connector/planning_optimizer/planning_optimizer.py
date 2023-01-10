"""
Module de récupération des données auprès du BACK pour la fonctionnalité planning_optimizer.
"""
from typing import Tuple

import pandas as pd

from api.back_connector.planning_optimizer.data_handlers.filtrage import filtre
from api.back_connector.tools import make_sql_requests
from api.string_keys import *


# TODO: corriger les ValueError
def fetch_data_to_wandeed_backend(
    url: str, access_token: str, date_start: str, date_end: str, key_project_prioritys_projets: dict
) -> Tuple[dict, dict, dict, list]:
    """
    Prépare et envoie les requêtes SQL auprès du Back Wandeed qui renvoie les données demandées.

    :param url: url de la base de données du back
    :param access_token: token d'accès à la base de données du back
    :param date_start: date de début du sprint à optimiser, au format ISO. example : "2022-10-03T06:31:00.000Z"
    :param date_end: date de FIN du sprint à optimiser, au format ISO. example : "2022-10-10T18:30:00.000Z"
    :param key_project_prioritys_projets: dictionnaire de la forme {id_projet (int):niveau_key_project_priority_projet (int)}.
                             Niveau le plus important: 0.

    :return df_imp:
        TODO: à compléter

    :return df_hor: dataframe contenant les horaires des utilisateurs
        epu_sfkutilisateur  -> id de l'utilisateur
        "epl_xdebutperiode"   -> debut de période d'application de l'horaire
        "epl_xfinperiode"     -> fin de période d'application de l'horaire
        key_epl_employe_horaire -> horaire de l'employe

    :return df_tsk:
        duree_evenement          -> duree (en h) de la tâche
        evenement    -> id de la tâche
        competence  -> utilisateur concerné # TODO: corriger clé
        evenement_project       -> projet de rattachement de la tâche
    """
    sql_querys_dict = {
        "imperatifs": {
            "select": [
                key_evenement,
                key_evenement_project,
                key_duree_evenement,
                key_competence,  # TODO : à remplacer par clé utilisateur
                "evt_xdate_debut",
                "evt_xdate_fin",
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
                    {
                        "condition": "or",
                        "rules": [
                            {
                                "label": "ecu_idsystem",
                                "field": "ecu_idsystem",
                                "operator": "equal",
                                "type": "integer",
                                "value": 1,
                            },
                            {
                                "label": "ecu_idsystem",
                                "field": "ecu_idsystem",
                                "operator": "equal",
                                "type": "integer",
                                "value": 2,
                            },
                        ],
                    },
                ],
            },
        },
        "horaires": {
            "select": [
                key_epu_sfkutilisateur,
                key_epl_employe_horaire,
                "epl_xdebutperiode",
                "epl_xfinperiode",
            ],
            "from": "lst_vutilisateur_horaires_py",
            "where": {
                "condition": "and",
                "rules": [
                    {
                        "label": "epl_xdebutperiode",
                        "field": "epl_xdebutperiode",
                        "operator": "lessthan",
                        "type": "date",
                        "value": f"{date_end}",
                    },
                    {
                        "label": "epl_xfinperiode",
                        "field": "epl_xfinperiode",
                        "operator": "greaterthan",
                        "type": "date",
                        "value": f"{date_start}",
                    },
                ],
            },
        },
        "taches": {
            "select": [
                key_evenement,
                key_evenement_project,
                key_duree_evenement,
                key_competence,  # TODO : à remplacer par clé utilisateur
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

    data = make_sql_requests(sql_querys_dict, url, access_token)

    # Mise en forme des données
    df_imp = pd.DataFrame(data["imperatifs"])
    df_hor = pd.DataFrame(data["horaires"]).reindex(
        columns=[
            key_epu_sfkutilisateur,
            "epl_xdebutperiode",
            "epl_xfinperiode",
            key_epl_employe_horaire,
        ]
    )
    df_hor.epl_xdebutperiode = pd.to_datetime(df_hor.epl_xdebutperiode).dt.date
    df_hor.epl_xfinperiode = pd.to_datetime(df_hor.epl_xfinperiode).dt.date
    df_hor = df_hor.sort_values(
        by=[key_epu_sfkutilisateur, "epl_xdebutperiode"]
    ).reset_index(drop=True)
    df_tsk = pd.DataFrame(data["taches"])

    imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires = filtre(
        df_imp, df_hor, df_tsk, key_project_prioritys_projets
    )
    return imperatifs, horaires, taches, utilisateurs_avec_taches_sans_horaires
