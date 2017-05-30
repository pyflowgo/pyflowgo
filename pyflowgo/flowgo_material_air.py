import math
import json


class FlowGoMaterialAir:
    _temp_air = 10. + 273.15  # temperature of the air [K]
    _wind_speed = 5.0  # Wind speed [m/s]
    _ch_air = 0.0036  # value from Greeley and Iverson (1987) C_H= (U'/U)^2 where U' is the fraction of wind speed according to Kesztheleyi and Denlinger (1996)
    _rho_air = 0.4412  # density of the air [kg/m3]
    _cp_air = 1099.  # Air specific heat capacity [J kg-1 K-1]

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._temp_air = float(data['convection_parameters']['air_temperature'])
            self._wind_speed = float(data['convection_parameters']['wind_speed'])
            self._ch_air = float(data['convection_parameters']['ch_air'])
            self._rho_air = float(data['convection_parameters']['air_density'])
            self._cp_air = float(data['convection_parameters']['air_specific_heat_capacity'])


    def compute_conv_heat_transfer_coef(self):
        return self._ch_air * self._rho_air * self._cp_air * self._wind_speed

    def get_temperature(self):
        return self._temp_air
