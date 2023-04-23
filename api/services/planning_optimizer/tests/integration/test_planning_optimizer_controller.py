from datetime import datetime, timedelta
from api.controllers.task_assigner import task_assigner_controller,\
    ContrainteEtreSurProjet
from api.tools import TestIntegration, run_test_integration


class TaskAssignerControllerTest(TestIntegration):
    def setUp(self) -> None:
        super().setUp()

    def test__debug_end_to_end(self):
        """Ce -test- sert à débugger en allant le plus loin possible à partir d'une requête"""
        json_file = {"backend_access_token": self.access_token,
                      "backend_url": self.url,
                      "date_start": (datetime.now()).isoformat(),
                      "date_end": (datetime.now() + timedelta(weeks=2)).isoformat(),
                      "selected_users": None,
                      "contrainte_etre_sur_projet": ContrainteEtreSurProjet.OUI,
                      "avantage_projet": 1.0,
                      "curseur": 0}
        task_assigner_controller(json_file=json_file)


test = TaskAssignerControllerTest()
test.setUp()
if test.commandline:
    run_test_integration(test_integration=test)
