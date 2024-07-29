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

import json
import math
import pyflowgo.base.flowgo_base_vesicle_fraction_model


class FlowGoVesicleFractionModelPoly(pyflowgo.base.flowgo_base_vesicle_fraction_model.
                                        FlowGoBaseVesicleFractionModel):


    """ This method "variable" considers the volume fraction of vesicle (bubbles) to vary linearly with distnace from the vent.

        %vesicles = vesicle_poly_a * math.pow(distance,2) + b * distance + c

        for Kileauea 2018
        vesicle_fraction_1 = 0.7415
        vesicle_poly_a = -1.4e-9
        vesicle_poly_b = -2.16e-5

        Input data
        -----------
        json file containing the fraction of vesicle and the polynomial coeficients

        variables
        -----------
        distance = 0 in the json file and then is calculated down flow

        Returns
        ------------
        new_vesicle fraction

        """
    def __init__(self) -> None:
        super().__init__()
        # this is the Volume fraction considered constant along the flow
        self._vesicle_fraction = 0.1

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

            self._vesicle_fraction = float(data['lava_state']['vesicle_fraction'])
            self._vesicle_poly_a = float(data['lava_state']['vesicle_poly_a'])
            self._vesicle_poly_b = float(data['lava_state']['vesicle_poly_b'])

    def computes_vesicle_fraction(self, state):

        """this function permits to calculate the new vesicle fraction"""
        current_position = state.get_current_position()
        vesicle_fraction = (self._vesicle_fraction + self._vesicle_poly_b * current_position +
                            self._vesicle_poly_a * math.pow(current_position,2))

        if vesicle_fraction <= 0:
            vesicle_fraction = 0
            return vesicle_fraction
        else:
            return vesicle_fraction