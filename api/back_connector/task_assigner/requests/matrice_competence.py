"""Request builder for matrice compétence in Task Assigner"""
from api.string_keys import *


def get_matrice_competence_request():
    """Request builder for matrice compétence in Task Assigner"""
    return {"select": [key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau],
            "from": "lst_vcompetence_py",
            }
