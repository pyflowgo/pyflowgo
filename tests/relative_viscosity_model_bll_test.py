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
import sys
import os
# Ajoute le dossier parent du script (main) au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyflowgo.flowgo_relative_viscosity_model_bll
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_melt_viscosity_model_vft

class MyTestCase(unittest.TestCase):
    def test_compute_relative_viscosity_bll(self):
        filename = './resources/input_parameters_bll.json'
        state = pyflowgo.flowgo_state.FlowGoState()

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)
        state.set_core_temperature(1419.15)  # this is in Kelvin
        melt_viscosity = melt_viscosity_model_vft.compute_melt_viscosity(state)
        self.assertAlmostEqual(melt_viscosity, 318.6256524, 4)
        print("melt viscosity ok")

        relative_viscosity_model_bll = pyflowgo.flowgo_relative_viscosity_model_bll. \
            FlowGoRelativeViscosityModelBLL(vesicle_fraction_model=vesicle_fraction_model_constant,
                                            melt_viscosity_model=melt_viscosity_model_vft)

        relative_viscosity_model_bll.read_initial_condition_from_json_file(filename)

        self.assertEqual(relative_viscosity_model_bll._phimax, 0.56)
        self.assertEqual(relative_viscosity_model_bll._Bsolid, 2.74)

        state.set_crystal_fraction(0.15)
        state.set_strain_rate(0.001)

        vesicle_fraction = vesicle_fraction_model_constant.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.64)
        print("vesicle fraction ok")

        relative_viscosity = relative_viscosity_model_bll.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 77.160624, 6)  # model at phi = 0.15, phi_b = 0.64


if __name__ == '__main__':
    unittest.main()
