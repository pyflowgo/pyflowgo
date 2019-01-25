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
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_state
import math

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_terrain_condition.json'
        terrain_condition= pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        self.assertEqual(terrain_condition.get_channel_depth(0), 1.4)
        self.assertEqual(terrain_condition.get_channel_width(0), 4.5)
        self.assertEqual(terrain_condition.get_gravity(0), 9.81)
        self.assertEqual(terrain_condition._slope_smoothing_number_of_points, 6)
        self.assertEqual(terrain_condition._slope_smoothing_active, False)

    def test_read_slope_file(self):
        filename = './resources/input_parameters_terrain_condition.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)

        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(0)
        slope = terrain_condition.get_channel_slope(state.get_current_position())
        self.assertAlmostEqual(slope, 0.328342197625647,15)
        self.assertAlmostEqual(terrain_condition.get_channel_slope(1000),(0.197395559779715),15)
        self.assertAlmostEqual(terrain_condition.get_channel_slope(30), (0.325347225021063), 15)
