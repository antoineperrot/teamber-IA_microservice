"""
Tools for the api
"""
import sys
from flask import request, abort
import unittest
from functools import wraps
from pandas import DataFrame
from api.config import config
from api.string_keys import *


def api_key_required(func):
    """
    View decorator - require valid api key
    Extract api-key information from authorization header
    authorization header has the following form: Bearer key
    """

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        """wrapper"""
        if request.headers:
            auth_header = request.headers.get("Authorization", None)

            if not auth_header:
                abort(401, "Missing Authorization header")

            if "Bearer" not in auth_header:
                abort(401, "Missing Authorization header")

            api_key = auth_header.replace("Bearer ", "")

            if api_key != config["FLASK_API_KEY"]:
                abort(401, "Invalid api-key")

        return func(*args, **kwargs)

    return wrapper_function


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        """set token et url"""
        self.commandline = True
        access_token = ""
        try:
            access_token = str(sys.argv[1])
            if "Bearer" not in access_token:
                self.commandline = False
        except IndexError:
            self.commandline = False
        self.access_token = access_token if self.commandline else "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLQ01VZlkwNDZJSF9vOFo2SmUzaUF2cTRXc21yQkFrdGRTU18wZjNzMmlzIn0.eyJleHAiOjE2ODIyNzY0MzUsImlhdCI6MTY4MjI1ODQzNSwiYXV0aF90aW1lIjoxNjgyMTc2MjUyLCJqdGkiOiJkNjI3ZjgxZi0yMzBmLTRiNmEtOTMyNC05NzAwOGRiMjdlZWUiLCJpc3MiOiJodHRwczovL2FudG9pbmUuYXV0aC53YW5kZWVkLmNvbS9hdXRoL3JlYWxtcy93YW5kZWVkLXJlYWxtIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjVkNDc5Y2QxLTgyZTUtNGI3Ni04ZGZjLTE0Y2Q4N2ZlOWIzMyIsInR5cCI6IkJlYXJlciIsImF6cCI6IndhbmRlZWQtY2xpZW50Iiwibm9uY2UiOiIyNzBiNTU4ZC0yMzU4LTRlNjAtYWY4OC0yMDQ1NDkwMWIxY2QiLCJzZXNzaW9uX3N0YXRlIjoiYzUwOGE1NzYtZjU4My00MjE1LTlmNzQtMjgwYzk3Nzc4ZjhhIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovLyoud2FuZGVlZC5jb20vKiIsImh0dHBzOi8vKi5hcGkud2FuZGVlZC5jb20vKiIsIioiLCJodHRwczovLyouYWRtaW4ud2FuZGVlZC5jb20vKiIsImh0dHBzOi8vKi5hdXRoLndhbmRlZWQuY29tIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLXdhbmRlZWQtcmVhbG0iLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsInNpZCI6ImM1MDhhNTc2LWY1ODMtNDIxNS05Zjc0LTI4MGM5Nzc3OGY4YSIsInV0bF9zcGt1dGlsaXNhdGV1ciI6Mjk2LCJ1dGxfY3ByZW5vbSI6IkdheWxvcmQiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwidXRsX3V0aWxpc2F0ZXVyX3JvbGVzIjoiWzFdIiwidXRsX3NhcHBhcnRlbmFuY2UiOlsxMjJdLCJ1dGxfY25vbSI6IlBFVElUIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZ2F5bG9yZC5wZXRpdEB0ZWFtYmVyLmZyIiwiZ2l2ZW5fbmFtZSI6IkdheWxvcmQiLCJ1dGxfc2ZraW5zdGFuY2UiOjEsInV0bF9zYWRtaW5pc3RyZXIiOltdLCJuYW1lIjoiR2F5bG9yZCBQRVRJVCIsInV0bF9zZHJvaXRzYWNjZXMiOlsxMjAsMTIzLDEyNSwxMjYsMTI3LDIyMiwyNjQsMjY1LDI2NiwyNjcsMjY4LDI3MSwyNzIsMjczLDI3NCwyNzUsMjc2LDI3NywyNjksMjcwLDI4MSwyODJdLCJmYW1pbHlfbmFtZSI6IlBFVElUIiwiZW1haWwiOiJnYXlsb3JkLnBldGl0QHRlYW1iZXIuZnIiLCJ1c2VyX2dyb3VwcyI6WzEyMiwxMjAsMTIzLDEyNSwxMjYsMTI3LDIyMiwyNjQsMjY1LDI2NiwyNjcsMjY4LDI3MSwyNzIsMjczLDI3NCwyNzUsMjc2LDI3NywyNjksMjcwLDI4MSwyODJdfQ.eeC3SdPWt0ckRz_4h65tYUKOaiO_XKP6LBuhV_wtOqolLDMBh-Wp9zr27gWPjn4gO8HznukN7BpiGv-aq-61HxvFmTN_LFzQpNMlfZgRRynPkOURKBR78gkulMjVOrLz_RA1k-spRcXx-1bos3WN_dT9gnTv7rb9w6tdOJe2rDTPRbkrju4g6Fx70WMhtC9VaR5PMvJIHIQnML_WnzyLJ4sX0xrnWEEdB29LVCcPDj_ghTfUWI-G5uymOx2bPA2wZQ5Mkwa1OMjLnX3aHCL2KQS-1je6F3QqxSujfoSWtEnYYbYTAKLkKS793BIA2MrckF3Z085tCQIkTaaS-Zszug"
        self.url = "https://antoine.api.wandeed.com/api/lst/search?offset=0&limit=500"


def get_defaults_horaires() -> DataFrame:
    """Retourne les horaires par défaut"""
    default_horaires = DataFrame({key_day_plage_horaire: [0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
                                  key_debut_plage_horaire: ["08:30", "13:30"] * 5,
                                  key_fin_plage_horaire: ["12:00", "17:30"] * 5})
    return default_horaires


def run_test_integration(test_integration: TestIntegration):
    """Run les tests d'intégration"""
    print(f"\n\n========= DEBUT DU TEST INTEGRATION =========")
    test_integration.setUp()
    object_methods = [method_name for method_name in dir(test_integration)
                      if callable(getattr(test_integration, method_name))]

    test_methods = list(filter(lambda name: name[:5] == "test_", object_methods))
    for i, test_method in enumerate(test_methods):
        success_msg = "SUCCESS"
        msg = ""
        try:
            exec(f"test_integration.{test_method}()")
        except AssertionError as a:
            success_msg = "FAIL"
            msg = str(a)

        print(f"TEST {i + 1} / {len(test_methods)} - {success_msg} - {test_method} {'-' + msg}")

    print("========= FIN DU TEST INTEGRATION =========")
    print("Si échec : avez vous bien mis les guillemets ?")
