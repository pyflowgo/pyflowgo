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
import pyflowgo.flowgo_crust_temperature_model_bimodal
import math

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crust_temperature_bimodal.json'

        crust_temperature_model_bimodal = pyflowgo.flowgo_crust_temperature_model_bimodal.FlowGoCrustTemperatureModelHonBimodal()
        crust_temperature_model_bimodal.read_initial_condition_from_json_file(filename)

        self.assertEqual(crust_temperature_model_bimodal._crust_temperature_1, 773.15)
        self.assertEqual(crust_temperature_model_bimodal._crust_temperature_2, 500.0)

    def test_compute_crust_temperature(self):
        filename = './resources/input_parameters_crust_temperature_bimodal.json'
        state = pyflowgo.flowgo_state.FlowGoState()
        crust_temperature_model_bimodal = pyflowgo.flowgo_crust_temperature_model_bimodal.FlowGoCrustTemperatureModelHonBimodal()
        crust_temperature_model_bimodal.read_initial_condition_from_json_file(filename)


        state.set_current_time(4.50220927088170)
        state.set_current_position(10)
        effective_crust_temperature = crust_temperature_model_bimodal.compute_crust_temperature(state)
        self.assertAlmostEqual(effective_crust_temperature, 982.55275519699, 10)

        state.set_current_time(0)
        state.set_current_position(26)
        effective_crust_temperature = crust_temperature_model_bimodal.compute_crust_temperature(state)
        self.assertAlmostEqual(effective_crust_temperature, 500, 10)

if __name__ == '__main__':
    unittest.main()
