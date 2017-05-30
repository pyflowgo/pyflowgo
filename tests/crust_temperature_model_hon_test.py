import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_crust_temperature_model_hon
import math

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crust_temperature.json'
        crust_temperature_model_hon = pyflowgo.flowgo_crust_temperature_model_hon.FlowGoCrustTemperatureModelHon()
        crust_temperature_model_hon.read_initial_condition_from_json_file(filename)

    def test_compute_effective_cover_fraction(self):
        filename = './resources/input_parameters_crust_temperature.json'
        state = pyflowgo.flowgo_state.FlowGoState()

        state.set_current_time(4.50220927088170)

        crust_temperature_model_hon = pyflowgo.flowgo_crust_temperature_model_hon.FlowGoCrustTemperatureModelHon()
        crust_temperature_model_hon.read_initial_condition_from_json_file(filename)

        effective_crust_temperature = crust_temperature_model_hon.compute_crust_temperature(state)

        self.assertAlmostEqual(effective_crust_temperature, 982.55275519699, 10)

if __name__ == '__main__':
    unittest.main()
