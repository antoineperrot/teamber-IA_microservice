"""Request builder for matrice compétence in Task Assigner"""
from typing import Optional
from api.string_keys import *


def get_matrice_competence_request(selected_competences: Optional[list[int]] = None,
                                   selected_users: Optional[list[int]] = None):
    """Request builder for matrice compétence in Task Assigner"""
    sql_request = {"select": [key_emc_sfkutilisateur, key_emc_sfkarticle, key_emc_sniveau],
                   "from": "lst_vcompetence_py",
                   "where":
                       {
                        "condition": "and",
                        "rules": [
                            {
                                "label": key_emc_sfkutilisateur,
                                "field": key_emc_sfkutilisateur,
                                "operator": "isnotnull",
                                "type": "integer",
                                "value": "none",
                            },
                            {
                                "label": key_emc_sfkarticle,
                                "field": key_emc_sfkarticle,
                                "operator": "isnotnull",
                                "type": "integer",
                                "value": "none",
                            },
                            {
                                "label": key_emc_sniveau,
                                "field": key_emc_sniveau,
                                "operator": "isnotnull",
                                "type": "integer",
                                "value": "none",
                            },
                            {
                                "label": key_emc_sniveau,
                                "field": key_emc_sniveau,
                                "operator": "greaterthan",
                                "type": "integer",
                                "value": 0,
                            }
                        ]
                       }
                   }
    if selected_competences is not None:
        sql_request["where"]["rules"].append({
            "label": key_emc_sfkarticle,
            "field": key_emc_sfkarticle,
            "operator": "in",
            "type": "integer",
            "value": selected_competences
        }
        )
    if selected_users is not None:
        sql_request["where"]["rules"].append({
            "label": key_emc_sfkutilisateur,
            "field": key_emc_sfkutilisateur,
            "operator": "in",
            "type": "integer",
            "value": selected_users
        }
        )

    return sql_request
