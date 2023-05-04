import os
import os.path
import sys
import fileinput
import math
import matplotlib.pyplot as plt
import numpy as np
import csv


def get_downflow_probabilities(lat, long, dem, path, parameter_file_downflow):
    """    # Execute DOWNFLOW and create a raster file 'sim.asc' with the probability of trajectories for a given dem (dem)
    Change n_path and DH for the given volcano  = 2 for Piton / 0.4 (Nyiragongo)"""

    space = ' '

    with open(parameter_file_downflow) as f:
        l = list(f)
    with open(parameter_file_downflow, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM '+dem+'\n')
            elif line.startswith('attiva_output_grid_L'):
                output.write('attiva_output_grid_L ' + '1' + '\n')
            elif line.startswith('attiva_w_grid_new_h'):
                output.write('attiva_w_grid_new_h ' + '0' + '\n')
            elif line.startswith('Xorigine'):
                output.write('Xorigine ' + lat + '\n')
            elif line.startswith('Yorigine'):
                output.write('Yorigine ' + long + '\n')
            else:
                output.write(line)

    # path to executive downflow
    dem2 = path + '/prova_DOWNFLOW/dem2 -DOWNFLOW '
    os.system(dem2 + parameter_file_downflow + ' -write_shp_path_debug -input_point ' + lat + space + long)


def get_downflow_filled_dem(lat, long, dem, path):

    """ Execute DOWNFLOW and create a new DEM where the pit are filled with a thin layer of 1 mm"""

    n_path = "1000"
    DH= "0.001"
    lat = lat
    space = ' '
    long = long
    dem = dem
    path = path

    # path to executive downflow
    dem2 = path + '/prova_DOWNFLOW/dem2 -DOWNFLOW '

    # Parameters files to run DOWNFLOW
    parameters = path + '/prova_DOWNFLOW/parameters_DOWNFLOW.txt'
    with open(parameters) as f:
        l = list(f)

    with open(parameters, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM '+dem+'\n')
            elif line.startswith('n_path'):
                output.write('n_path '+n_path+'\n')
            elif line.startswith('DH'):
                output.write('DH '+DH+'\n')
            elif line.startswith('Xorigine'):
                output.write('Xorigine ' + lat + '\n')
            elif line.startswith('Yorigine'):
                output.write('Yorigine ' + long + '\n')
            elif line.startswith('attiva_output_grid_L'):
                output.write('attiva_output_grid_L ' + '0' + '\n')
            elif line.startswith('attiva_w_grid_new_h'):
                output.write('attiva_w_grid_new_h ' + '1' + '\n')
            else:
                output.write(line)

    DOWNFLOW_DH0_001_N1000 = dem2+parameters+' -write_shp_path_debug -input_point '+lat+space+long
    os.system(DOWNFLOW_DH0_001_N1000)
    # paths to filled dem


def get_downflow_losd(lat, long, path):
    """ Execute DOWNFLOW and create the shape file of the Line of Steepest descent (called path_dem_filed) """
    n_path = "1"
    DH = "0.001"
    lat = lat
    space = ' '
    long = long
    path = path

    # path to executive downflow
    dem2 = path + '/prova_DOWNFLOW/dem2 -DOWNFLOW '

    # Parameters files to run DOWNFLOW
    parameters = path + '/prova_DOWNFLOW/parameters_DOWNFLOW.txt'
    dem_filled = ' dem_filled_DH0.001_N1000.asc '
    with open(parameters) as f:
        l = list(f)
    with open(parameters, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM '+dem_filled+'\n')
            elif line.startswith('n_path'):
                output.write('n_path '+n_path+'\n')
            elif line.startswith('DH'):
                output.write('DH '+DH+'\n')
            elif line.startswith('Xorigine'):
                output.write('Xorigine ' + lat + '\n')
            elif line.startswith('Yorigine'):
                output.write('Yorigine ' + long + '\n')
            elif line.startswith('attiva_output_grid_L'):
                output.write('attiva_output_grid_L ' + '0' + '\n')
            elif line.startswith('attiva_w_grid_new_h'):
                output.write('attiva_w_grid_new_h ' + '0' + '\n')

            else:
                output.write(line)

    DOWNFLOW_DH0_001_N1 = dem2+parameters+' -write_shp_path_debug -input_point '+lat+space+long
    os.system(DOWNFLOW_DH0_001_N1)
    path_shp = ' path.shp '
    path_dem_filled = 'path_dem_filled.shp'

    #Execute DOWNFLOW to convert the shape file of the main LoSD into a txt file "profile_00000.txt" containing a point every 10m:
    poliline = path +'/prova_DOWNFLOW/dem2 -VEC_GRD_shp_polilinee_to_3d_shape '
    profile_losd = poliline+path_shp+dem_filled+' 10 '+path_dem_filled
    os.system(profile_losd)

def get_one_downflow_profile(lat,long,dem, path):
    lat = lat
    space = ' '
    long = long
    dem = dem
    path = path

    # Parameters files to run DOWNFLOW
    # This will find the main LoSD with DH=0.001

    parameters_DH0_001_N1000 = path + '/prova_DOWNFLOW/parameters_DH0.001_N1000.txt'
    # Look for the steepest line of descent:
    parameters_DH0_001_N1 = path + '/prova_DOWNFLOW/parameters_DH0.001_N1.txt'

    # modify parameters_file_with good DEM

    with open(parameters_DH0_001_N1000) as f:
        l = list(f)

    with open(parameters_DH0_001_N1000, 'w') as output:
        for line in l:
            if line.startswith('input_DEM'):
                output.write('input_DEM ' + dem + '\n')
            else:
                output.write(line)

    # path to executive downflow
    dem2 = path + '/prova_DOWNFLOW/dem2 -DOWNFLOW '

    # Execute DOWNFLOW and create a shapefile 'path.shp' with the steepest descent path, using the pitfilling algorithm of DOWNFLOW itself

    DOWNFLOW_DH0_001_N1000 = dem2 + parameters_DH0_001_N1000 + ' -write_shp_path_debug -input_point ' + lat + space + long
    os.system(DOWNFLOW_DH0_001_N1000)
    # paths to filled dem
    dem_filled = ' dem_filled_DH0.001_N1000.asc '

    DOWNFLOW_DH0_001_N1 = dem2 + parameters_DH0_001_N1 + ' -write_shp_path_debug -input_point ' + lat + space + long
    os.system(DOWNFLOW_DH0_001_N1)

    # Then create the slope file: This will create the text file: "profile_00000.txt" containing the profile data of path2.shp
    path_shp = ' path.shp '
    # file to be created with the new path on the dem filled
    path_dem_filled = ' path_dem_filled.shp'
    poliline = path + '/prova_DOWNFLOW/dem2 -VEC_GRD_shp_polilinee_to_3d_shape '
    profile_losd = poliline + path_shp + dem_filled + ' 10 ' + path_dem_filled
    os.system(profile_losd)

def convert_dem(dem):
    new_dem = dem.strip('.asc')+'.flt'
    # path to executive downflow
    dem2 = '/Users/chevrel/prova_DOWNFLOW/dem2'

    # Execute DOWNFLOW and convert the dem format
    os.system(dem2 + ' -GRD_converti_formato_grid' + dem + new_dem)


def create_hillshade(dem_flt):
    HS_ = dem_flt.strip('.flt') + '.bmp'
    # path to executive downflow
    dem2 = '/Users/chevrel/prova_DOWNFLOW/dem2'
    # Execute DOWNFLOW and convert the dem format
    os.system(dem2 + ' -BMP_GRD_create_hillshaded_from_grid' + dem_flt + HS_ + ' 315 45 0 255')


def clip_grid(folder, dem_flt,clip):
    # path to executive downflow
    dem2 = '/Users/chevrel/prova_DOWNFLOW/dem2'
    blank = folder + 'blank.flt'
    clip_dem_flt = folder + 'clip_dem.flt'
    HS_clip_dem = folder +'HS_clip_dem.bmp'
    # Execute DOWNFLOW and convert the dem format
    SHAPE = folder + 'mask_shp.shp'
    os.system(dem2 + ' -GRD_crea_grid_vuoto_con_dato_extent 5  '+clip+'  ' + blank)
    os.system(dem2 + ' -GRD__RESAMPLE_RESIZE '+ dem_flt + ' ' + blank + ' ' + clip_dem_flt)
    os.system(dem2 + ' -BMP_GRD_create_hillshaded_from_grid '+ clip_dem_flt + ' ' + HS_clip_dem + ' ' + '315 45 0 255')

def convert_lava_flow_to_mask_image(folder):
#Convert lava flow to mask image
# START - convert a shapefile to a grid  ('final' is a field with value 1)
    dem2 = '/Users/chevrel/prova_DOWNFLOW/dem2'
    SHAPE= folder +'lavaflow.shp'
    clip_dem_flt = folder + 'clip_dem.flt'
    mask_raster_out = folder + 'mask_raster_out.flt'
    os.system(dem2 + ' -GRD_2_linear_combination ' + clip_dem_flt + ' +0.0 ' + clip_dem_flt + ' -0.0 -9999 ' + mask_raster_out)
    os.system('gdal_rasterize -a final -l ' + 'lavaflow' + ' ' + SHAPE + ' ' + mask_raster_out)
##END - how to convert a shapefile to a grid
##convert the grid into the image needed (this holds for a value=1 in the field 'final' in the previous conversion)
    os.system(dem2 + ' -GRD_change_value ' + mask_raster_out + ' ' + mask_raster_out + ' -9999 0')
    os.system(dem2 + ' -GRD_change_value ' + mask_raster_out + ' ' + mask_raster_out + ' 1 255')
##create the image mask.bmp, needed in the calibration.
    image_mask_raster_out = folder + 'mask_raster_out.bmp'
    os.system(dem2 + ' -GRD_BMP_bmp_from_grid ' + ' ' + mask_raster_out + ' ' + image_mask_raster_out)

def clip_dem_from_mask(folder):
    #Clip of the DEM with the shapefile mask_shp and create the DEM mask_dem.flt (mask_RASTERin), needed in the calibration and the HS
    dem2 = '/Users/chevrel/prova_DOWNFLOW/dem2'
    SHAPE = folder + 'mask_shp.shp'
    clip_dem_flt = folder + 'clip_dem.flt'
    mask_clip_dem_raster_out = folder + 'mask_clip_dem_raster_out.flt'
    os.system(dem2 + ' -GRD_2_linear_combination ' + clip_dem_flt + ' +0.0 ' + clip_dem_flt + ' -0.0 -9999 ' + mask_clip_dem_raster_out)
    os.system('gdal_rasterize -a id -l ' + 'mask_shp' + ' ' + SHAPE + ' ' + mask_clip_dem_raster_out)
    mask_clip_dem_rather_in = folder + 'mask_clip_dem.flt'
    HS_mask_clip_dem_flt = folder + 'HS_mask_clip_dem_flt.bmp'

    os.system(dem2 + ' -GRD_apply_mask_grid ' + clip_dem_flt + ' ' + mask_clip_dem_raster_out + ' ' + mask_clip_dem_rather_in)
    os.system(dem2 + ' -BMP_GRD_create_hillshaded_from_grid ' + mask_clip_dem_rather_in + ' ' + HS_mask_clip_dem_flt + ' 315 45 0 255')

def compare_images(folder):

    # copy the file  'parameters_range.txt' in the folder
# in 'parameters_range.txt' set the right vent location ("Xorigine 366966.0" and "Yorigine 7647642.0")
# then run
    dem2 = '/Users/chevrel/prova_DOWNFLOW/dem2'
    image_mask_raster_out = folder + 'mask_raster_out.bmp'
    parameters_range = folder + 'parameters_range.txt'
    os.system(dem2 + ' -DOWNFLOW ' + parameters_range + ' ' + '-COMP_IMG' + ' ' + image_mask_raster_out)

# this will take a long time and create the file 'flow_report.txt'. If flow_report.txt already exists, it will just append the output to this file.
# So if you need to re-run the calibration in the same folder, remove/delete the file flow_report.txt. Also you cannot run 2 calibration in the same folder,
# as the calibration will write on the same file file at the same time with undesired effects.
# the most relevant columns in the file 'flow_report.txt' are the first three: dh, N and the fit

def plot_results(folder):
    flow_report = folder +'results/'+ 'flow_report.txt'
    f = open(flow_report, "r")

    data = f.readlines()
    data = data[2:]
    f.close()
    print(max(data), min(data))