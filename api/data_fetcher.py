import requests

from api.tools import return_json
from fastapi import HTTPException


def get_data_task_assigner(
    access_token: str, datein_isoformat: str, dateout_isoformat: str, url: str
) -> dict:
    data = {}
    sql_querys_dict = {
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

    headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}

    for key, sql_query in sql_querys_dict.items():
        request = requests.post(url, headers=headers, json=sql_query)
        if request.status_code != 200:
            # TODO: add controller
            raise HTTPException(
                status_code=424,
                detail=f"Erreur lors de la récupération des données auprès du BACK: {key}.",
                headers={
                    "status_code_BACK": str(request.status_code),
                    "sql_query_to_BACK": return_json(sql_query),
                },
            )
        else:
            data[key] = request.json()["result"]
    return data


def get_data_planning_optimizer(
    access_token: str, datein_isoformat: str, dateout_isoformat: str, url: str
) -> dict:
    """
    Prépare et envoie les requêtes SQL auprès du Back Wandeed qui renvoie les données demandées.
    """
    data = {}
    sql_querys_dict = {
        "imperatifs": {
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
                "epu_sfkutilisateur",
                "epl_employe_horaire",
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
                        "value": f"{dateout_isoformat}",
                    },
                    {
                        "label": "epl_xfinperiode",
                        "field": "epl_xfinperiode",
                        "operator": "greaterthan",
                        "type": "date",
                        "value": f"{datein_isoformat}",
                    },
                ],
            },
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

    headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}

    for key, sql_query in sql_querys_dict.items():
        request = requests.post(url, headers=headers, json=sql_query)
        if request.status_code != 200:
            raise HTTPException(
                status_code=424,
                detail=f"Erreur lors de la récupération des données auprès du BACK: {key}.",
                headers={
                    "status_code_BACK": str(request.status_code),
                    "sql_query_to_BACK": return_json(sql_query),
                },
            )
        else:
            data[key] = request.json()["result"]
    return data
