"""Request builder for matrice compétence in Task Assigner"""
from api.string_keys import *


def get_matrice_competence_request(selected_users: list[int] | None = None):
    """Request builder for matrice compétence in Task Assigner"""
    sql_request = {"select": [key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau],
                   "from": "lst_vcompetence_py",
                   }
    if selected_users is not None:
        sql_request["where"] = {"condition": "and",
                                "rules": []}
        sql_request["where"]["rules"].append({
            "label": key_emc_sfkutilisateur,
            "field": key_emc_sfkutilisateur,
            "operator": "in",
            "type": "number",
            "value": selected_users
        }
        )

    return sql_request
