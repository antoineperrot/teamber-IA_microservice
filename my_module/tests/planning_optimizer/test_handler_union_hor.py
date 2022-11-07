import unittest
import pandas as pd


class TestHandlerUnionHor(unittest.TestCase):
    def setUp(self):
        self.list_test_union = []
        self.list_expected_result = []

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

        self.list_test_union.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1, 1],
                    "eeh_xheuredebut": ["07:30", "06:45"],
                    "eeh_xheurefin": ["10:00", "11:00"],
                }
            )
        )

        self.list_expected_result.append(
            pd.DataFrame(
                {
                    "eeh_sfkperiode": [1],
                    "eeh_xheuredebut": ["06:45"],
                    "eeh_xheurefin": ["11:00"],
                }
            )
        )

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

    def test_handler_union_hor(self):
        for test_union, expected_result in zip(
            self.list_test_union, self.list_expected_result
        ):
            function_output = handler_union_hor(test_union)
            pd.testing.assert_frame_equal(function_output, expected_result)
