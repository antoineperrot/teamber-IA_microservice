"""
Module de test de récupération des données pour le Task Assigner
"""
import unittest
import requests
from datetime import datetime, timedelta
from api.back_connector.tools import make_sql_requests, to_iso_8601, FailRecuperationBackendDataException
from api.back_connector.task_assigner.requests import get_tasks_request, get_matrice_projet_request, \
    get_matrice_competence_request, get_dispo_user_request


class TestRecuperationDataTaskAssigner(unittest.TestCase):
    def setUp(self) -> None:
        """setup de l'url et du token"""
        self.access_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLQ01VZlkwNDZJSF9vOFo2SmUzaUF2cTRXc21yQkFrdGRTU18wZjNzMmlzIn0.eyJleHAiOjE2ODAwMzMxNTksImlhdCI6MTY4MDAxNTE1OSwiYXV0aF90aW1lIjoxNjgwMDEyMTUzLCJqdGkiOiIyM2MxNTFjNC1lNzlmLTQ4YzItYWFmOS1jMWE4ZjA1NGQ2MWUiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIyZGI0YTA2NS1hNjhkLTRlOWUtOTFmNC1lZGE5ZTczYWE4ZjAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiMTc5MTdkMDItZDNmZi00ODE3LThhZGItN2M3ZjBhYzUwNzQzIiwic2Vzc2lvbl9zdGF0ZSI6IjU1N2QzYjk5LTRhNzItNDlmNi05ZjRhLTVhYTFjMjM4NTQ3NyIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiI1NTdkM2I5OS00YTcyLTQ5ZjYtOWY0YS01YWExYzIzODU0NzciLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjUsInV0bF9jcHJlbm9tIjoiZ2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXRsX3V0aWxpc2F0ZXVyX3JvbGVzIjoiWzEsIDIsIDMsIDQsIDddIiwidXRsX3NhcHBhcnRlbmFuY2UiOlsyXSwidXRsX2Nub20iOiJwZXRpdCIsInByZWZlcnJlZF91c2VybmFtZSI6ImdheWxvcmQucGV0aXRAdGVhbWJlci5mciIsImdpdmVuX25hbWUiOiJnYXlsb3JkIiwidXRsX3Nma2luc3RhbmNlIjoxLCJ1dGxfc2FkbWluaXN0cmVyIjpbXSwibmFtZSI6ImdheWxvcmQgcGV0aXQiLCJ1dGxfc2Ryb2l0c2FjY2VzIjpbMyw0LDUsNiw3LDgsOV0sImZhbWlseV9uYW1lIjoicGV0aXQiLCJlbWFpbCI6ImdheWxvcmQucGV0aXRAdGVhbWJlci5mciIsInVzZXJfZ3JvdXBzIjpbMiwzLDQsNSw2LDcsOCw5XX0.K_-8XPYtQN2fUg43rzlO9pUlK51BFLv2mWOiemMbvG4M6631MiVwwq4Sm9vwpv6ij8paT5ZQ8qJjuuMeAeoUdNd5FKGdViERtr-ovn0WZTwAueqcrWjI8D2Y-pWXvqIumVb-uZIoPPQMFOW1mzvoiRexBzOslxCQL85MZWa_KijH5prurHPdKk3z7iHlGLSnba-Utx8KPITKdrmAUn8_mtMH8VLMY7yjW2_Q8NKFiF2zYkxyquoTiRdfvt1wSdtRHn2eRVIBZZc4-6FAWmZO9ABRFr7diY-gRnTvjQJKdd2-MHkviqxbOKhCN1JJffslRds5phCffXYldj-X7h45qw"
        self.url = "https://development.api.wandeed.com/api/lst/search?offset=0&limit=500"

    def _test_request(self, request_builder: callable, test_name: str, **kwargs):
        """teste une requête de récupération des données"""
        sql_request = request_builder(**kwargs)

        success = True
        try:
            make_sql_requests(sql_queries={"test_query_tasks": sql_request},
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
