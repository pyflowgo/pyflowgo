import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_state
import pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal_f_temp.json'
        crystallization_rate_model_bimodal_f_temp =pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp.\
            FlowGoCrystallizationRateModelBimodalFonctionTemperature()
        crystallization_rate_model_bimodal_f_temp.read_initial_condition_from_json_file(filename)

    def test_get_crystal_fraction(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal_f_temp.json'
        crystallization_rate_model_bimodal_f_temp =pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp.\
            FlowGoCrystallizationRateModelBimodalFonctionTemperature()
        crystallization_rate_model_bimodal_f_temp.read_initial_condition_from_json_file(filename)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(0)
        crystal_fraction= crystallization_rate_model_bimodal_f_temp.get_crystal_fraction(state)
        self.assertEqual(crystal_fraction, 0.104)

    def test_get_solid_temperature(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal_f_temp.json'
        crystallization_rate_model_bimodal_f_temp =pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp.\
            FlowGoCrystallizationRateModelBimodalFonctionTemperature()
        crystallization_rate_model_bimodal_f_temp.read_initial_condition_from_json_file(filename)
        self.assertEqual(crystallization_rate_model_bimodal_f_temp.get_solid_temperature(), 1237.15)

    def test_compute_crystallization_rate(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal_f_temp.json'
        crystallization_rate_model_bimodal_f_temp = pyflowgo.flowgo_crystallization_rate_model_bimodal_f_temp.FlowGoCrystallizationRateModelBimodalFonctionTemperature()
        crystallization_rate_model_bimodal_f_temp.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1300)
        crystallization_rate = crystallization_rate_model_bimodal_f_temp.compute_crystallization_rate(state)
        self.assertAlmostEqual(crystallization_rate, 0.006, 10)

        state.set_core_temperature(1190)
        crystallization_rate = crystallization_rate_model_bimodal_f_temp.compute_crystallization_rate(state)
        self.assertAlmostEqual(crystallization_rate, 0.02, 10)


if __name__ == '__main__':
    unittest.main()
