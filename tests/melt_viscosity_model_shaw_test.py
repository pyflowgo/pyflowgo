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
import pyflowgo.flowgo_melt_viscosity_model_shaw
import pyflowgo.flowgo_state


class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_melt_viscosity_model.json'

        melt_viscosity_model_shaw = pyflowgo.flowgo_melt_viscosity_model_shaw.FlowGoMeltViscosityModelShaw()
        melt_viscosity_model_shaw.read_initial_condition_from_json_file(filename)
        self.assertEqual(melt_viscosity_model_shaw._shaw_slope,2.36)

    def test_computes_melt_viscosity(self):
        filename = './resources/input_parameters_melt_viscosity_model.json'

        melt_viscosity_model_shaw = pyflowgo.flowgo_melt_viscosity_model_shaw.FlowGoMeltViscosityModelShaw()
        melt_viscosity_model_shaw.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1200)

        melt_viscosity = melt_viscosity_model_shaw.compute_melt_viscosity(state)
        self.assertAlmostEqual(melt_viscosity, 1672.9255910394, 10)

if __name__ == '__main__':
    unittest.main()
