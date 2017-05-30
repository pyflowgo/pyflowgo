import math
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_material_air
import pyflowgo.flowgo_state
import pyflowgo.flowgo_crust_temperature_model_constant
import json

import pyflowgo.base.flowgo_base_flux

class FlowGoFluxHeatLossRain(pyflowgo.base.flowgo_base_flux.FlowGoBaseFlux):

    def __init__(self):
        self._rainfall_rate = 7.98e-8  # Keiszthelyi 1995a
        self._density_water = 958.  # [kg/m3]
        self._latent_heat_vaporization = 2.8e6  # [J/kg]

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._rainfall_rate = float(data['rain_parameters']['rainfall_rate'])
            self._density_water = float(data['rain_parameters']['density_water'])
            self._latent_heat_vaporization = float(data['rain_parameters']['latent_heat_vaporization'])

    def compute_flux(self, state, channel_width, channel_depth):
        qrain = self._rainfall_rate * self._density_water * self._latent_heat_vaporization * channel_width
        return qrain
