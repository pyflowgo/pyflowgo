import unittest
import pyflowgo.flowgo_material_air

class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_forced_convection_heat_flux.json'

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)

        self.assertEqual(material_air._temp_air, 293.15)
        self.assertEqual(material_air._wind_speed, 5.0)
        self.assertEqual(material_air._ch_air, 0.0036)
        self.assertEqual(material_air._rho_air, 0.4412)
        self.assertEqual(material_air._cp_air, 1099.0)

    def test_compute_conv_heat_transfer_coef(self):
        filename = './resources/input_parameters_forced_convection_heat_flux.json'

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        conv_heat_transfer_coef = material_air.compute_conv_heat_transfer_coef()

        self.assertAlmostEqual(conv_heat_transfer_coef, 8.7278184,5)

    def test_get_temp_air(self):
        filename = './resources/input_parameters_forced_convection_heat_flux.json'

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        temp_air = material_air.get_temperature()

        self.assertEqual(temp_air, 293.15)

if __name__ == '__main__':
    unittest.main()
