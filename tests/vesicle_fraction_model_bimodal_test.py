import unittest
import pyflowgo.flowgo_vesicle_fraction_model_bimodal
import pyflowgo.flowgo_state


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_vesicle_fraction_model_bimodal.json'

        vesicle_fraction_model_bimodal = pyflowgo.flowgo_vesicle_fraction_model_bimodal.FlowGoVesicleFractionModelBimodal()
        vesicle_fraction_model_bimodal.read_initial_condition_from_json_file(filename)

        self.assertEqual(vesicle_fraction_model_bimodal._vesicle_fraction_1, 0.6)
        self.assertEqual(vesicle_fraction_model_bimodal._vesicle_fraction_2, 0.2)

    def test_vesicle_fraction_model_bimodal(self):
        filename = './resources/input_parameters_vesicle_fraction_model_bimodal.json'

        vesicle_fraction_model_bimodal = pyflowgo.flowgo_vesicle_fraction_model_bimodal.FlowGoVesicleFractionModelBimodal()
        vesicle_fraction_model_bimodal.read_initial_condition_from_json_file(filename)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(10)
        vesicle_fraction = vesicle_fraction_model_bimodal.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.6)

        state.set_current_position(11000)
        vesicle_fraction = vesicle_fraction_model_bimodal.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.2)

if __name__ == '__main__':
    unittest.main()

