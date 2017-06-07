# Copyright 2017 PyFLOWGO development team (Magdalena Oryaelle Chevrel and Jeremie Labroquere)
#
# This file is part of the PyFLOWGO library.
#
# The PyFLOWGO library is free software: you can redistribute it and/or modify
# it under the terms of the the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# The PyFLOWGO library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received copies of the GNU Lesser General Public License
# along with the PyFLOWGO library.  If not, see https://www.gnu.org/licenses/.

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
