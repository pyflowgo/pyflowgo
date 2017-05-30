import unittest
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_state
import math

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_terrain_condition.json'
        terrain_condition= pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)

        self.assertEqual(terrain_condition.get_channel_depth(0), 1.4)
        self.assertEqual(terrain_condition.get_channel_width(0), 4.5)
        self.assertEqual(terrain_condition.get_gravity(0), 9.81)

    def test_read_slope_file(self):
        filename = './resources/input_parameters_terrain_condition.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)

        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(0)
        slope = terrain_condition.get_channel_slope(state.get_current_position())
        self.assertAlmostEqual(slope, 0.328342197625647,15)
        #self.assertAlmostEqual(terrain_condition.get_channel_slope(100),(0.24642041508094412),16)

