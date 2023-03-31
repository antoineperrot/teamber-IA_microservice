"""Request builder for tasks in Task Assigner"""
from api.string_keys import *


def get_tasks_request(date_start: str, date_end: str, selected_users: list[int] | None = None):
    """Request builder for tasks in Task Assigner"""

    sql_request = {"select": [
        key_evenement,
        key_evenement_project,
        key_duree_evenement,
        key_competence,
        key_user_po,
        key_evenement_date_debut,
        key_evenement_date_fin
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
            ]}
    }
    if selected_users is not None:
        sql_request["where"] = {"condition": "and",
                                "rules": []}
        sql_request["where"]["rules"].append({
            "label": key_user_po,
            "field": key_user_po,
            "operator": "in",
            "type": "number",
            "value": selected_users
        }
        )

    return sql_request
