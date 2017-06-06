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

import math

import pyflowgo.flowgo_melt_viscosity_model_shaw
import pyflowgo.flowgo_relative_viscosity_model_kd
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_vesicle_fraction_model_constant
import json

class FlowGoMaterialLava:

    _eruption_temperature = 1137. + 273.15
    _buffer = 0.
    _latent_heat_of_crystallization = 350000.  # L [K.Kg-1]
    _density_dre = 2600.

    def __init__(self, melt_viscosity_model=None, relative_viscosity_model=None, yield_strength_model=None, vesicle_fraction_model=None):
        super().__init__()

        # TODO: Raise a warning here that the default model is used if no model has been passed
        # TODO: Check that the models are in the good ABC type

        if melt_viscosity_model == None:
            self._melt_viscosity_model = pyflowgo.flowgo_melt_viscosity_model_shaw.FlowGoMeltViscosityModelShaw()
        else:
            self._melt_viscosity_model = melt_viscosity_model

        if relative_viscosity_model == None:
            self._relative_viscosity_model = pyflowgo.flowgo_relative_viscosity_model_kd.FlowGoRelativeViscosityModelKD()
        else:
            self._relative_viscosity_model = relative_viscosity_model

        if yield_strength_model == None:
            self._yield_strength_model = pyflowgo.flowgo_yield_strength_model_basic.FlowGoYieldStrengthModelBasic()
        else:
            self._yield_strength_model = yield_strength_model

        if vesicle_fraction_model == None:
            self._vesicle_fraction_model = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        else:
            self._vesicle_fraction_model = vesicle_fraction_model

    def read_initial_condition_from_json_file(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            self._eruption_temperature = float(data['eruption_condition']['eruption_temperature'])
            self._buffer = float(data['thermal_parameters']['buffer'])
            self._latent_heat_of_crystallization = float(data['crystals_parameters']['latent_heat_of_crystallization'])
            self._density_dre = float(data['lava_state']['density_dre'])

    def get_eruption_temperature(self):
        return self._eruption_temperature  # [K]

    def get_latent_heat_of_crystallization(self):
        return self._latent_heat_of_crystallization  # L [K.Kg-1]

    def computes_molten_material_temperature(self, state):
        return state.get_core_temperature() - self._buffer  # [K]

    def computes_bulk_viscosity(self, state):
        bulk_viscosity = self._melt_viscosity_model.compute_melt_viscosity(state) * \
                         self._relative_viscosity_model.compute_relative_viscosity(state)
        return bulk_viscosity  # [Pa/s]

    def compute_mean_velocity(self, state, terrain_condition):
        channel_depth = terrain_condition.get_channel_depth(state.get_current_position())
        bulk_viscosity = self.computes_bulk_viscosity(state)
        tho_0 = self._yield_strength_model.compute_yield_strength(state, self._eruption_temperature)
        tho_b = self._yield_strength_model.compute_basal_shear_stress(state, terrain_condition, self)

        v_mean = ((channel_depth * tho_b) / (3. * bulk_viscosity)) * (
            1. - (3. / 2.) * (tho_0 / tho_b) + 0.5 * ((tho_0 / tho_b) ** 3.))

        return v_mean  # [m/s]

    def computes_vesicle_fraction(self, state):
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)
        return vesicle_fraction

    def get_bulk_density(self, state):
        vesicle_fraction = self.computes_vesicle_fraction(state)
        bulk_density = self._density_dre * (1. - vesicle_fraction)  # [kg/m3]
        return bulk_density  # [kg/m3]
