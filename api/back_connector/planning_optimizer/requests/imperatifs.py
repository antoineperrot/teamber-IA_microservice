"""Contient la requête pour récupérer les imperatifs"""
from typing import Optional
from api.string_keys import *


def get_request_imperatifs(date_start: str, date_end: str, selected_users: Optional[list[int]] = None) -> dict:
    """Retourne la requête pour récupérer les imperatifs"""
    sql_request = {
            "select": [
                key_evenement,
                key_evenement_project,
                key_duree_evenement,
                key_user_po,
                key_evenement_date_debut,
                key_evenement_date_fin,
            ],
            "from": key_table_evenements,
            "where": {
                "condition": "and",
                "rules": [
                    {
                        "label": key_evenement_date_debut,
                        "field": key_evenement_date_debut,
                        "operator": "greaterthan",
                        "type": "date",
                        "value": f"{date_start}",
                    },
                    {
                        "label": key_evenement_date_fin,
                        "field": key_evenement_date_fin,
                        "operator": "lessthan",
                        "type": "date",
                        "value": f"{date_end}",
                    },
                    {
                        "label": key_user_po,
                        "field": key_user_po,
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
        }

    if selected_users is not None:
        sql_request["where"]["rules"].append({
            "label": key_user_po,
            "field": key_user_po,
            "operator": "in",
            "type": "number",
            "value": selected_users
        }
        )

    return sql_request
