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
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_effective_cover_crust_model_basic


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_effective_cover_crust_basic.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava()
        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)

        self.assertEqual(effective_cover_crust_model_basic._alpha, -7.56e-3)
        self.assertEqual(effective_cover_crust_model_basic._crust_cover_fraction, 1.0)

    def test_compute_effective_cover_fraction(self):
        filename = './resources/input_parameters_effective_cover_crust_basic.json'
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
        # TODO: to pass the tests you need to comment the running_mean function in pyflowgo/flowgo_terrain_condition.py
        # slope = self.running_mean(slope, 10)

        effective_cover_crust_model_basic = pyflowgo.flowgo_effective_cover_crust_model_basic.FlowGoEffectiveCoverCrustModelBasic(
            terrain_condition, material_lava)
        effective_cover_crust_model_basic.read_initial_condition_from_json_file(filename)

        effective_cover_fraction = effective_cover_crust_model_basic.compute_effective_cover_fraction(state)

        self.assertAlmostEqual(effective_cover_fraction, 0.968487820088,10)


if __name__ == '__main__':
    unittest.main()
