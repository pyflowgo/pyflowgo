import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_flux_viscous_heating



class MyTestCase(unittest.TestCase):

    def test_compute_flux(self):

        filename = './resources/input_parameters_material_lava.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)


        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1322.70208376477)
        state.set_crystal_fraction(0.4888694761447)
        state.set_current_position(3710)
        #TODO:where do I get the width ?
        channel_width = 4734.06367207989
        channel_depth = terrain_condition.get_channel_depth(3710)

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

        flowgo_flux_viscous_heating = pyflowgo.flowgo_flux_viscous_heating.FlowGoFluxViscousHeating(terrain_condition,
                                                                                                    material_lava)
        flowgo_flux_viscous_heating.read_initial_condition_from_json_file(filename)

        qviscous=flowgo_flux_viscous_heating.compute_flux(state,channel_width, channel_depth)

        self.assertAlmostEqual(qviscous, 2090.0103751966,5)


if __name__ == '__main__':
    unittest.main()
