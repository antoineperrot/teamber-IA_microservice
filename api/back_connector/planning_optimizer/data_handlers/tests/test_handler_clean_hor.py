import unittest

import pandas as pd

from api.back_connector.planning_optimizer.data_handlers.horaires import (
    handler_clean_hor,
)
from api.string_keys import *


class TestHandlerCleanHor(unittest.TestCase):
    def setUp(self):
        self.list_test_input = []
        self.list_expected_result = []

        self.list_test_input.append(
            pd.DataFrame(
                {
                    key_fin_plage_horaire: ["10:45", "23:00"],
                    key_day_plage_horaire: [1, 2],
                    key_debut_plage_horaire: ["06:30", "22:45"],
                }
            )
        )
        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1, 2],
                    key_debut_plage_horaire: ["06:30", "22:45"],
                    key_fin_plage_horaire: ["10:45", "23:00"],
                }
            )
        )

        self.list_test_input.append(
            pd.DataFrame(
                {
                    key_debut_plage_horaire: ["06:30", "22:45"],
                    key_day_plage_horaire: [1, 0],
                    key_fin_plage_horaire: ["10:45", "00:30"],
                }
            )
        )
        self.list_expected_result.append(
            pd.DataFrame(
                {
                    key_day_plage_horaire: [1],
                    key_debut_plage_horaire: ["06:30"],
                    key_fin_plage_horaire: ["10:45"],
                }
            )
        )

    def test_handler_clean_hor(self):
        for input_value, expected_result in zip(
            self.list_test_input, self.list_expected_result
        ):
            function_output = handler_clean_hor(input_value)
            pd.testing.assert_frame_equal(function_output, expected_result, check_dtype=False)
