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
import pyflowgo.flowgo_relative_viscosity_model_kd
import pyflowgo.flowgo_state

class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_relative_viscosity_model.json'

        relative_viscosity_model_kd = pyflowgo.flowgo_relative_viscosity_model_kd.FlowGoRelativeViscosityModelKD()
        relative_viscosity_model_kd.read_initial_condition_from_json_file(filename)
        self.assertEqual(relative_viscosity_model_kd._phimax, 0.641)
        self.assertEqual(relative_viscosity_model_kd._beinstein, 3.27)

    def test_computes_relative_viscosity(self):
        filename = './resources/input_parameters_relative_viscosity_model.json'
        relative_viscosity_model_kd = pyflowgo.flowgo_relative_viscosity_model_kd.FlowGoRelativeViscosityModelKD()
        relative_viscosity_model_kd.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)
        relative_viscosity = relative_viscosity_model_kd.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 2.18999193613,10)

if __name__ == '__main__':
    unittest.main()
