"""
Module de test de récupération des données pour le Planinng Optimizer
"""
import unittest
import requests
from datetime import datetime, timedelta
from api.back_connector.tools import make_sql_requests, to_iso_8601, FailRecuperationBackendDataException
from api.back_connector.planning_optimizer.requests import get_request_tasks, get_request_imperatifs, get_request_horaires


class TestRecuperationDataPlanningOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        """setup de l'url et du token"""
        self.access_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLQ01VZlkwNDZJSF9vOFo2SmUzaUF2cTRXc21yQkFrdGRTU18wZjNzMmlzIn0.eyJleHAiOjE2ODAzMDc4ODMsImlhdCI6MTY4MDI4OTg4MywiYXV0aF90aW1lIjoxNjgwMjg5ODc3LCJqdGkiOiJmNjRjYTNkMS0zNzVjLTQ4MjQtYThmOC0wNDg1ZTJjZDU4YWEiLCJpc3MiOiJodHRwczovL2RldmVsb3BtZW50LmF1dGgud2FuZGVlZC5jb20vYXV0aC9yZWFsbXMvd2FuZGVlZC1yZWFsbSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiIyZGI0YTA2NS1hNjhkLTRlOWUtOTFmNC1lZGE5ZTczYWE4ZjAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ3YW5kZWVkLWNsaWVudCIsIm5vbmNlIjoiZDIyYjA4NjYtOWE5OC00NGUxLWEwM2UtZGM2NGRhZDY2YjgzIiwic2Vzc2lvbl9zdGF0ZSI6ImFhZmZkMGQ0LWRhMGItNGEyNi1hZDFhLTM4NjkxYjA5MDFiMSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8qLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXBpLndhbmRlZWQuY29tLyoiLCIqIiwiaHR0cHM6Ly8qLmFkbWluLndhbmRlZWQuY29tLyoiLCJodHRwczovLyouYXV0aC53YW5kZWVkLmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy13YW5kZWVkLXJlYWxtIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiJhYWZmZDBkNC1kYTBiLTRhMjYtYWQxYS0zODY5MWIwOTAxYjEiLCJ1dGxfc3BrdXRpbGlzYXRldXIiOjUsInV0bF9jcHJlbm9tIjoiZ2F5bG9yZCIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwidXRsX3V0aWxpc2F0ZXVyX3JvbGVzIjoiWzIsIDEsIDMsIDksIDEyLCAxM10iLCJ1dGxfc2FwcGFydGVuYW5jZSI6WzJdLCJ1dGxfY25vbSI6InBldGl0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwiZ2l2ZW5fbmFtZSI6ImdheWxvcmQiLCJ1dGxfc2ZraW5zdGFuY2UiOjEsInV0bF9zYWRtaW5pc3RyZXIiOltdLCJuYW1lIjoiZ2F5bG9yZCBwZXRpdCIsInV0bF9zZHJvaXRzYWNjZXMiOlszLDQsNSw2LDcsOCw5XSwiZmFtaWx5X25hbWUiOiJwZXRpdCIsImVtYWlsIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwidXNlcl9ncm91cHMiOlsyLDMsNCw1LDYsNyw4LDldfQ.UPhPqx6x2srPRI2pIGsVeppVjrDUv34-5uSW5dgaEV-gYlrH2408ASgEkPFzIWqglCE4Fz33s_ldn7-hV_2_HjC1Z0OpNzoHzzPnaCFtpeoM9SDKWhDGJouC0W46Vcr5qeA2R-b7jv0UaeuCY37BS89dd7GE3JoFexkirNTQxot3XLjY3qC6blQHmdraQ7yLQg_Udoenhre3od0lpfoggPcW630kEf-LJC7coUCcwYi_fr8a8mz4bOaRZ3T97hbFUP0IPv3t7HEjtQSgwhXFju_zLIkXPb_T-qn2OYlYzMdw9wSgTy2uhUtSGJHuYyIwRmz3uaH25faUruYZtEkzgw"
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
        url ="https://development.api.wandeed.com/api/agrp/1"
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
