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
import pyflowgo.flowgo_logger

import pyflowgo.base.flowgo_base_yield_strength_model

class FlowGoYieldStrengthModelBLL(pyflowgo.base.flowgo_base_yield_strength_model.FlowGoBaseYieldStrengthModel):
    """
        This function calculates the effect of crystal and bubble cargo on yield strength using the model of
        Birnbaum, Lev, and Llewellin (2021):

        tho_0 = math.pow(10,61*(phi/(1-vesicle_fraction) - phicrit)) +
                math.exp(1.98*(phi/(1-vesicle_fraction) + vesicle_fraction - phicrit))


        on the basis of analogue experiments where phi_crit was 0.34

        Input data
        -----------
        critical packing fractions for particles and bubbles (phicrit)

        variables
        -----------
        crystal fraction: phi
        vesicle fraction: vesicle_fraction

        Returns
        ------------
        the yield strength due to the crystal and bubble cargo

        Reference
        ---------

        Birnbaum, J., Lev, E., Llewellin, E. W. (2021) Rheology of three-phase suspensions determined
        via dam-break experiments. Proc. R. Soc. A 477 (20210394): 1-16.

        """
    def __init__(self, vesicle_fraction_model=None, melt_viscosity_model=None):
        self.logger = pyflowgo.flowgo_logger.FlowGoLogger()
        self._eruption_temperature = None

        if vesicle_fraction_model == None:
            self._vesicle_fraction_model = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        else:
            self._vesicle_fraction_model = vesicle_fraction_model

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._eruption_temperature = float(data['eruption_condition']['eruption_temperature'])
            self._critphi = float(data['relative_viscosity_parameters']['crit_packing'])

    def compute_yield_strength(self, state, eruption_temperature):
        phi = state.get_crystal_fraction()
        vesicle_fraction = self._vesicle_fraction_model.computes_vesicle_fraction(state)

        phi_crit = 0.34
        tho_0 = math.pow(10, 61 * (phi / (1 - vesicle_fraction) - self._critphi)) + math.exp(
            1.98 * (phi / (1 - vesicle_fraction) + vesicle_fraction - self._critphi))
        return tho_0

    def compute_basal_shear_stress(self, state, terrain_condition, material_lava):
        #basal_shear_stress is tho_b

        g = terrain_condition.get_gravity(state.get_current_position)
        #print('g =', str(g))
        bulk_density = material_lava.get_bulk_density(state)
        #print('bulk_density =', str(bulk_density))
        channel_depth = terrain_condition.get_channel_depth(state.get_current_position())
        channel_slope = terrain_condition.get_channel_slope(state.get_current_position())

        tho_b = channel_depth * bulk_density * g * math.sin(channel_slope)
        return tho_b

    def yield_strength_notcompatible(self, state, terrain_condition, material_lava):
        tho_0 = self.compute_yield_strength(state, self._eruption_temperature)
        tho_b = self.compute_basal_shear_stress(state, terrain_condition, material_lava)
        if tho_0 >= tho_b:
            return True
        else:
            return False
