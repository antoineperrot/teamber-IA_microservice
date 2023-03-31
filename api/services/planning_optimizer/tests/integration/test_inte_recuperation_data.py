"""
Module de test de récupération des données pour le Planinng Optimizer
"""
import unittest
import sys
import requests
from datetime import datetime, timedelta
from api.tools import run_test_inte
from api.back_connector.tools import make_sql_requests, to_iso_8601, FailRecuperationBackendDataException
from api.back_connector.planning_optimizer.requests import get_request_tasks, get_request_imperatifs,\
    get_request_horaires

access_token = str(sys.argv[1])
print(f"\nAccess token: {access_token}\n\n")


class TestRecuperationDataPlanningOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        """setup de l'url et du token"""

        self.access_token = access_token
        self.url = "https://development.api.wandeed.com/api/lst/search?offset=0&limit=500"

    def _test_request(self, request_builder: callable, test_name: str):
        """teste une requête de récupération des données"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        sql_request = request_builder(to_iso_8601(date_start), to_iso_8601(date_end))

        success = True
        try:
            make_sql_requests(sql_queries={"test_query_tasks": sql_request},
                              url=self.url,
                              access_token=self.access_token)
        except FailRecuperationBackendDataException:
            success = False

        self.assertTrue(success, msg=f"Le test de récupération {test_name} a fail")

    def test_inte_simple(self):
        url = "https://development.api.wandeed.com/api/agrp/1"
        headers = {"Authorization": f"{self.access_token}", "Content-Type": "application/json"}
        r = requests.get(url=url, headers=headers)
        self.assertEqual(200, r.status_code)

    def test_inte_request_tasks(self):
        """Teste l'exécution de la requête de récupération des tâches auprès du back wandeed pour la fonction PO"""
        self._test_request(request_builder=get_request_tasks, test_name="tâches pour Planning optimizer")

    def test_inte_request_horaires(self):
        """Teste l'exécution de la requête de récupération des horaires auprès du back wandeed pour la fonction PO"""
        self._test_request(request_builder=get_request_horaires, test_name="horaires pour Planning optimizer")

    def test_inte_request_imperatifs(self):
        """Teste l'exécution de la requête de récupération des imperatifs auprès du back wandeed pour la fonction PO"""
        self._test_request(request_builder=get_request_imperatifs, test_name="impératifs pour Planning optimizer")


test = TestRecuperationDataPlanningOptimizer()
run_test_inte(test)
