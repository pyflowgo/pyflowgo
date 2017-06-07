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
import pyflowgo.flowgo_vesicle_fraction_model_bimodal
import pyflowgo.flowgo_state


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_vesicle_fraction_model_bimodal.json'

        vesicle_fraction_model_bimodal = pyflowgo.flowgo_vesicle_fraction_model_bimodal.FlowGoVesicleFractionModelBimodal()
        vesicle_fraction_model_bimodal.read_initial_condition_from_json_file(filename)

        self.assertEqual(vesicle_fraction_model_bimodal._vesicle_fraction_1, 0.6)
        self.assertEqual(vesicle_fraction_model_bimodal._vesicle_fraction_2, 0.2)

    def test_vesicle_fraction_model_bimodal(self):
        filename = './resources/input_parameters_vesicle_fraction_model_bimodal.json'

        vesicle_fraction_model_bimodal = pyflowgo.flowgo_vesicle_fraction_model_bimodal.FlowGoVesicleFractionModelBimodal()
        vesicle_fraction_model_bimodal.read_initial_condition_from_json_file(filename)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(10)
        vesicle_fraction = vesicle_fraction_model_bimodal.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.6)

        state.set_current_position(11000)
        vesicle_fraction = vesicle_fraction_model_bimodal.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.2)

if __name__ == '__main__':
    unittest.main()

