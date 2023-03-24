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
import pyflowgo.flowgo_flux_radiation_heat_lin_emi
import pyflowgo.flowgo_crust_temperature_model_constant
import pyflowgo.flowgo_effective_cover_crust_model_basic

class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_radiation_flux.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava()
        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(terrain_condition, material_lava)

        flowgo_flux_radiation_heat = pyflowgo.flowgo_flux_radiation_heat_lin_emi.FlowGoFluxRadiationHeat(terrain_condition,material_lava, material_air, crust_temperature_model_constant,effective_cover_crust_model_basic)
        flowgo_flux_radiation_heat.read_initial_condition_from_json_file(filename)

        self.assertEqual(flowgo_flux_radiation_heat._sigma, 5.67e-8)

    def test_compute_effective_radiation_temperature(self):
        filename = './resources/input_parameters_radiation_flux.json'
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
        molten_material_temperature = material_lava.computes_molten_material_temperature(state)
        print("molten_material_temperature=", molten_material_temperature)

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        air_temperature = material_air.get_temperature()
        print("air_temperature=", air_temperature)

        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)
        effective_cover_crust=effective_cover_crust_model_basic.compute_effective_cover_fraction(state)
        print("effective_cover_crust=",effective_cover_crust)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)
        crust_temperature = crust_temperature_model_constant.compute_crust_temperature(state)
        print("crust_temperature=", crust_temperature)

        flowgo_flux_radiation_heat = pyflowgo.flowgo_flux_radiation_heat_lin_emi.FlowGoFluxRadiationHeat(terrain_condition,
                                                                                                 material_lava,
                                                                                                 material_air,
                                                                                                 crust_temperature_model_constant,
                                                                                                 effective_cover_crust_model_basic)
        flowgo_flux_radiation_heat.read_initial_condition_from_json_file(filename)

        effective_radiation_temperature = flowgo_flux_radiation_heat._compute_effective_radiation_temperature(state, terrain_condition)
        # if T air not considered :
        # self.assertAlmostEqual(effective_radiation_temperature,806.125082231417,5)

        # if T air considered :
        self.assertAlmostEqual(effective_radiation_temperature, 802.577271980509, 5)

    def test_compute_epsilon_effective(self):
        filename = './resources/input_parameters_radiation_flux.json'
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
        molten_material_temperature = material_lava.computes_molten_material_temperature(state)
        print("molten_material_temperature=", molten_material_temperature)

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        air_temperature = material_air.get_temperature()
        print("air_temperature=", air_temperature)

        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)
        effective_cover_crust=effective_cover_crust_model_basic.compute_effective_cover_fraction(state)
        print("effective_cover_crust=",effective_cover_crust)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)
        crust_temperature = crust_temperature_model_constant.compute_crust_temperature(state)
        print("crust_temperature=", crust_temperature)


        flowgo_flux_radiation_heat= pyflowgo.flowgo_flux_radiation_heat_lin_emi.FlowGoFluxRadiationHeat(terrain_condition,
                                                                                                 material_lava,
                                                                                                 material_air,
                                                                                                 crust_temperature_model_constant,
                                                                                                 effective_cover_crust_model_basic)
        flowgo_flux_radiation_heat.read_initial_condition_from_json_file(filename)

        effective_epsilon = flowgo_flux_radiation_heat._compute_epsilon_effective(state, terrain_condition)
        self.assertAlmostEqual(effective_epsilon,0.927404392619719,10)

    def test_get_emissivity(self):
        filename = './resources/input_parameters_radiation_flux.json'
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
        molten_material_temperature = material_lava.computes_molten_material_temperature(state)
        print("molten_material_temperature=", molten_material_temperature)

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        air_temperature = material_air.get_temperature()
        print("air_temperature=", air_temperature)

        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)
        effective_cover_crust=effective_cover_crust_model_basic.compute_effective_cover_fraction(state)
        print("effective_cover_crust=",effective_cover_crust)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)
        crust_temperature = crust_temperature_model_constant.compute_crust_temperature(state)
        print("crust_temperature=", crust_temperature)


        flowgo_flux_radiation_heat= pyflowgo.flowgo_flux_radiation_heat_lin_emi.FlowGoFluxRadiationHeat(terrain_condition,
                                                                                                 material_lava,
                                                                                                 material_air,
                                                                                                 crust_temperature_model_constant,
                                                                                                 effective_cover_crust_model_basic)
        flowgo_flux_radiation_heat.read_initial_condition_from_json_file(filename)

        emissivity_crust = flowgo_flux_radiation_heat._compute_emissivity_crust(state, terrain_condition)
        self.assertAlmostEqual(emissivity_crust,0.9317638664,10)
        emissivity_molten = flowgo_flux_radiation_heat._compute_emissivity_molten(state, terrain_condition)
        self.assertAlmostEqual(emissivity_molten, 0.861546075860903, 10)

    def test_compute_spectral_radiance(self):
        filename = './resources/input_parameters_radiation_flux.json'
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



        molten_material_temperature = material_lava.computes_molten_material_temperature(state)
        print("molten_material_temperature=", molten_material_temperature)

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        air_temperature = material_air.get_temperature()
        print("air_temperature=", air_temperature)

        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)
        effective_cover_crust=effective_cover_crust_model_basic.compute_effective_cover_fraction(state)
        print("effective_cover_crust=",effective_cover_crust)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)
        crust_temperature = crust_temperature_model_constant.compute_crust_temperature(state)
        print("crust_temperature=", crust_temperature)

        flowgo_flux_radiation_heat = pyflowgo.flowgo_flux_radiation_heat_lin_emi.FlowGoFluxRadiationHeat(terrain_condition,
                                                                                                 material_lava,
                                                                                                 material_air,
                                                                                                 crust_temperature_model_constant,
                                                                                                 effective_cover_crust_model_basic)
        flowgo_flux_radiation_heat.read_initial_condition_from_json_file(filename)


        spectral_radiance = flowgo_flux_radiation_heat._compute_spectral_radiance(state, terrain_condition, channel_width=6.20861841618025)
        print("spectral_radiance=", spectral_radiance)
        self.assertAlmostEqual(spectral_radiance,1729.10711808488,5)

    def test_compute_flux(self):
        filename = './resources/input_parameters_radiation_flux.json'
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
        molten_material_temperature = material_lava.computes_molten_material_temperature(state)
        print("molten_material_temperature=", molten_material_temperature)

        material_air = pyflowgo.flowgo_material_air.FlowGoMaterialAir()
        material_air.read_initial_condition_from_json_file(filename)
        air_temperature = material_air.get_temperature()
        print("air_temperature=", air_temperature)

        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)
        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)
        effective_cover_crust=effective_cover_crust_model_basic.compute_effective_cover_fraction(state)
        print("effective_cover_crust=",effective_cover_crust)

        crust_temperature_model_constant = pyflowgo.flowgo_crust_temperature_model_constant.FlowGoCrustTemperatureModelConstant()
        crust_temperature_model_constant.read_initial_condition_from_json_file(filename)
        crust_temperature = crust_temperature_model_constant.compute_crust_temperature(state)
        print("crust_temperature=", crust_temperature)

        flowgo_flux_radiation_heat = pyflowgo.flowgo_flux_radiation_heat_lin_emi.FlowGoFluxRadiationHeat(terrain_condition,
                                                                                                 material_lava,
                                                                                                 material_air,
                                                                                                 crust_temperature_model_constant,
                                                                                                 effective_cover_crust_model_basic)
        flowgo_flux_radiation_heat.read_initial_condition_from_json_file(filename)

        effective_radiation_temperature = flowgo_flux_radiation_heat._compute_effective_radiation_temperature(state, terrain_condition)
        print("effective_radiation_temperature", effective_radiation_temperature)

        qradiation = flowgo_flux_radiation_heat.compute_flux(state, channel_depth=1.4,
                                                                      channel_width=6.20861841803369)

        # if T air not considered :
        #self.assertAlmostEqual(qradiation, 141224.930628606, 4)
        # if T air not considered :
        self.assertAlmostEqual(qradiation, 135454.863787622, 4)

if __name__ == '__main__':
    unittest.main()
