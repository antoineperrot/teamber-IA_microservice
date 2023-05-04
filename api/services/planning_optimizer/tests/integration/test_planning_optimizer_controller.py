from datetime import datetime, timedelta
from time import sleep

from api.controllers.planning_optimizer import planning_optimizer_controller
from api.models import StatutCalculEnum
from api.models.calcul_cache import cache
from api.tools import TestIntegration, run_test_integration


class PlanningOptimizerControllerTest(TestIntegration):
    def setUp(self) -> None:
        super().setUp()

    def test_planning_optimization_controller(self):
        """Ce -test- sert à débugger en allant le plus loin possible à partir d'une requête"""
        json_file = {"backend_access_token": self.access_token,
                      "backend_url": self.url,
                      "date_start": (datetime.now() - timedelta(weeks=6)).isoformat(),
                      "date_end": (datetime.now() + timedelta(weeks=6) + timedelta(days=2)).isoformat(),
                      "selected_users": None,
                      "key_project_prioritys_projets": None,
                      "parts_max_length": 1,
                      "min_duration_section": 0.5}

        etat_calcul = planning_optimizer_controller(json=json_file)
        success = True
        while etat_calcul.statut in [StatutCalculEnum.IN_PROGRESS]:
            etat_calcul = cache.get_status(calcul_id=etat_calcul.identifiant)
            sleep(1)
        if etat_calcul.statut == StatutCalculEnum.FAIL:
            success = False

        self.assertTrue(success, msg=f"Echec du test {etat_calcul.message}")


test = PlanningOptimizerControllerTest()
test.setUp()
if test.commandline:
    run_test_integration(test_integration=test)
