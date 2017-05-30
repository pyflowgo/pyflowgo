import math
import json

import pyflowgo.base.flowgo_base_flux


class FlowGoFluxViscousHeating(pyflowgo.base.flowgo_base_flux.FlowGoBaseFlux):

    def __init__(self, terrain_condition, material_lava):
        self._material_lava = material_lava
        self._terrain_condition = terrain_condition


    def compute_flux(self, state, channel_width, channel_depth):
        bulk_viscosity = self._material_lava.computes_bulk_viscosity(state)
        v_mean = self._material_lava.compute_mean_velocity(state, self._terrain_condition)
        qviscous = bulk_viscosity * (v_mean / channel_depth) ** 2. * channel_width
        return qviscous

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
