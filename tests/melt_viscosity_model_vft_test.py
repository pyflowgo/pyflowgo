# Copyright 2017 PyFlowGo development team (Oryaelle Magdalena Chevrel and Jeremie Labroquere)
#
# This file is part of the PyFlowGo library.
#
# The PyFlowGo library is free software: you can redistribute it and/or modify
# it under the terms of the the GNU Lesser General Public License as published by 
# the Free Software Foundation; either version 3 of the License, or 
# (at your option) any later version.
#
# The PyFlowGo library is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
#
# You should have received copies of the GNU Lesser General Public License 
# along with the PyFlowGo library.  If not, see https://www.gnu.org/licenses/.

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
