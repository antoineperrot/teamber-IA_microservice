"""Contient la requête pour récupérer les horaires"""
from typing import Optional
from api.string_keys import *


def get_request_horaires(date_start: str, date_end: str, users: Optional[list[int]] = None) -> dict:
    """Retourne la requête pour récupérer les horaires"""
    sql_request = {
        "select": [
            key_epu_sfkutilisateur,
            key_epl_employe_horaire,
            key_debut_periode_horaire_utilisateur,
            key_fin_periode_horaire_utilisateur,
        ],
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

    if users is not None:
        sql_request["where"]["rules"].append({
            "label": key_epu_sfkutilisateur,
            "field": key_epu_sfkutilisateur,
            "operator": "in",
            "type": "number",
            "value": users
        }
        )
    return sql_request
