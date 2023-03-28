"""Contient la requête pour récupérer les horaires"""
from api.string_keys import *


def get_request_horaires(date_start: str, date_end: str):
    """Retourne la requête pour récupérer les horaires"""
    return {
            "select": LIST_FIELD_KEYS_HORAIRES_REQUEST,
            "from": key_table_horaires_utilisateurs,
            "where": {
                "condition": "and",
                "rules": [
                    {
                        "label": key_debut_periode_horaire_utilisateur,
                        "field": key_debut_periode_horaire_utilisateur,
                        "operator": "lessthan",
                        "type": "date",
                        "value": f"{date_end}",
                    },
                    {
                        "label": key_fin_periode_horaire_utilisateur,
                        "field": key_fin_periode_horaire_utilisateur,
                        "operator": "greaterthan",
                        "type": "date",
                        "value": f"{date_start}",
                    },
                ],
            },
        }