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
import pyflowgo.flowgo_crystallization_rate_model_basic


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crystallization_rate.json'
        crystallization_rate_model_basic =pyflowgo.flowgo_crystallization_rate_model_basic.FlowGoCrystallizationRateModelBasic()
        crystallization_rate_model_basic.read_initial_condition_from_json_file(filename)

        self.assertEqual(crystallization_rate_model_basic._crystal_fraction, 0.104)
        self.assertEqual(crystallization_rate_model_basic._crystals_grown_during_cooling, 0.896)
        self.assertEqual(crystallization_rate_model_basic._solid_temperature, 1237.15)
        self.assertEqual(crystallization_rate_model_basic._eruption_temperature, 1387.15)

    def test_get_crystal_fraction(self):
        filename = './resources/input_parameters_crystallization_rate.json'
        crystallization_rate_model_basic =pyflowgo.flowgo_crystallization_rate_model_basic.FlowGoCrystallizationRateModelBasic()
        crystallization_rate_model_basic.read_initial_condition_from_json_file(filename)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(0)
        crystal_fraction= crystallization_rate_model_basic.get_crystal_fraction(state)
        self.assertEqual(crystal_fraction, 0.104)

    def test_get_solid_temperature(self):
        filename = './resources/input_parameters_crystallization_rate.json'
        crystallization_rate_model_basic =pyflowgo.flowgo_crystallization_rate_model_basic.FlowGoCrystallizationRateModelBasic()
        crystallization_rate_model_basic.read_initial_condition_from_json_file(filename)
        self.assertEqual(crystallization_rate_model_basic.get_solid_temperature(), 1237.15)

    def test_compute_crystallization_rate(self):
        filename = './resources/input_parameters_crystallization_rate.json'
        crystallization_rate_model_basic =pyflowgo.flowgo_crystallization_rate_model_basic.FlowGoCrystallizationRateModelBasic()
        crystallization_rate_model_basic.read_initial_condition_from_json_file(filename)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(0)
        crystallization_rate=crystallization_rate_model_basic.compute_crystallization_rate(state)

        self.assertAlmostEqual(crystallization_rate, 0.00597333333,10)

if __name__ == '__main__':
    unittest.main()
