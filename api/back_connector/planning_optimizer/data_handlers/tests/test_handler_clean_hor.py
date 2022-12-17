import unittest

import pandas as pd

from api.back_connector.planning_optimizer.data_handlers.horaires import (
    handler_clean_hor,
)


class TestHandlerCleanHor(unittest.TestCase):
    def setUp(self):
        self.list_test_input = []
        self.list_expected_result = []

        self.list_test_input.append(
            pd.DataFrame(
                {
                    "eeh_xheurefin": ["10:45", "23:00"],
                    "eeh_sfkperiode": [1, 2],
                    "eeh_xheuredebut": ["06:30", "22:45"],
                }
            )
        )
        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [0, 1],
                    "eeh_xheuredebut": ["06:30", "22:45"],
                    "eeh_xheurefin": ["10:45", "23:00"],
                }
            )
        )

        self.list_test_input.append(
            pd.DataFrame(
                {
                    "eeh_xheuredebut": ["06:30", "22:45"],
                    "eeh_sfkperiode": [2, 1],
                    "eeh_xheurefin": ["10:45", "00:30"],
                }
            )
        )
        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1],
                    "eeh_xheuredebut": ["06:30"],
                    "eeh_xheurefin": ["10:45"],
                }
            )
        )

    def test_handler_clean_hor(self):
        for input_value, expected_result in zip(
            self.list_test_input, self.list_expected_result
        ):
            function_output = handler_clean_hor(input_value)
            pd.testing.assert_frame_equal(function_output, expected_result)
