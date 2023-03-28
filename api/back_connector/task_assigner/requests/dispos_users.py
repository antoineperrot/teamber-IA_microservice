"""Request builder for dispos users in Task Assigner"""
from api.string_keys import *


def get_dispo_user_request():
    """Request builder for dispos users in Task Assigner"""
    return {
            "select": [key_user, key_user_dispo],
            "from": "lst_vdispo_py",
        }
