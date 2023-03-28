"""Contient la requête pour récupérer les tâches"""
from api.string_keys import *


def get_request_tasks(date_start: str, date_end: str):
    """Retourne la requête pour récupérer les tâches"""
    return {"select": LIST_FIELD_KEYS_TACHES_REQUEST,
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
                ]}
            }
