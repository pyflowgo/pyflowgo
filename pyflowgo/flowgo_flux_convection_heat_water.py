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
        
    
    def compute_lentgh_scale(self, channel_width):
        
        length_scale = (1*channel_width) / (2*1 + 2*channel_width)         #1 corresponds to the volume unity
        
        return length_scale
    
    
    def compute_prandlt_number(self):
        dynamic_visco_water = self._dynamic_visco_water
        cp_water = self._cp_water
        water_thermal_conductivity = self._water_thermal_conductivity
        
        prandlt_number = (dynamic_visco_water*cp_water)/water_thermal_conductivity
        
        return prandlt_number
    
    
    def compute_rayleight_number(self, state, channel_width):
        water_temperature = self._material_water.get_temperature()
        kinematic_visco_water = self._kinematic_visco_water
        gravity = self._gravity
        
        T = (characteristic_surface_temperature - water_temperature)/2.
        B = 1./T
        
        grasholf_number = ((gravity * B * (characteristic_surface_temperature-water_temperature)/kinematic_visco_water**2)*length_scale**3
        
        rayleight_number = prandlt_number * grasholf_number
        
        return rayleight_number
        
    
    def compute_qconvfree(self, state):
        water_temperature = self._material_water.get_temperature()
        water_thermal_conductivity = self._water_thermal_conductivity        
        
        if rayleight_number < 10**9:
            Nu = 0.59*rayleight_number**(1/4)
            hfree = (Nu*water_thermal_conductivity)/length_scale
            qconvfree = hfree*(characteristic_surface_temperature - water_temperature) * channel_width
        else:
            Nu = 0.1*rayleight_number**(1/3)
            hfree = (Nu*water_thermal_conductivity)/length_scale
            qconvfree = hfree*(characteristic_surface_temperature - water_temperature) * channel_width
        return qconvfree
        
    
    def compute_reynolds_number(self, channel_width):
        water_speed = self._water_speed
        kinematic_visco_water = self._kinematic_visco_water
        
        reynolds_number = (water_speed*channel_width)/kinematic_visco_water
        
        return reynolds_number    
    
    
    def compute_qconvforced(self, state, channel_width):
        water_temperature = self._material_water.get_temperature()
        water_thermal_conductivity = self._water_thermal_conductivity       
        
        if reynolds_number < 5*10**5:
            Nu = 0.332*reynolds_number**(1/2)*prandlt_number**(1/3)
            hforced = 2*(Nu*water_thermal_conductivity)/channel_width
            qconvforced = hforced*(characteristic_surface_temperature - water_temperature) * channel_width
        else:
            Nu = 0.0296*reynolds_number**(4/5)*prandlt_number**(1/3)
            hforced = 2*(Nu*water_thermal_conductivity)/channel_width
            qconvforced = hforced*(characteristic_surface_temperature - water_temperature) * channel_width
        return qconvforced    


    def compute_flux(self, state, channel_width, channel_depth):

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

        return qconv

  
    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)

