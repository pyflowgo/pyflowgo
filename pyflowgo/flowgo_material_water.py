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

import math
import json


class FlowGoMaterialWater:

    def __init__(self) -> None:
        super().__init__()

        self._temp_water = 10. + 273.15  # temperature of the water [K]
        self._water_current_speed = 5.0  # Water current speed [m/s]
        self._ch_water = 0.0036  # value from Greeley and Iverson (1987) C_H= (U'/U)^2 where U' is the fraction of wind speed according to Kesztheleyi and Denlinger (1996)
        self._rho_water = 0.4412  # density of the water [kg/m3]
        self._cp_water = 1099.  # water specific heat capacity [J kg-1 K-1]

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._temp_water = float(data['convection_parameters']['water_temperature'])
            self._water_current_speed = float(data['convection_parameters']['water_current_speed'])
            self._ch_water = float(data['convection_parameters']['ch_water'])
            self._rho_water = float(data['convection_parameters']['water_density'])
            self._cp_water = float(data['convection_parameters']['water_specific_heat_capacity'])

    def compute_conv_heat_transfer_coef_water(self):
        #return 35
        return self._ch_water * self._rho_water * self._cp_water * self._water_current_speed

    def get_temperature(self):
        return self._temp_water
