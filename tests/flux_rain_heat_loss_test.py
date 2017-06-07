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
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_flux_heat_loss_rain


class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_conduction_heat_flux.json'
        flowgo_flux_rain_heat_loss = pyflowgo.flowgo_flux_heat_loss_rain.FlowGoFluxHeatLossRain()
        flowgo_flux_rain_heat_loss.read_initial_condition_from_json_file(filename)

        self.assertEqual(flowgo_flux_rain_heat_loss._rainfall_rate, 7.98e-8)
        self.assertEqual(flowgo_flux_rain_heat_loss._density_water, 958.)
        self.assertEqual(flowgo_flux_rain_heat_loss._latent_heat_vaporization, 2.8e6)

    def test_compute_flux(self):
        filename = './resources/input_parameters_conduction_heat_flux.json'
        flowgo_flux_rain_heat_loss = pyflowgo.flowgo_flux_heat_loss_rain.FlowGoFluxHeatLossRain()
        flowgo_flux_rain_heat_loss.read_initial_condition_from_json_file(filename)

        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(10)

        qrain = flowgo_flux_rain_heat_loss.compute_flux(state,
                                                         channel_width=6.20861841803369,
                                                         channel_depth=terrain_condition.get_channel_depth(10))

        self.assertAlmostEqual(qrain, 1328.9890439538, 10)

if __name__ == '__main__':
    unittest.main()
