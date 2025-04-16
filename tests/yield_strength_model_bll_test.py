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
import sys
import os
# Ajoute le dossier parent du script (main) au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pyflowgo.flowgo_yield_strength_model_ryerson
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_yield_strength_model_bll

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename ='./resources/input_parameters_bll.json'

        yield_strength_model_bll = pyflowgo.flowgo_yield_strength_model_bll.FlowGoYieldStrengthModelBLL()
        yield_strength_model_bll.read_initial_condition_from_json_file(filename)
        self.assertEqual(yield_strength_model_bll._eruption_temperature, 1223.15)
        print("read json valid")

    def test_compute_yield_strength(self):
        filename = './resources/input_parameters_bll.json'

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        yield_strength_model_bll = pyflowgo.flowgo_yield_strength_model_bll. \
            FlowGoYieldStrengthModelBLL(vesicle_fraction_model=vesicle_fraction_model_constant)

        yield_strength_model_bll.read_initial_condition_from_json_file(filename)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.15)
        yield_strength = yield_strength_model_bll.compute_yield_strength(state, eruption_temperature=None)
        vesicle_fraction = vesicle_fraction_model_constant.computes_vesicle_fraction(state)
        self.assertEqual(vesicle_fraction, 0.64)
        print("vesicle_fraction valid")
        self.assertAlmostEqual(yield_strength, 7.433613897,8)
        print("yield_strength valid")
        #TODO: to pass the tests you need to comment the running_mean function in pyflowgo/flowgo_terrain_condition.py
                            #slope = self.running_mean(slope, 10)


    def test_compute_basal_shear_stress(self):

        yield_strength_model_basic = pyflowgo.flowgo_yield_strength_model_basic.FlowGoYieldStrengthModelBasic()

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
        basal_shear_stress = yield_strength_model_basic.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)
        state.set_current_position(0)
        self.assertAlmostEqual(basal_shear_stress, 4735.3382991549,10)
        print("basal_shear_stress valid")


        state.set_current_position(30)
        basal_shear_stress = yield_strength_model_basic.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)

        self.assertAlmostEqual(basal_shear_stress, 4693.68722398169,10)

        state.set_current_position(1010)
        basal_shear_stress = yield_strength_model_basic.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)

        self.assertAlmostEqual(basal_shear_stress, 2178.2894789708,10)

        #TODO: to pass the tests you need to comment the running_mean function in pyflowgo/flowgo_terrain_condition.py
                            #slope = self.running_mean(slope, 10)

if __name__ == '__main__':
    unittest.main()

