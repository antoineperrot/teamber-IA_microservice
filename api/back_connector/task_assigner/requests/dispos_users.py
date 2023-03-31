"""Request builder for dispos users in Task Assigner"""
from api.string_keys import *


def get_dispo_user_request(selected_users: list[int] | None = None):
    """Request builder for dispos users in Task Assigner"""
    sql_request = {"select": [key_user, key_user_dispo],
                   "from": "lst_vdispo_py", }

    if selected_users is not None:
        sql_request["where"] = {"condition": "and",
                                "rules": []}
        sql_request["where"]["rules"].append({
            "label": key_user,
            "field": key_user,
            "operator": "in",
            "type": "number",
            "value": selected_users
        }
        )

    return sql_request

