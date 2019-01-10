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
import pyflowgo.flowgo_yield_strength_model_dragoni
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_vesicle_fraction_model_constant

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_yield_strength_model.json'

        yield_strength_model_dragoni = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()
        yield_strength_model_dragoni.read_initial_condition_from_json_file(filename)

        self.assertEqual(yield_strength_model_dragoni._liquidus_temperature, 1400)

    def test_compute_yield_strength(self):
        filename = './resources/input_parameters_yield_strength_model.json'
        yield_strength_model_dragoni = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()
        yield_strength_model_dragoni.read_initial_condition_from_json_file(filename)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1387.15)
        state.set_crystal_fraction(0.104)
        yield_strength = yield_strength_model_dragoni.compute_yield_strength(state,eruption_temperature=1387.15)

        self.assertAlmostEqual(yield_strength, 10.2776341191,10)

    def test_compute_basal_shear_stress(self):

        yield_strength_model_dragoni = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()

        filename_1 = './resources/input_parameters_yield_strength_model.json'
        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename_1)
        filename = './resources/input_parameters_yield_strength_model.json'
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(vesicle_fraction_model=vesicle_fraction_model_constant)
        material_lava.read_initial_condition_from_json_file(filename)

        filename = './resources/input_parameters_yield_strength_model.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        state = pyflowgo.flowgo_state.FlowGoState()
        basal_shear_stress = yield_strength_model_dragoni.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)
        state.set_current_position(0)
        self.assertAlmostEqual(basal_shear_stress, 4735.3382991549,10)

        state.set_current_position(30)
        basal_shear_stress = yield_strength_model_dragoni.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)

        self.assertAlmostEqual(basal_shear_stress, 4693.68722398169,10)

        state.set_current_position(1010)
        basal_shear_stress = yield_strength_model_dragoni.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)

        self.assertAlmostEqual(basal_shear_stress, 2178.2894789708,10)


        #TODO: to pass the tests you need to comment the running_mean function in pyflowgo/flowgo_terrain_condition.py
                            #slope = self.running_mean(slope, 10)


if __name__ == '__main__':
    unittest.main()

