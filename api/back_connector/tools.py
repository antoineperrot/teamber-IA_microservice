import requests


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
            # TODO: Add bonne exception
            raise ValueError(f"Erreur lors de la récupération des données auprès du BACK: {key}.")
        else:
            fetched_data[key] = request.json()["result"]

    return fetched_data

