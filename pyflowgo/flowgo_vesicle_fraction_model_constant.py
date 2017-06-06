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

import json
import pyflowgo.base.flowgo_base_vesicle_fraction_model

class FlowGoVesicleFractionModelConstant(pyflowgo.base.flowgo_base_vesicle_fraction_model.
                                        FlowGoBaseVesicleFractionModel):
    # TODO: comment the function

    # this is the Volume fraction considered constant along the flow
    _vesicle_fraction = 0.1

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._vesicle_fraction = float(data['lava_state']['vesicle_fraction'])

    def computes_vesicle_fraction(self, state):
        vesicle_fraction = self._vesicle_fraction
        return vesicle_fraction

