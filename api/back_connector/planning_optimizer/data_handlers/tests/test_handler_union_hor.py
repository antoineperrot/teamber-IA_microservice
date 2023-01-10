import unittest
import pandas as pd
from api.back_connector.planning_optimizer.data_handlers.horaires import handler_union_hor
from api.string_keys import *


class TestHandlerUnionHor(unittest.TestCase):
    def setUp(self):
        self.list_test_union = []
        self.list_expected_result = []
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1],
                    key_debut_plage_horaire: ["06:30", "06:45"],
                    key_fin_plage_horaire: ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1],
                    key_debut_plage_horaire: ["06:30"],
                    key_fin_plage_horaire: ["11:00"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1, 2, 2],
                    key_debut_plage_horaire: ["07:30", "06:45", "07:00", "07:30"],
                    key_fin_plage_horaire: ["10:00", "11:00", "08:00", "08:30"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 2],
                    key_debut_plage_horaire: ["06:45", "07:00"],
                    key_fin_plage_horaire: ["11:00", "08:30"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 2],
                    key_debut_plage_horaire: ["06:30", "06:45"],
                    key_fin_plage_horaire: ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 2],
                    key_debut_plage_horaire: ["06:30", "06:45"],
                    key_fin_plage_horaire: ["10:00", "11:00"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1],
                    key_debut_plage_horaire: ["06:50", "06:30"],
                    key_fin_plage_horaire: ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1],
                    key_debut_plage_horaire: ["06:30"],
                    key_fin_plage_horaire: ["11:00"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1, 1],
                    key_debut_plage_horaire: ["06:50", "06:30", "07:00"],
                    key_fin_plage_horaire: ["10:00", "11:00", "08:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1],
                    key_debut_plage_horaire: ["06:30"],
                    key_fin_plage_horaire: ["11:00"],
                }
            )
        )

        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1, 1],
                    key_debut_plage_horaire: ["06:50", "06:30", "10:00"],
                    key_fin_plage_horaire: ["10:00", "11:00", "12:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1],
                    key_debut_plage_horaire: ["06:30"],
                    key_fin_plage_horaire: ["12:00"],
                }
            )
        )

        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1, 1],
                    key_debut_plage_horaire: ["06:30", "11:30", "06:30"],
                    key_fin_plage_horaire: ["10:30", "15:30", "10:45"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 1],
                    key_debut_plage_horaire: ["06:30", "11:30"],
                    key_fin_plage_horaire: ["10:45", "15:30"],
                }
            )
        )

    def test_handler_union_hor(self):
        for test_union, expected_result in zip(
            self.list_test_union, self.list_expected_result
        ):
            function_output = handler_union_hor(test_union)
            pd.testing.assert_frame_equal(function_output, expected_result, check_dtype=False)
