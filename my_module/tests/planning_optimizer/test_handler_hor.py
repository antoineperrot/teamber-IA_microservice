import unittest
import pandas as pd
import pickle


class TestHandlerHor(unittest.TestCase):
    def setUp(self):
        self.input_data = pickle.load(open('my_module/tests/planning_optimizer/test_data/input_handler_hor.pkl', 'rb'))
        self.expected_output = pickle.load(
            open('my_module/tests/planning_optimizer/test_data/expected_result_handler_hor.pkl', 'rb'))

    def test_handler_hor(self):
        self.output_func = handler_hor(self.input_data)
        self.assertTrue(set(self.expected_output.keys()) == set(self.output_func.keys()),
                        msg='Les dictionnaires ont des clés différentes.')

        for key in self.output_func.keys():
            pd.testing.assert_frame_equal(self.output_func[key],
                                          self.expected_output[key])
