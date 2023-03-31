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

print("\n\n========= DEBUT DU TEST =========")

commandline = True
access_token = ""
try:
    access_token = str(sys.argv[1])
except IndexError:
    commandline = False


class TestRecuperationDataTaskAssigner(unittest.TestCase):
    def setUp(self) -> None:
        """setup de l'url et du token"""
        self.access_token = access_token if commandline else "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLQ01VZlkwNDZJSF9vOFo2SmUzaUF2cTRXc21yQkFrdGRTU18wZjNzMmlzIn0.eyJleHAiOjE2ODAzMTUxNjUsImlhdCI6MTY4MDI5NzE2NSwiYXV0aF90aW1lIjoxNjgwMjg5ODc3LCJqdGkiOiIyMWQ5MzYwZi00MzRlLTRkZTktYWY1MC0zMDk2NDBlYWU3YWIiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIyZGI0YTA2NS1hNjhkLTRlOWUtOTFmNC1lZGE5ZTczYWE4ZjAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiMWU4YTIyMzUtZTg5MC00MjUwLTgzZTktOTBhMDNlNzUyMDQwIiwic2Vzc2lvbl9zdGF0ZSI6ImFhZmZkMGQ0LWRhMGItNGEyNi1hZDFhLTM4NjkxYjA5MDFiMSIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiJhYWZmZDBkNC1kYTBiLTRhMjYtYWQxYS0zODY5MWIwOTAxYjEiLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjUsInV0bF9jcHJlbm9tIjoiZ2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXRsX3V0aWxpc2F0ZXVyX3JvbGVzIjoiWzIsIDEsIDMsIDksIDEyLCAxM10iLCJ1dGxfc2FwcGFydGVuYW5jZSI6WzJdLCJ1dGxfY25vbSI6InBldGl0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwiZ2l2ZW5fbmFtZSI6ImdheWxvcmQiLCJ1dGxfc2ZraW5zdGFuY2UiOjEsInV0bF9zYWRtaW5pc3RyZXIiOltdLCJuYW1lIjoiZ2F5bG9yZCBwZXRpdCIsInV0bF9zZHJvaXRzYWNjZXMiOlszLDQsNSw2LDcsOCw5XSwiZmFtaWx5X25hbWUiOiJwZXRpdCIsImVtYWlsIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwidXNlcl9ncm91cHMiOlsyLDMsNCw1LDYsNyw4LDldfQ.YY_sMT5Vc6IQnBEVrSfymgX_8mGLxzeVwwj1hyMQs-mSZ-lm0OPg3RA2gqy5UHdK3-R3qy3go04JNXoOjPr1PMzkHyrVavFYVk6d1S0C0uA4rNmD4JSrmOXO4efoCoN6REgT0j2beVqwf89mTYr5eOrulQAG88GFrfRlm_J5NIb1VofRUym8ihIeMr5EXOP2YeH9l3Kx6wg6XnTw5A3N5-7tXRySMDq7FCua4EBrDlVsSIHH1y3FyxaAJwu8T4ae3fvNE3RtpgiHUIBFS8xwouSPYTOdZ08-zMk0E-usjkbKuqzNWZrrDdCXKUXiAxCFIOCOlFKyZc_SwJDezfJy2w"
        self.url = "https://development.api.wandeed.com/api/lst/search?offset=0&limit=500"

    def _test_request(self, request_builder: callable, test_name: str, **kwargs):
        """teste une requête de récupération des données"""
        sql_request = request_builder(**kwargs)

        success = True
        try:
            make_sql_requests(sql_queries={"test_" + test_name: sql_request},
                              url=self.url,
                              access_token=self.access_token)
            print("-" * 5, f"SUCCESS {test_name}")
        except FailRecuperationBackendDataException:
            print("-" * 5, f"FAIL    {test_name}")
            success = False

        self.assertTrue(success, msg=f"Le test de récupération {test_name} a fail")

    def _test_request_selected_users(self, request_builder: callable, test_name: str, **kwargs):
        """teste une requête de récupération des données"""
        kwargs["selected_users"] = [3, 4, 5, 8]
        sql_request = request_builder(**kwargs)

        success = True
        try:
            data = make_sql_requests(sql_queries={"test_query_tasks": sql_request},
                                     url=self.url,
                                     access_token=self.access_token)
            print("-" * 5, f"SUCCESS {test_name}")
        except FailRecuperationBackendDataException:
            print("-" * 5, f"FAIL    {test_name}")
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
                           date_start=to_iso_8601(date_start),
                           date_end=to_iso_8601(date_end), )
        self._test_request_selected_users(request_builder=get_tasks_request,
                                          test_name="tâches pour Task Assigner with selected_users",
                                          date_start=to_iso_8601(date_start),
                                          date_end=to_iso_8601(date_end), )

    def test_inte_request_matrice_projet(self):
        """Teste l'exécution de la requête de récupération de la matrice projet auprès du back wandeed pour la fonction
         TA"""
        self._test_request(request_builder=get_matrice_projet_request,
                           test_name="matrice projet pour Task Assigner")
        self._test_request_selected_users(request_builder=get_matrice_projet_request,
                                          test_name="matrice projet pour Task Assigner with selected_users")

    def test_inte_request_matrice_competence(self):
        """Teste l'exécution de la requête de récupération de la matrice compétence auprès du back wandeed pour
         la fonction TA"""
        self._test_request(request_builder=get_matrice_competence_request,
                           test_name="matrice compétence pour Task Assigner")
        self._test_request_selected_users(request_builder=get_matrice_competence_request,
                                          test_name="matrice compétence pour Task Assigner with selected_users")

    def test_inte_request_dispos_users(self):
        """Teste l'exécution de la requête de récupération de la matrice compétence auprès du back wandeed pour
         la fonction TA"""
        self._test_request(request_builder=get_dispo_user_request,
                           test_name="indispos users pour Task Assigner")
        self._test_request_selected_users(request_builder=get_dispo_user_request,
                                          test_name="indispos users pour Task Assigner with selected_users")


if commandline:
    test = TestRecuperationDataTaskAssigner()
    run_test_inte(test)

print("========= FIN DU TEST =========")
