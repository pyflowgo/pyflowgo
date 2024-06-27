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

import pyflowgo.base.flowgo_base_flux


class FlowGoFluxConvectionHeatWater(pyflowgo.base.flowgo_base_flux.FlowGoBaseFlux):

    def __init__(self, terrain_condition, material_water, material_lava, crust_temperature_model, effective_cover_crust_model):
        self._material_water = material_water
        self._material_lava = material_lava
        self._terrain_condition = terrain_condition
        self._crust_temperature_model = crust_temperature_model
        self._effective_cover_crust_model = effective_cover_crust_model
        self.logger = pyflowgo.flowgo_logger.FlowGoLogger()

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._temp_water = float(data['convection_parameters']['water_temperature'])
            self._water_speed = float(data['convection_parameters']['water_speed'])
            self._water_thermal_conductivity = float(data['convection_parameters']['water_thermal_conductivity'])
            self._rho_water = float(data['convection_parameters']['water_density'])
            self._cp_water = float(data['convection_parameters']['water_specific_heat_capacity'])
            self._effusivity_water = float(data['convection_parameters']['E_water'])
            self._water_dynamic_visco = float(data['convection_parameters']['water_dynamic_visco'])
            self._water_kinematic_visco = float(data['convection_parameters']['water_kinematic_visco'])
            self._gravity=float(data['terrain_conditions']['gravity'])
    def compute_characteristic_surface_temperature(self, state, terrain_condition):
        """ This is Tconv of Harris and Rowland"""
        crust_temperature = self._crust_temperature_model.compute_crust_temperature(state)
        effective_cover_fraction = self._effective_cover_crust_model.compute_effective_cover_fraction(state)
        molten_material_temperature = self._material_lava.computes_molten_material_temperature(state)
        characteristic_surface_temperature = math.pow((effective_cover_fraction * crust_temperature **
                                                       1.333 + (1. - effective_cover_fraction) *
                                                       molten_material_temperature ** 1.333),0.75)
        self.logger.add_variable("characteristic_surface_temperature", state.get_current_position(),
                                 characteristic_surface_temperature)
        return characteristic_surface_temperature

    def compute_length_scale(self, channel_width):
        length_scale = (channel_width) / (2 + 2 * channel_width)         #1 corresponds to the volume unity
        print("length_scale", length_scale)
        print("channel_width", channel_width)
        return length_scale

    def compute_prandlt_number(self):
        prandlt_number = (self._water_dynamic_visco*self._cp_water)/self._water_thermal_conductivity
        print("prandlt_number",prandlt_number)
        return prandlt_number

    def compute_rayleight_number(self, state, channel_width):
        length_scale = self.compute_length_scale(channel_width)
        prandlt_number = self.compute_prandlt_number()
        water_temperature = self._material_water.get_temperature()
        water_kinematic_visco = self._water_kinematic_visco
        gravity = self._gravity
        characteristic_surface_temperature = self.compute_characteristic_surface_temperature \
            (state, self._terrain_condition)

        T = (characteristic_surface_temperature - water_temperature)/2.
        B = 1./T
        
        grasholf_number = (gravity * B * (characteristic_surface_temperature-water_temperature)/water_kinematic_visco**2)*length_scale**3
       
        rayleight_number = prandlt_number * grasholf_number
        
        print("water_temperature",water_temperature)
        print("T=",T)
        print("B=", B)
        print("water_kinematic_visco",water_kinematic_visco)
        print("characteristic_surface_temperature", characteristic_surface_temperature)
        print("grasholf_number", grasholf_number)
        print("rayleight_number",rayleight_number)
        return rayleight_number
    
    def compute_hfree(self,state, channel_width):
        length_scale = self.compute_length_scale(channel_width)
        rayleight_number = self.compute_rayleight_number(state, channel_width)

        if rayleight_number < 10 ** 9:
            Nu = 0.59 * rayleight_number ** (1 / 4)
            hfree = (Nu * self._water_thermal_conductivity) / length_scale
        else:
            Nu = 0.1 * rayleight_number ** (1 / 3)
            hfree = (Nu * self._water_thermal_conductivity) / length_scale
        
        print("Nu",Nu)
        print("hfree", hfree)
        return hfree
    def compute_qconvfree(self, state, channel_width):
        hfree = self.compute_hfree(state, channel_width)
        water_temperature = self._material_water.get_temperature()
        water_thermal_conductivity = self._water_thermal_conductivity        
        characteristic_surface_temperature = self.compute_characteristic_surface_temperature \
            (state, self._terrain_condition)

        qconvfree = hfree*(characteristic_surface_temperature - water_temperature) * channel_width
        
        print("qconvfree", qconvfree)
        return qconvfree
    
    def compute_hforced(self, channel_width):
        water_temperature = self._material_water.get_temperature()
        water_thermal_conductivity = self._water_thermal_conductivity
        prandlt_number = self.compute_prandlt_number()
        reynolds_number = self._water_speed * channel_width / self._water_kinematic_visco

        if reynolds_number < 5e5:
            Nu = 0.332 * reynolds_number ** (1 / 2) * prandlt_number ** (1 / 3)
            hforced = 2 * (Nu * water_thermal_conductivity) / channel_width
        else:
            Nu = 0.0296 * reynolds_number ** (4 / 5) * prandlt_number ** (1 / 3)
            hforced = 2 * (Nu * water_thermal_conductivity) / channel_width
        
        print("prandlt_number",prandlt_number)
        print("reynolds_number",reynolds_number)
        print("Nu",Nu)
        print("hforced", hforced)        
        return hforced
    def compute_qconvforced(self, state, channel_width):
        water_temperature = self._material_water.get_temperature()
        hforced = self.compute_hforced(channel_width)
        characteristic_surface_temperature = self.compute_characteristic_surface_temperature \
            (state, self._terrain_condition)

        qconvforced = hforced*(characteristic_surface_temperature - water_temperature) * channel_width
        print("qconvforced", qconvforced )
        return qconvforced    

    def compute_flux(self, state, channel_width, channel_depth):
        qconvforced = self.compute_qconvforced(state, channel_width)
        qconvfree = self.compute_qconvfree(state, channel_width)
        hfree = self.compute_hfree(state, channel_width)
        hforced = self.compute_hforced(channel_width)

        if hfree<hforced:
            qconv = qconvforced  
        else:
            qconv = qconvfree
        
        #log Snyder flux to zero
        effective_temperature_snyder = 0
        flowgofluxsnyderheat = 0
        self.logger.add_variable("effective_temperature_snyder", state.get_current_position(),
                                 effective_temperature_snyder)
        self.logger.add_variable("flowgofluxsnyderheat", state.get_current_position(), flowgofluxsnyderheat)
        print("qconv",qconv)
        return qconv
