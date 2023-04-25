"""
Module tools du back connector
"""
import datetime

import requests
from api.loggers import root_logger


class FailRecuperationBackendDataException(Exception):
    """Exception à lever lorsque la récupération de données échoue"""
    def __init__(self, missing_data):
        self.msg = f"Erreur lors de la récupération des données auprès du BACK: {missing_data}."

    def __repr__(self):
        return self.msg


def make_sql_requests(sql_queries: dict, url: str, access_token: str) -> dict:
    """
    :param sql_queries: dictionnaire de la forme {nom_requete: requete_sql}
    :param url: url de la base de données du back
    :param access_token: token d'accès à la base de données du back
    """
    headers = {"Authorization": f"{access_token}", "Content-Type": "application/json"}
    fetched_data = {}
    for key, sql_query in sql_queries.items():

        request = requests.post(url, headers=headers, json=sql_query)
        if request.status_code != 200:
            root_logger.warning(f"Backend Data Recupération :  récupération de {key}, "
                                f"code erreur requête {request.status_code}")
            raise FailRecuperationBackendDataException(missing_data=key)
        else:
            root_logger.info(f"Backend Data Recupération :  récupération de {key} - OK")
            fetched_data[key] = request.json()["result"]

    return fetched_data


def to_iso_8601(date: datetime.datetime) -> str:
    """Convert to isoformat YYYY-MM-DDTHH:MM:SS.mmmmmmZ"""
    date = date.replace(second=0, microsecond=0)
    out = date.isoformat()
    return out + ".000Z"
