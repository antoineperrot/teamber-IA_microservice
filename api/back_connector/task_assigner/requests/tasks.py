"""Request builder for tasks in Task Assigner"""
from api.string_keys import *


def get_tasks_request(date_start: str, date_end: str):
    """Request builder for tasks in Task Assigner"""
    return {"select": [
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
        }
