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
import pyflowgo.flowgo_relative_viscosity_model_ptp1
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant


class MyTestCase(unittest.TestCase):

    def test_compute_relative_viscosity(self):
        filename = './resources/input_parameters_vesicle_fraction_model_constant.json'

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        relative_viscosity_model_ptp1 = pyflowgo.flowgo_relative_viscosity_model_ptp1. \
            FlowGoRelativeViscosityModelPhanThienPham1(vesicle_fraction_model=vesicle_fraction_model_constant)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)

        relative_viscosity = relative_viscosity_model_ptp1.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 21.093750000,10)

if __name__ == '__main__':
    unittest.main()
