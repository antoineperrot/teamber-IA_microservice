"""Request builder for tasks in Task Assigner"""
from api.string_keys import *


def get_tasks_request(date_start: str, date_end: str):
    """Request builder for tasks in Task Assigner"""
    return {"select": [
        key_evenement,
        key_evenement_project,
        key_duree_evenement,
        #key_competence
    ],
        "from": key_table_evenements,
    }
