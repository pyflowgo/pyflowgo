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

#The density, thermal conductivity, specific heat capacity and dynamic viscosity of seawater have been estimated at T = 2°C, S = 26.1 and P = 300 bar

class FlowGoMaterialWater:

    def __init__(self) -> None:
        super().__init__()

        self._temp_water = 2. + 273.15  # temperature of the seawater [K]
        self._water_speed = 1.0  # Seawater speed [m/s]
        self._k_water = 0.581  # Seawater thermal conductivity [W m-1 K-1]
        self._rho_water = 1040.  # density of the seawater [kg/m3]
        self._cp_water = 3945.  # Seawater specific heat capacity [J kg-1 K-1]
        self._effusivity_water = 1505.41 # Effusivity of the seawater [J K-1 m-2 s-1/2] 
        self._dynamic_visco_water = 1.75E-03 # Dynamic viscosity of the seawater [Pa s] 
        self._kinematic_visco_water = 1.72E-06 # Kinematic viscosity of the seawater [m2 s-1] 


    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._temp_water = float(data['convection_parameters']['water_temperature'])
            self._water_speed = float(data['convection_parameters']['water_speed'])
            self._k_water = float(data['convection_parameters']['k_water'])
            self._rho_water = float(data['convection_parameters']['water_density'])
            self._cp_water = float(data['convection_parameters']['water_specific_heat_capacity'])
            self._effusivity_water = float(data['convection_parameters']['E_water'])
            self._dynamic_visco_water = float(data['convection_parameters']['water_dynamic_visco'])
            self._kinematic_visco_water = float(data['convection_parameters']['water_kinematic_visco'])
    
    def compute_conv_heat_transfer_coef_water(self):
        #return 35
        return self._k_water * self._rho_water * self._cp_water * self._water_speed

    def get_temperature(self):
        return self._temp_water
