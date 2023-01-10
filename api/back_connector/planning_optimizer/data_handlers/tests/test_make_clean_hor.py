"""
Test la fonction split_n_clean_horaires
"""
import pickle
import unittest

from pandas.testing import assert_frame_equal

from api.back_connector.planning_optimizer.data_handlers.horaires import make_clean_hor


class TestMakeCleanHor(unittest.TestCase):
    """
    Test la fonction split_n_clean_horaires
    """

    def setUp(self):
        self.input_value = pickle.load(
            open(
                "api/back_connector/planning_optimizer/data_handlers/tests/test_data/input_handler_hor.pkl",
                "rb",
            )
        )
        self.expected_result = pickle.load(
            open(
                "api/back_connector/planning_optimizer/data_handlers/tests/test_data/expected_result_make_clean_hor.pkl",
                "rb",
            )
        )

    def test_make_clean_hor(self):
        output_func = make_clean_hor(self.input_value)

        set_keys_output_func = set(output_func.keys())
        set_keys_expected_result = set(self.expected_result.keys())
        self.assertSetEqual(
            set_keys_output_func,
            set_keys_expected_result,
            msg="Les dictionnnaires n'ont pas les mêmes clés.",
        )

        for key in output_func.keys():
            assert_frame_equal(output_func[key], self.expected_result[key])
