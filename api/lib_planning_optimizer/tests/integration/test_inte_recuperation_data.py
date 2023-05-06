"""
Module de test de récupération des données pour le Planinng Optimizer
"""
import requests
from datetime import datetime, timedelta
from api.tools import run_test_integration, TestIntegration
from api.back_connector.tools import make_sql_requests, to_iso_8601, FailRecuperationBackendDataException
from api.back_connector.planning_optimizer.requests import get_request_tasks, get_request_imperatifs,\
    get_request_horaires


class TestRecuperationDataPlanningOptimizer(TestIntegration):
    def _test_request(self, request_builder: callable, test_name: str):
        """teste une requête de récupération des données"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        sql_request = request_builder(to_iso_8601(date_start), to_iso_8601(date_end))

        success = True
        try:
            data = make_sql_requests(sql_queries={"test_" + test_name: sql_request},
                                     url=self.url,
                                     access_token=self.access_token)
        except FailRecuperationBackendDataException:
            success = False

        self.assertTrue(success, msg=f"Le test de récupération {test_name} a fail")

    def _test_request_selected_users(self, request_builder: callable, test_name: str):
        """teste une requête de récupération des données"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        selected_users = None
        sql_request = request_builder(to_iso_8601(date_start), to_iso_8601(date_end), selected_users)

        success = True
        try:
            data = make_sql_requests(sql_queries={"test_" + test_name: sql_request},
                                     url=self.url,
                                     access_token=self.access_token)
        except FailRecuperationBackendDataException:
            success = False

        self.assertTrue(success, msg=f"Le test de récupération {test_name} a fail")

    def _test_inte_simple(self):
        url = "https://antoine.api.wandeed.com/api/agrp/1"
        headers = {"Authorization": f"{self.access_token}", "Content-Type": "application/json"}
        r = requests.get(url=url, headers=headers)
        self.assertEqual(200, r.status_code)

    def test_inte_request_tasks(self):
        """Teste l'exécution de la requête de récupération des tâches auprès du back wandeed pour la fonction PO"""
        self._test_request(request_builder=get_request_tasks, test_name="tâches pour Planning optimizer")
        self._test_request_selected_users(request_builder=get_request_tasks,
                                          test_name="tâches pour Planning optimizer with selected_users")

    def test_inte_request_horaires(self):
        """Teste l'exécution de la requête de récupération des horaires auprès du back wandeed pour la fonction PO"""
        self._test_request(request_builder=get_request_horaires, test_name="horaires pour Planning optimizer")
        self._test_request_selected_users(request_builder=get_request_horaires,
                                          test_name="horaires pour Planning optimizer with selected_users")

    def test_inte_request_imperatifs(self):
        """Teste l'exécution de la requête de récupération des imperatifs auprès du back wandeed pour la fonction PO"""
        self._test_request(request_builder=get_request_imperatifs, test_name="impératifs pour Planning optimizer")
        self._test_request_selected_users(request_builder=get_request_imperatifs,
                                          test_name="impératifs pour Planning optimizer with selected_users")


test = TestRecuperationDataPlanningOptimizer()
test.setUp()
if test.commandline:
    run_test_integration(test_integration=test)
