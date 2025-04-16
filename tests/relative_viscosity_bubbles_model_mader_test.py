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
import pyflowgo.flowgo_relative_viscosity_model_mp_mueller2010
import pyflowgo.flowgo_relative_viscosity_bubbles_model_mader
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant

class MyTestCase(unittest.TestCase):

    def test_compute_relative_viscosity(self):
        filename = './resources/input_parameters_relative_viscosity_model_mader.json'
        state = pyflowgo.flowgo_state.FlowGoState()

        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)
        state.set_core_temperature(1419.15)  # this is in Kelvin
        melt_viscosity = melt_viscosity_model_vft.compute_melt_viscosity(state)
        self.assertAlmostEqual(melt_viscosity, 318.6256524, 4)
        print("melt viscosity ok")

        relative_viscosity_model_mp_mueller = pyflowgo.flowgo_relative_viscosity_model_mp_mueller2010.FlowGoRelativeViscosityModelMPMUELLER()
        relative_viscosity_model_mp_mueller.read_initial_condition_from_json_file(filename)
        state.set_crystal_fraction(0.2)
        relative_viscosity_crystals = relative_viscosity_model_mp_mueller.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity_crystals,2.9033817, 4)
        print("relative_viscosity_crystals ok")


        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)


        relative_viscosity_bubbles_model_mader = pyflowgo.flowgo_relative_viscosity_bubbles_model_mader. \
            FlowGoRelativeViscosityBubblesModelMader(vesicle_fraction_model=vesicle_fraction_model_constant,
                                              melt_viscosity_model=melt_viscosity_model_vft,
                                                     relative_viscosity_model = relative_viscosity_model_mp_mueller)
        relative_viscosity_bubbles_model_mader.read_initial_condition_from_json_file(filename)

        state.set_strain_rate(1.0)
        relative_viscosity_bubbles = relative_viscosity_bubbles_model_mader.compute_relative_viscosity_bubbles(state)
        self.assertAlmostEqual(relative_viscosity_bubbles, 0.182181456, 3)
        print("relative_viscosity ok for  strain-rate=1, vesicle=0.64")
        
        state.set_strain_rate(0.0001)
        relative_viscosity_bubbles = relative_viscosity_bubbles_model_mader.compute_relative_viscosity_bubbles(state)
        self.assertAlmostEqual(relative_viscosity_bubbles, 2.777777778, 3)
        print("relative_viscosity ok for strain-rate=0.0001, vesicle=0.64")



if __name__ == '__main__':
    unittest.main()
