import unittest
import pyflowgo.flowgo_melt_viscosity_model_basic
import pyflowgo.flowgo_state


class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_melt_viscosity_model.json'

        melt_viscosity_model_basic = pyflowgo.flowgo_melt_viscosity_model_basic.FlowGoMeltViscosityModelBasic()
        melt_viscosity_model_basic.read_initial_condition_from_json_file(filename)

        self.assertEqual(melt_viscosity_model_basic._viscosity_eruption, 100)
        self.assertEqual(melt_viscosity_model_basic._eruption_temperature, 1273.15)


    def test_computes_melt_viscosity(self):
        filename = './resources/input_parameters_melt_viscosity_model.json'

        melt_viscosity_model_basic = pyflowgo.flowgo_melt_viscosity_model_basic.FlowGoMeltViscosityModelBasic()
        melt_viscosity_model_basic.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1200)

        melt_viscosity = melt_viscosity_model_basic.compute_melt_viscosity(state)
        self.assertAlmostEqual(melt_viscosity, 1865.28695961684, 10)

if __name__ == '__main__':
    unittest.main()
