"""Request builder for matrice projet in Task Assigner"""
from api.string_keys import *


def get_matrice_projet_request():
    """Request builder for matrice projet in Task Assigner"""
    return {"select": [key_user, key_project],
            "from": "lst_vprojet_utilisateur_py"}
