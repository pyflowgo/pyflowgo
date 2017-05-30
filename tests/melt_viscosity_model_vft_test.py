import unittest
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_state


class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_melt_viscosity_model.json'

        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)

        self.assertEqual(melt_viscosity_model_vft._a, -4.7)
        self.assertEqual(melt_viscosity_model_vft._b, 5429.7)
        self.assertEqual(melt_viscosity_model_vft._c, 595.5)

    def test_computes_melt_viscosity(self):
        filename = './resources/input_parameters_melt_viscosity_model.json'

        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1200)

        melt_viscosity = melt_viscosity_model_vft.compute_melt_viscosity(state)
        self.assertAlmostEqual(melt_viscosity, 19148.466310475585, 10)

if __name__ == '__main__':
    unittest.main()
