"""
Module de test de récupération des données pour le Task Assigner
"""
import sys
import unittest
import requests
from datetime import datetime, timedelta

from api.tools import run_test_inte
from api.back_connector.task_assigner.requests import get_tasks_request, get_matrice_projet_request, \
    get_matrice_competence_request, get_dispo_user_request
from api.back_connector.tools import make_sql_requests, to_iso_8601, FailRecuperationBackendDataException


access_token = str(sys.argv[1])
print(f"\nAccess token: {access_token}\n\n")


class TestRecuperationDataTaskAssigner(unittest.TestCase):
    def setUp(self) -> None:
        """setup de l'url et du token"""
        self.access_token = access_token
        self.url = "https://development.api.wandeed.com/api/lst/search?offset=0&limit=500"

    def _test_request(self, request_builder: callable, test_name: str, **kwargs):
        """teste une requête de récupération des données"""
        sql_request = request_builder(**kwargs)

        success = True
        try:
            make_sql_requests(sql_queries={"test_" + test_name: sql_request},
                              url=self.url,
                              access_token=self.access_token)
        except FailRecuperationBackendDataException:
            success = False

        self.assertTrue(success, msg=f"Le test de récupération {test_name} a fail")

    def test_inte_simple(self):
        """Test un ping secure simple"""
        url = "https://development.api.wandeed.com/api/agrp/1"
        headers = {"Authorization": f"{self.access_token}", "Content-Type": "application/json"}
        r = requests.get(url=url, headers=headers)
        self.assertEqual(200, r.status_code)

    def test_inte_request_tasks(self):
        """Teste l'exécution de la requête de récupération des tâches auprès du back wandeed pour la fonction TA"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        self._test_request(request_builder=get_tasks_request,
                           test_name="tâches pour Task Assigner",
                           date_start=to_iso_8601(date_start), date_end=to_iso_8601(date_end), )

    def test_inte_request_matrice_projet(self):
        """Teste l'exécution de la requête de récupération de la matrice projet auprès du back wandeed pour la fonction
         TA"""
        self._test_request(request_builder=get_matrice_projet_request,
                           test_name="horaires pour Task Assigner")

    def test_inte_request_matrice_competence(self):
        """Teste l'exécution de la requête de récupération de la matrice compétence auprès du back wandeed pour
         la fonction TA"""
        self._test_request(request_builder=get_matrice_competence_request,
                           test_name="matrice compétence pour Task Assigner")

    def test_inte_request_dispos_users(self):
        """Teste l'exécution de la requête de récupération de la matrice compétence auprès du back wandeed pour
         la fonction TA"""
        self._test_request(request_builder=get_dispo_user_request,
                           test_name="matrice compétence pour Task Assigner")


test = TestRecuperationDataTaskAssigner()
run_test_inte(test)
