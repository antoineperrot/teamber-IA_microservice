"""
Test la fonction make_horaire_clean
"""
import pickle
import unittest
from pandas.testing import assert_frame_equal

from api.data_handling.planning_optimizer.horaires import make_horaire_clean


class TestMakeCleanHor(unittest.TestCase):
    """
    Test la fonction make_horaire_clean
    """

    def setUp(self):
        self.input_value = pickle.load(
            open(
                "my_module/tests/planning_optimizer/test_data/input_handler_hor.pkl",
                "rb",
            )
        )
        self.expected_result = pickle.load(
            open(
                "my_module/tests/planning_optimizer/test_data/expected_result_make_clean_hor.pkl",
                "rb",
            )
        )

    def test_make_clean_hor(self):
        output_func = make_horaire_clean(self.input_value)

        set_keys_output_func = set(output_func.keys())
        set_keys_expected_result = set(self.expected_result.keys())
        self.assertSetEqual(
            set_keys_output_func,
            set_keys_expected_result,
            msg="Les dictionnnaires n'ont pas les mêmes clés.",
        )

        for key in output_func.keys():
            assert_frame_equal(output_func[key], self.expected_result[key])
