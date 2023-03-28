"""
Module de test de récupération des données pour le Planinng Optimizer
"""
import unittest
import requests
from datetime import datetime, timedelta
from api.back_connector.planning_optimizer.planning_optimizer import fetch_data_to_wandeed_backend
from api.back_connector.tools import make_sql_requests
from api.back_connector.planning_optimizer.requests import get_request_tasks, get_request_imperatifs, get_request_horaires


class TestRecuperationDataPlanningOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        self.access_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLQ01VZlkwNDZJSF9vOFo2SmUzaUF2cTRXc21yQkFrdGRTU18wZjNzMmlzIn0.eyJleHAiOjE2ODAwMzMxNTksImlhdCI6MTY4MDAxNTE1OSwiYXV0aF90aW1lIjoxNjgwMDEyMTUzLCJqdGkiOiIyM2MxNTFjNC1lNzlmLTQ4YzItYWFmOS1jMWE4ZjA1NGQ2MWUiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIyZGI0YTA2NS1hNjhkLTRlOWUtOTFmNC1lZGE5ZTczYWE4ZjAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiMTc5MTdkMDItZDNmZi00ODE3LThhZGItN2M3ZjBhYzUwNzQzIiwic2Vzc2lvbl9zdGF0ZSI6IjU1N2QzYjk5LTRhNzItNDlmNi05ZjRhLTVhYTFjMjM4NTQ3NyIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiI1NTdkM2I5OS00YTcyLTQ5ZjYtOWY0YS01YWExYzIzODU0NzciLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjUsInV0bF9jcHJlbm9tIjoiZ2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXRsX3V0aWxpc2F0ZXVyX3JvbGVzIjoiWzEsIDIsIDMsIDQsIDddIiwidXRsX3NhcHBhcnRlbmFuY2UiOlsyXSwidXRsX2Nub20iOiJwZXRpdCIsInByZWZlcnJlZF91c2VybmFtZSI6ImdheWxvcmQucGV0aXRAdGVhbWJlci5mciIsImdpdmVuX25hbWUiOiJnYXlsb3JkIiwidXRsX3Nma2luc3RhbmNlIjoxLCJ1dGxfc2FkbWluaXN0cmVyIjpbXSwibmFtZSI6ImdheWxvcmQgcGV0aXQiLCJ1dGxfc2Ryb2l0c2FjY2VzIjpbMyw0LDUsNiw3LDgsOV0sImZhbWlseV9uYW1lIjoicGV0aXQiLCJlbWFpbCI6ImdheWxvcmQucGV0aXRAdGVhbWJlci5mciIsInVzZXJfZ3JvdXBzIjpbMiwzLDQsNSw2LDcsOCw5XX0.K_-8XPYtQN2fUg43rzlO9pUlK51BFLv2mWOiemMbvG4M6631MiVwwq4Sm9vwpv6ij8paT5ZQ8qJjuuMeAeoUdNd5FKGdViERtr-ovn0WZTwAueqcrWjI8D2Y-pWXvqIumVb-uZIoPPQMFOW1mzvoiRexBzOslxCQL85MZWa_KijH5prurHPdKk3z7iHlGLSnba-Utx8KPITKdrmAUn8_mtMH8VLMY7yjW2_Q8NKFiF2zYkxyquoTiRdfvt1wSdtRHn2eRVIBZZc4-6FAWmZO9ABRFr7diY-gRnTvjQJKdd2-MHkviqxbOKhCN1JJffslRds5phCffXYldj-X7h45qw"
        self.url = "https://development.api.wandeed.com/api/lst/search?offset=0&limit=500"
    def test_simple(self):
        url ="https://development.api.wandeed.com/api/agrp/1"
        headers = {"Authorization": f"{self.access_token}", "Content-Type": "application/json"}
        r = requests.get(url=url, headers=headers)
        self.assertEqual(200, r.status_code)

    def test_request_tasks(self):
        """Teste l'exécution de la requête de récupération des tâches auprès du back wandeed pour la fonction PO"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        sql_request = get_request_tasks(date_start=date_start, date_end=date_end)
        make_sql_requests(sql_queries={"test_query_tasks":sql_request},
                          url=self.url,
                          access_token=self.access_token)

    def test_request_horaires(self):
        """Teste l'exécution de la requête de récupération des horaires auprès du back wandeed pour la fonction PO"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        sql_request = get_request_horaires(date_start=date_start, date_end=date_end)
        make_sql_requests(sql_queries={"test_query_horaires":sql_request},
                          url=self.url,
                          access_token=self.access_token)

    def test_request_imperatifs(self):
        """Teste l'exécution de la requête de récupération des imperatifs auprès du back wandeed pour la fonction PO"""
        date_end = datetime.now()
        date_start = date_end - timedelta(weeks=4)
        sql_request = get_request_imperatifs(date_start=date_start, date_end=date_end)
        make_sql_requests(sql_queries={"test_query_imperatifs":sql_request},
                          url=self.url,
                          access_token=self.access_token)
