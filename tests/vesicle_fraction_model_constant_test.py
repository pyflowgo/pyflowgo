import unittest
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_state


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_vesicle_fraction_model_constant.json'

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        self.assertEqual(vesicle_fraction_model_constant._vesicle_fraction, 0.64)

    def test_computes_vesicle_fraction(self):
        filename = './resources/input_parameters_vesicle_fraction_model_constant.json'

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(10)

        vesicle_fraction = vesicle_fraction_model_constant.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.64)

if __name__ == '__main__':
    unittest.main()