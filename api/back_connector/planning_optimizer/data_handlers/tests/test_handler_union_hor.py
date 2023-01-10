import unittest
import pandas as pd
from api.back_connector.planning_optimizer.data_handlers.horaires import handler_union_hor


class TestHandlerUnionHor(unittest.TestCase):
    def setUp(self):
        self.list_test_union = []
        self.list_expected_result = []
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1],
                    "eeh_xheuredebut": ["06:30", "06:45"],
                    "eeh_xheurefin": ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1],
                    "eeh_xheuredebut": ["06:30"],
                    "eeh_xheurefin": ["11:00"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1, 2, 2],
                    "eeh_xheuredebut": ["07:30", "06:45", "07:00", "07:30"],
                    "eeh_xheurefin": ["10:00", "11:00", "08:00", "08:30"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 2],
                    "eeh_xheuredebut": ["06:45", "07:00"],
                    "eeh_xheurefin": ["11:00", "08:30"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 2],
                    "eeh_xheuredebut": ["06:30", "06:45"],
                    "eeh_xheurefin": ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 2],
                    "eeh_xheuredebut": ["06:30", "06:45"],
                    "eeh_xheurefin": ["10:00", "11:00"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1],
                    "eeh_xheuredebut": ["06:50", "06:30"],
                    "eeh_xheurefin": ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1],
                    "eeh_xheuredebut": ["06:30"],
                    "eeh_xheurefin": ["11:00"],
                }
            )
        )
        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1, 1],
                    "eeh_xheuredebut": ["06:50", "06:30", "07:00"],
                    "eeh_xheurefin": ["10:00", "11:00", "08:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1],
                    "eeh_xheuredebut": ["06:30"],
                    "eeh_xheurefin": ["11:00"],
                }
            )
        )

        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1, 1],
                    "eeh_xheuredebut": ["06:50", "06:30", "10:00"],
                    "eeh_xheurefin": ["10:00", "11:00", "12:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1],
                    "eeh_xheuredebut": ["06:30"],
                    "eeh_xheurefin": ["12:00"],
                }
            )
        )

        ########################################
        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1, 1],
                    "eeh_xheuredebut": ["06:30", "11:30", "06:30"],
                    "eeh_xheurefin": ["10:30", "15:30", "10:45"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1],
                    "eeh_xheuredebut": ["06:30", "11:30"],
                    "eeh_xheurefin": ["10:45", "15:30"],
                }
            )
        )

    def test_handler_union_hor(self):
        for test_union, expected_result in zip(
            self.list_test_union, self.list_expected_result
        ):
            function_output = handler_union_hor(test_union)
            pd.testing.assert_frame_equal(function_output, expected_result, check_dtype=False)
