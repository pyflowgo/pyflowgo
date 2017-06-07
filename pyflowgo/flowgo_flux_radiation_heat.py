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
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_material_air
import pyflowgo.flowgo_state
import pyflowgo.flowgo_crust_temperature_model_constant
import pyflowgo.flowgo_effective_cover_crust_model_basic
import pyflowgo.flowgo_logger
import json

import pyflowgo.base.flowgo_base_flux

class FlowGoFluxRadiationHeat(pyflowgo.base.flowgo_base_flux.FlowGoBaseFlux):

    #def __init__(self, terrain_condition, material_lava, crust_temperature_model):
    def __init__(self, terrain_condition, material_lava, crust_temperature_model, effective_cover_crust_model):
        self._material_lava = material_lava
        self._crust_temperature_model = crust_temperature_model
        self._terrain_condition = terrain_condition
        self._effective_cover_crust_model = effective_cover_crust_model
        self.logger = pyflowgo.flowgo_logger.FlowGoLogger()
        self._sigma = 0.0000000567  # Stefan-Boltzmann [W m-1 K-4]
        self._epsilon = 0.95  # Emissivity

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._sigma = float(data['radiation_parameters']['stefan-boltzmann_sigma'])
            self._epsilon = float(data['radiation_parameters']['emissivity_epsilon'])

    def _compute_effective_radiation_temperature(self, state, terrain_condition):

        #effective_cover_fraction = self._material_lava.compute_effective_cover_fraction(state, terrain_condition)

        # TODO call effective_cover_fraction from a model like this:
        effective_cover_fraction = self._effective_cover_crust_model.compute_effective_cover_fraction(state)

        # the effective radiation temperature of the
        # surface (Te) is given by (Pieri & Baloga 1986; Crisp & Baloga, 1990; Pieri et al. 1990):
        # The user is free to adjust the model, for example, f_crust can be set as a constant or can be varied
        # downflow as a function of velocity (Harris & Rowland 2001). See in material_lava
        # the effective radiation temperature of the surface (Te) is given by (Pieri & Baloga 1986;
        # Crisp & Baloga, 1990; Pieri et al. 1990):

        crust_temperature = self._crust_temperature_model.compute_crust_temperature(state)

        molten_material_temperature = self._material_lava.computes_molten_material_temperature(state)

        effective_radiation_temperature = math.pow(effective_cover_fraction * crust_temperature ** 4. +
                                               (1. - effective_cover_fraction) * molten_material_temperature ** 4.,
                                               0.25)

        self.logger.add_variable("effective_radiation_temperature", state.get_current_position(),
                                 effective_radiation_temperature)
        return effective_radiation_temperature

    def compute_flux(self, state, channel_width, channel_depth):
        effective_radiation_temperature = self._compute_effective_radiation_temperature \
            (state, self._terrain_condition)

        qradiation = self._sigma * self._epsilon * (effective_radiation_temperature ** 4.) * channel_width
        return qradiation
