"""Test controller with mocked data"""
from datetime import datetime, timedelta
import unittest
from api.controllers.task_assigner_controller import handler_demande_task_assigner, SolverCrashException,\
    FrontEndTaskAssignerRequestParameters
from api.lib_task_assigner.tools.contrainte_projet import ContrainteEtreSurProjet


class TestUnitTaskAssignerMockedData(unittest.TestCase):
    def test_unit_task_assigner_with_mocked_data(self):

        params = FrontEndTaskAssignerRequestParameters(backend_access_token="",
                                                       backend_url="",
                                                       date_start=datetime.now().replace(microsecond=0, second=0),
                                                       date_end=(datetime.now() + timedelta(days=21)).replace(microsecond=0, second=0),
                                                       contrainte_etre_sur_projet=ContrainteEtreSurProjet.DE_PREFERENCE,
                                                       curseur=0.5,
                                                       avantage_projet=1.0,
                                                       selected_users=None)
        success = True
        try:
            for i in range(20):
                handler_demande_task_assigner(request_parameters=params, force_mock=True)
        except SolverCrashException as e:
            import traceback
            print(traceback.format_exc())
            success = False
        self.assertTrue(success, msg="Fail du solveur avec les données mockées")
