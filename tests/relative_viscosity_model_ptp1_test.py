import unittest
import pyflowgo.flowgo_relative_viscosity_model_ptp1
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant


class MyTestCase(unittest.TestCase):

    def test_compute_relative_viscosity(self):
        filename = './resources/input_parameters_vesicle_fraction_model_constant.json'

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        relative_viscosity_model_ptp1 = pyflowgo.flowgo_relative_viscosity_model_ptp1. \
            FlowGoRelativeViscosityModelPhanThienPham1(vesicle_fraction_model=vesicle_fraction_model_constant)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)

        relative_viscosity = relative_viscosity_model_ptp1.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 21.093750000,10)

if __name__ == '__main__':
    unittest.main()
