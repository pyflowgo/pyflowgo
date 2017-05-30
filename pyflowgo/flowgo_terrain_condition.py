import math
import json

from scipy import interpolate


class FlowGoTerrainCondition:
   #default values that are erased as soon as the slope_file is read
    _channel_depth = 5.5
    _channel_width = 5.5
    _gravity = 9.81
    _default_slope = math.radians(2.657414)
    _slope_spline = None
    _max_channel_length = -1

    def read_initial_condition_from_json_file(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            self._channel_depth = float(data['terrain_conditions']['depth'])
            self._channel_width = float(data['terrain_conditions']['width'])
            self._gravity = float(data['terrain_conditions']['gravity'])
            self._max_channel_length = float(data['terrain_conditions']['max_channel_length'])

    def read_slope_from_file(self, filename=None):
        if filename == None:
            filename = '../MaunaUlu74/DEM_maunaulu74.txt'

        distance = []
        slope = []
        # here read the slope file (.txt) where each line represent the distance from the vent (first column) and
        # the corresponding slope in degree (second column) that is then converted in gradiant
        f_slope = open(filename, "r")
        f_slope.readline()
        for line in f_slope:
            split_line = line.strip('\n').split('\t')
            distance.append(float(split_line[0]))
            slope.append(math.radians(float(split_line[1])))
        f_slope.close()

        #slope = self.running_mean(slope, 50)

        # build the spline to interpolate the distance (k=1 : it is a linear interpolation)
        self._slope_spline = interpolate.InterpolatedUnivariateSpline(distance, slope, k=1.)

    def get_channel_slope(self, position_x):
        if (self._slope_spline is not None):
            return self._slope_spline(position_x)
        else:
            return self._default_slope

    def get_channel_depth(self, current_x):
        return self._channel_depth

    def get_channel_width(self, current_x):
        return self._channel_width

    def get_gravity(self, current_x):
        return self._gravity

    def get_max_channel_length(self):
        return self._max_channel_length
    #
    # def running_mean(self, l, N):
    #     sum = 0
    #     result = list( 0 for x in l)
    #
    #     for i in range (0, N):
    #         sum = sum+l[i]
    #         result[i] =sum/ (i+1)
    #
    #     for i in range (0, len(l)):
    #         sum = sum - l[i-N]+ l[i]
    #         result[i] =sum/N
    #
    #     return result
