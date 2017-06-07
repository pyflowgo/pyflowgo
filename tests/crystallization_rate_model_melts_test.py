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
import pyflowgo.flowgo_crystallization_rate_model_melts
import csv


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crystallization_rate_melts.json'
        crystallization_rate_model_melts =pyflowgo.flowgo_crystallization_rate_model_melts.FlowGoCrystallizationRateModelMelts()
        crystallization_rate_model_melts.read_initial_condition_from_json_file(filename)


    def test_get_crystal_fraction(self):
        filename = './resources/input_parameters_crystallization_rate_melts.json'
        crystallization_rate_model_melts =pyflowgo.flowgo_crystallization_rate_model_melts.FlowGoCrystallizationRateModelMelts()
        crystallization_rate_model_melts.read_initial_condition_from_json_file(filename)
        filename_melts = './resources/Results-melts_MU74.csv'
        crystallization_rate_model_melts.read_crystal_from_melts(filename_melts)
        crystal_fraction = crystallization_rate_model_melts.get_crystal_fraction(1329.9)
        self.assertAlmostEqual(crystal_fraction, 0.964450359, 8)

    def test_get_solid_temperature(self):
        filename = './resources/input_parameters_crystallization_rate_melts.json'
        crystallization_rate_model_melts =pyflowgo.flowgo_crystallization_rate_model_melts.FlowGoCrystallizationRateModelMelts()
        crystallization_rate_model_melts.read_initial_condition_from_json_file(filename)
        self.assertEqual(crystallization_rate_model_melts.get_solid_temperature(), 1237.15)

    def test_compute_crystallization_rate(self):
        filename = './resources/input_parameters_crystallization_rate_melts.json'
        crystallization_rate_model_melts = pyflowgo.flowgo_crystallization_rate_model_melts.FlowGoCrystallizationRateModelMelts()
        crystallization_rate_model_melts.read_initial_condition_from_json_file(filename)
        filename_melts = './resources/Results-melts_MU74.csv'
        crystallization_rate_model_melts.read_crystal_from_melts(filename_melts)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1350.65)
        crystallization_rate=crystallization_rate_model_melts.compute_crystallization_rate(state)
        self.assertAlmostEqual(crystallization_rate, 0.002351632,8)
        state.set_core_temperature(1490.65)
        crystallization_rate=crystallization_rate_model_melts.compute_crystallization_rate(state)
        self.assertAlmostEqual(crystallization_rate, 0.000858503,8)

if __name__ == '__main__':
    unittest.main()

