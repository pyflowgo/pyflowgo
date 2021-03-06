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
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_crust_temperature_model_field
import math

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crust_temperature.json'
        crust_temperature_model_field = pyflowgo.flowgo_crust_temperature_model_field.FlowGoCrustTemperatureModelField()
        crust_temperature_model_field.read_initial_condition_from_json_file(filename)
        self.assertEqual(crust_temperature_model_field._crust_temperature, 773.15)

    def test_read_crust_temperature_from_file(self):
        filename = './resources/input_parameters_crust_temperature.json'
        crust_temperature_model_field = pyflowgo.flowgo_crust_temperature_model_field.FlowGoCrustTemperatureModelField()
        crust_temperature_model_field.read_initial_condition_from_json_file(filename)

        filename_crust_temperature = './resources/crust_temperature_profile.txt'
        crust_temperature_model_field.read_crust_temperature_from_file(filename_crust_temperature)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(3.15)
        crust_temperature = crust_temperature_model_field.get_crust_temperature(state.get_current_position())
        self.assertAlmostEqual(crust_temperature, 860.06+273.15, 2)

    def test_compute_crust_temperature(self):
        filename = './resources/input_parameters_crust_temperature.json'
        crust_temperature_model_field = pyflowgo.flowgo_crust_temperature_model_field.FlowGoCrustTemperatureModelField()
        crust_temperature_model_field.read_initial_condition_from_json_file(filename)

        filename_crust_temperature = './resources/crust_temperature_profile.txt'
        crust_temperature_model_field.read_crust_temperature_from_file(filename_crust_temperature)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(8)

        effective_crust_temperature = crust_temperature_model_field.compute_crust_temperature(state)

        self.assertAlmostEqual(effective_crust_temperature, 500+273.15, 2)


if __name__ == '__main__':
    unittest.main()
