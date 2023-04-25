from datetime import datetime, timedelta
from time import sleep

from api.controllers.task_assigner import task_assigner_controller, \
    ContrainteEtreSurProjet
from api.models import StatutCalculEnum
from api.models.calcul_cache import cache
from api.tools import TestIntegration, run_test_integration


class TaskAssignerControllerTest(TestIntegration):
    def setUp(self) -> None:
        super().setUp()

    def test_debug_end_to_end(self):
        """Ce -test- sert à débugger en allant le plus loin possible à partir d'une requête"""
        json_file = {"backend_access_token": self.access_token,
                      "backend_url": self.url,
                      "date_start": (datetime.now() - timedelta(weeks=52)).isoformat(),
                      "date_end": (datetime.now() - timedelta(weeks=4)).isoformat(),
                      "selected_users": None,
                      "contrainte_etre_sur_projet": ContrainteEtreSurProjet.NON,
                      "avantage_projet": 1.0,
                      "curseur": 0}

        etat_calcul = task_assigner_controller(json_file=json_file)
        success = True
        while etat_calcul.statut in [StatutCalculEnum.IN_PROGRESS]:
            etat_calcul = cache.get_status(calcul_id=etat_calcul.identifiant)
            sleep(1)

        if etat_calcul.statut in [StatutCalculEnum.FAIL, StatutCalculEnum.CRASH_SOLVEUR]:
            success = False

        self.assertTrue(success, msg=f"Echec du test {etat_calcul.message}")


test = TaskAssignerControllerTest()
test.setUp()
if test.commandline:
    run_test_integration(test_integration=test)
