import os
import os.path
import sys
import fileinput
import math
import matplotlib.pyplot as plt
import numpy as np
import csv

def run_downflow(parameter_file_downflow, path):
    # Run DOWNFLOW
    os.system(path + '/DOWNFLOW/src/DOWNFLOW ' + parameter_file_downflow)
def get_downflow_probabilities(lat, long, dem, path, parameter_file_downflow):
    """    # Run DOWNFLOW and create a raster file 'sim.asc' with the probability of trajectories for a given dem (dem)
    and a given parameter file"""

    with open(parameter_file_downflow) as f:
        l = list(f)
    with open(parameter_file_downflow, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM '+dem+'\n')
            elif line.startswith('Xorigine'):
                output.write('Xorigine ' + lat + '\n')
            elif line.startswith('Yorigine'):
                output.write('Yorigine ' + long + '\n')
            elif line.startswith('New_h_grid_name'):
                output.write('#New_h_grid_name ' + '\n')
            elif line.startswith('write_profile'):
                output.write('#write_profile ' + '\n')
            elif line.startswith('#output_L_grid_name '):
                output.write('output_L_grid_name sim.asc' + '\n')
            else:
                output.write(line)
    # Run DOWNFLOW
    os.system(path + '/DOWNFLOW/src/DOWNFLOW ' + parameter_file_downflow)

def get_downflow_filled_dem(lat, long, dem, path, parameter_file_downflow):

    """ Execute DOWNFLOW and create a new DEM where the pit are filled with a thin layer of 1 mm"""

    n_path = "1000"
    DH= "0.001"

    with open(parameter_file_downflow) as f:
        l = list(f)
    with open(parameter_file_downflow, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM '+dem+'\n')
            elif line.startswith('Xorigine'):
                output.write('Xorigine ' + lat + '\n')
            elif line.startswith('Yorigine'):
                output.write('Yorigine ' + long + '\n')
            elif line.startswith('DH'):
                output.write('DH ' + DH + '\n')
            elif line.startswith('n_path'):
                output.write('n_path ' + n_path +'\n')
            elif line.startswith('output_L_grid_name '):
                output.write('#output_L_grid_name  sim.asc' + '\n')
            elif line.startswith('#New_h_grid_name'):
                output.write('New_h_grid_name  dem_filled_DH0.001_N1000.asc' + '\n')
            elif line.startswith('write_profile'):
                output.write('#write_profile' + '\n')
            else:
                output.write(line)
    # Run DOWNFLOW
    os.system(path + '/DOWNFLOW/src/DOWNFLOW ' + parameter_file_downflow)

def get_downflow_losd(lat, long, filled_dem, path,parameter_file_downflow):
    """ Execute DOWNFLOW and create the profile.txt """
    n_path = "1"
    DH= "0.001"

    with open(parameter_file_downflow) as f:
        l = list(f)
    with open(parameter_file_downflow, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM '+filled_dem+'\n')
            elif line.startswith('Xorigine'):
                output.write('Xorigine ' + lat + '\n')
            elif line.startswith('Yorigine'):
                output.write('Yorigine ' + long + '\n')
            elif line.startswith('DH'):
                output.write('DH ' + DH + '\n')
            elif line.startswith('n_path'):
                output.write('n_path ' + n_path +'\n')
            elif line.startswith('output_L_grid_name '):
                output.write('#output_L_grid_name  sim.asc' + '\n')
            elif line.startswith('New_h_grid_name'):
                output.write('#New_h_grid_name  dem_filled_DH0.001_N1000.asc' + '\n')
            elif line.startswith('#write_profile'):
                output.write('write_profile 10' + '\n')
            else:
                output.write(line)
    # Run DOWNFLOW
    os.system(path + '/DOWNFLOW/src/DOWNFLOW ' + parameter_file_downflow)
