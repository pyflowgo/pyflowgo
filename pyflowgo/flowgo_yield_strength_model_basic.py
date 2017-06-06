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
import json
import pyflowgo.flowgo_logger


import pyflowgo.base.flowgo_base_yield_strength_model


class FlowGoYieldStrengthModelBasic(pyflowgo.base.flowgo_base_yield_strength_model.FlowGoBaseYieldStrengthModel):
    # TODO: here I add the log
    def __init__(self):
        self.logger = pyflowgo.flowgo_logger.FlowGoLogger()

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._eruption_temperature = float(data['eruption_condition']['eruption_temperature'])

    def compute_yield_strength(self, state, eruption_temperature):
        # yield_strength is tho_0
        b = 0.01  # Constant B given by Dragoni, 1989[Pa]
        c = 0.08  # Constant C given by Dragoni, 1989[K-1]
        core_temperature = state.get_core_temperature()
        crystal_fraction = state.get_crystal_fraction()

        # the new yield strength is calculated using this new T and the corresponding slope:
        tho_0 = b * (math.exp(c * (self._eruption_temperature - core_temperature) - 1.)) + (6500. * (crystal_fraction ** 2.85))
        # TODO: here I add the log
        self.logger.add_variable("tho_0", state.get_current_position(),tho_0)
        #print("tho_0=",tho_0)
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
        # TODO: here I add the log
        self.logger.add_variable("tho_b", state.get_current_position(), tho_b)
        #("tho_b=", tho_b)
        return tho_b
