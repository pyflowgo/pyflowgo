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
import pyflowgo.flowgo_relative_viscosity_model_costa2
import pyflowgo.flowgo_state

class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_relative_viscosity_model_costa_1s-1.json'

        relative_viscosity_model_costa2 = pyflowgo.flowgo_relative_viscosity_model_costa2.FlowGoRelativeViscosityModelCosta2()
        relative_viscosity_model_costa2.read_initial_condition_from_json_file(filename)

        self.assertEqual(relative_viscosity_model_costa2._strain_rate, 1.0)

    def test_computes_relative_viscosity(self):
        filename = './resources/input_parameters_relative_viscosity_model_costa_1s-1.json'
        relative_viscosity_model_costa2 = pyflowgo.flowgo_relative_viscosity_model_costa2.FlowGoRelativeViscosityModelCosta2()
        relative_viscosity_model_costa2.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)
        relative_viscosity = relative_viscosity_model_costa2.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 2.5801670393,10)

        filename_2 = './resources/input_parameters_relative_viscosity_model_costa_1s-4.json'
        relative_viscosity_model_costa2 = pyflowgo.flowgo_relative_viscosity_model_costa2.FlowGoRelativeViscosityModelCosta2()
        relative_viscosity_model_costa2.read_initial_condition_from_json_file(filename_2)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)
        relative_viscosity = relative_viscosity_model_costa2.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 2.9347017411, 10)

if __name__ == '__main__':
    unittest.main()
