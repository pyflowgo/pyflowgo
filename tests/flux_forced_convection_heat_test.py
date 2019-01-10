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

import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_material_air
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_flux_forced_convection_heat
import pyflowgo.flowgo_crust_temperature_model_constant
import pyflowgo.flowgo_effective_cover_crust_model_basic

class MyTestCase(unittest.TestCase):


    def test_compute_compute_characteristic_surface_temperature(self):
        filename = './resources/input_parameters_forced_convection_heat_flux.json'

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)

        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1387.13335767292)
        state.set_crystal_fraction(0.104)
        state.set_current_position(10)

        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)

        relative_viscosity_model_er = pyflowgo.flowgo_relative_viscosity_model_er.FlowGoRelativeViscosityModelER()
        relative_viscosity_model_er.read_initial_condition_from_json_file(filename)

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        yield_strength_model_basic = pyflowgo.flowgo_yield_strength_model_basic.FlowGoYieldStrengthModelBasic()
        yield_strength_model_basic.read_initial_condition_from_json_file(filename)

        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(melt_viscosity_model=melt_viscosity_model_vft,
                                                                         relative_viscosity_model=relative_viscosity_model_er,
                                                                         yield_strength_model=yield_strength_model_basic,
                                                                         vesicle_fraction_model=vesicle_fraction_model_constant)
        material_lava.read_initial_condition_from_json_file(filename)
        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)
        print(mean_velocity)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)

        flowgo_flux_forced_convection_heat = pyflowgo.flowgo_flux_forced_convection_heat. \
            FlowGoFluxForcedConvectionHeat(terrain_condition,
                                           material_air, material_lava,
                                           crust_temperature_model_constant, effective_cover_crust_model_basic)
        flowgo_flux_forced_convection_heat.read_initial_condition_from_json_file(filename)
        characteristic_surface_temperature = flowgo_flux_forced_convection_heat.compute_characteristic_surface_temperature(state,terrain_condition)

        self.assertAlmostEqual(characteristic_surface_temperature, 788.07144823895, 8)

    def test_compute_flux(self):
        filename = './resources/input_parameters_forced_convection_heat_flux.json'

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)

        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1387.13335767292)
        state.set_crystal_fraction(0.104)
        state.set_current_position(10)

        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)

        relative_viscosity_model_er = pyflowgo.flowgo_relative_viscosity_model_er.FlowGoRelativeViscosityModelER()
        relative_viscosity_model_er.read_initial_condition_from_json_file(filename)

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        yield_strength_model_basic = pyflowgo.flowgo_yield_strength_model_basic.FlowGoYieldStrengthModelBasic()
        yield_strength_model_basic.read_initial_condition_from_json_file(filename)

        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(melt_viscosity_model=melt_viscosity_model_vft,
                                                                         relative_viscosity_model=relative_viscosity_model_er,
                                                                         yield_strength_model=yield_strength_model_basic,
                                                                         vesicle_fraction_model=vesicle_fraction_model_constant)
        material_lava.read_initial_condition_from_json_file(filename)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)

        flowgo_flux_forced_convection_heat = pyflowgo.flowgo_flux_forced_convection_heat. \
            FlowGoFluxForcedConvectionHeat(terrain_condition,
                                           material_air, material_lava,
                                           crust_temperature_model_constant, effective_cover_crust_model_basic)
        flowgo_flux_forced_convection_heat.read_initial_condition_from_json_file(filename)

        qforcedconv = flowgo_flux_forced_convection_heat.compute_flux(state,
                                                                      channel_depth=terrain_condition.get_channel_depth(10),
                                                                      channel_width=6.208618418034)

        self.assertAlmostEqual(qforcedconv, 26818.6520246127,6)

        #TODO: to pass the tests you need to comment the running_mean function in pyflowgo/flowgo_terrain_condition.py
                            #slope = self.running_mean(slope, 10)


if __name__ == '__main__':
    unittest.main()
