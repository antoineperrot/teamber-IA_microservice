import unittest

import pandas as pd

from api.services.planning_optimizer.solver.tools.taches import split_tasks


class TestSplitTasks(unittest.TestCase):
    def setUp(self):
        self.input_df = pd.DataFrame(
            {
                "evt_dduree": {
                    0: 0.75,
                    1: 3.25,
                    2: 3.25,
                    3: 0.25,
                    4: 1.0,
                    5: 1.5,
                    6: 0.75,
                },
                "evt_spkevenement": {
                    0: 1075,
                    1: 1500,
                    2: 3591,
                    3: 5035,
                    4: 6391,
                    5: 8501,
                    6: 9646,
                },
                "lgl_sfkligneparent": {
                    0: 2871,
                    1: 2871,
                    2: 2871,
                    3: 2871,
                    4: 2871,
                    5: 2871,
                    6: 2871,
                },
                "evt_sfkprojet": {
                    0: 2842,
                    1: 9077,
                    2: 9077,
                    3: 2842,
                    4: 9077,
                    5: 9227,
                    6: 9077,
                },
                "priorite": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 0},
                "n_parts": {0: 1, 1: 4, 2: 4, 3: 1, 4: 1, 5: 2, 6: 1},
                "n_filled_parts": {0: 0, 1: 3, 2: 3, 3: 0, 4: 1, 5: 1, 6: 0},
                "length": {0: 0.75, 1: 0.25, 2: 0.25, 3: 0.25, 4: 0.0, 5: 0.5, 6: 0.75},
            }
        )

        self.mod_length = 1.0

        self.expected_result = pd.DataFrame(
            {
                "evt_dduree": {
                    0: 0.75,
                    1: 3.25,
                    2: 3.25,
                    3: 3.25,
                    4: 3.25,
                    5: 3.25,
                    6: 3.25,
                    7: 3.25,
                    8: 3.25,
                    9: 0.25,
                    10: 1.0,
                    11: 1.5,
                    12: 1.5,
                    13: 0.75,
                },
                "evt_spkevenement": {
                    0: 1075,
                    1: 1500,
                    2: 1500,
                    3: 1500,
                    4: 1500,
                    5: 3591,
                    6: 3591,
                    7: 3591,
                    8: 3591,
                    9: 5035,
                    10: 6391,
                    11: 8501,
                    12: 8501,
                    13: 9646,
                },
                "lgl_sfkligneparent": {
                    0: 2871,
                    1: 2871,
                    2: 2871,
                    3: 2871,
                    4: 2871,
                    5: 2871,
                    6: 2871,
                    7: 2871,
                    8: 2871,
                    9: 2871,
                    10: 2871,
                    11: 2871,
                    12: 2871,
                    13: 2871,
                },
                "evt_sfkprojet": {
                    0: 2842,
                    1: 9077,
                    2: 9077,
                    3: 9077,
                    4: 9077,
                    5: 9077,
                    6: 9077,
                    7: 9077,
                    8: 9077,
                    9: 2842,
                    10: 9077,
                    11: 9227,
                    12: 9227,
                    13: 9077,
                },
                "priorite": {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0,
                    6: 0,
                    7: 0,
                    8: 0,
                    9: 0,
                    10: 0,
                    11: 1,
                    12: 1,
                    13: 0,
                },
                "length": {
                    0: 0.75,
                    1: 0.25,
                    2: 1.0,
                    3: 1.0,
                    4: 1.0,
                    5: 0.25,
                    6: 1.0,
                    7: 1.0,
                    8: 1.0,
                    9: 0.25,
                    10: 1.0,
                    11: 0.5,
                    12: 1.0,
                    13: 0.75,
                },
                "id_part": {
                    0: 0,
                    1: 1,
                    2: 2,
                    3: 3,
                    4: 4,
                    5: 5,
                    6: 6,
                    7: 7,
                    8: 8,
                    9: 9,
                    10: 10,
                    11: 11,
                    12: 12,
                    13: 13,
                },
            }
        )

        self.expected_result["evt_spkevenement"] = self.expected_result[
            "evt_spkevenement"
        ].astype(int)
        self.expected_result["lgl_sfkligneparent"] = self.expected_result[
            "lgl_sfkligneparent"
        ].astype(int)
        self.expected_result["evt_sfkprojet"] = self.expected_result[
            "evt_sfkprojet"
        ].astype(int)
        self.expected_result["priorite"] = self.expected_result["priorite"].astype(int)

    def test_split_task(self):
        output_func = split_tasks(self.input_df, self.mod_length)
        pd.testing.assert_frame_equal(output_func, self.expected_result)
