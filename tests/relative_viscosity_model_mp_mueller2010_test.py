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

import sys
import os
# Ajoute le dossier parent du script (main) au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pyflowgo.flowgo_relative_viscosity_model_mp_mueller2010
import pyflowgo.flowgo_state

class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_relative_viscosity_model_mader.json'

        relative_viscosity_model_mp_mueller2010 = pyflowgo.flowgo_relative_viscosity_model_mp_mueller2010.\
            FlowGoRelativeViscosityModelMPMUELLER()
        relative_viscosity_model_mp_mueller2010.read_initial_condition_from_json_file(filename)

        self.assertEqual(relative_viscosity_model_mp_mueller2010._Rp, 3.2)

    def test_computes_relative_viscosity(self):
        filename = './resources/input_parameters_relative_viscosity_model.json'
        relative_viscosity_model_mp_mueller2010 = pyflowgo.flowgo_relative_viscosity_model_mp_mueller2010.\
            FlowGoRelativeViscosityModelMPMUELLER()
        relative_viscosity_model_mp_mueller2010.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)
        relative_viscosity = relative_viscosity_model_mp_mueller2010.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 2.9033817,6)

if __name__ == '__main__':
    unittest.main()
