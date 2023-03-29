import csv
import os
import math
import matplotlib.pyplot as plt
import downflow2
import run_flowgo_effusion_rate_array
import pandas as pd
import os
#import geopandas as gpd
from shapely.geometry import Point  # convert to 3D GeoPandas GeoDataFrame

if __name__ == "__main__":

    #  ------------------------------------------------ RUN DOWNFLOW  -------------------------------------------------

    # TODO : choose the path
    path = os.path.abspath('')
    path_to_results = "/Users/chevrel/GoogleDrive/Eruption_PdF/exercice_EMZ"
    #path_to_results = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_exercice_EMZ"
    #path_to_results = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_090421"
    #path_to_results = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_221221"
    #path_to_results ="/Users/chevrel/GoogleDrive/Eruption_PdF/280418/test_nico"
    #path_to_results = "/Users/chevrel/Documents/iceland-simu"
    #path_to_results = "/Users/chevrel/Documents/VIRUNGA/Nyiragongo/downflowgo_simu/scenarios"
    # TODO : choose the DEM
    #dem = path + '/DEM/Clip_DEM_update_oct2010_aug2015_nosea.asc'
    #dem_name = '_2010modified'
    #dem = path + '/DEM/clip_MNT_ENCLOS_2017_5m.asc'
    #dem_name = '_2017_5m_TL'
    #dem = path + '/DEM/MNT-10m-post20200210.asc'
    #dem_name = '_2020'
    #dem = path + '/DEM/Clip_MNT-5m-post20200210-coulee0421.asc'
    #dem_name = '_post20200210-coulee0421'
    #dem = path + '/DEM/MNT-post-20220919_5m.asc'
    #dem_name = '_MNT-post-20220919'

    #dem = path + '/DEM/MNT-PRE-20220919-5m.asc'
    #dem_name = '_MNT_pre_20220919-test'

    #dem = path + '/DEM/Clip_plaine-palmistes_Lidar_2010_5m_complete.asc'
    #dem_name = '_2010'

    dem = path + '/DEM/Clip_Pdf_NE_Lidar2010_5m_complete.asc'
    dem_name = '_2010NE_testdownflow2_proba'
    #dem = path + '/DEM/dem_complete_fournaise_5m_SE.asc'
    #dem_name = '_2010SE'
    #dem = path + '/DEM/reunion_25m.asc'
    #dem_name = '_1997_BB_test'

    #dem = "/Users/chevrel/Documents/iceland-simu/DEM-5m-all.asc"
    #dem_name ='_dem5m'
    #dem ="/Users/chevrel/Documents/VIRUNGA/Nyiragongo/Tandem_X_DEM_10m.asc"
    #dem_name ='_Tandem_'
    #dem ="/Users/chevrel/Documents/VIRUNGA/Nyiragongo/alos_clip_utm.asc"
    #dem_name ='_alos_'
    #dem = path+'/DEM/Clip_enclos_Lidar_2010_5m_complete.asc'
    #dem_name = '_DEM_2010'
    #dem = path + '/DEM/mask_dem2016-corr.asc'
    #dem_name = '_2016-test'
    #dem = path + '/DEM/Clip_Pdf-Est_Lidar_2010_5m_complete.asc'
    #dem_name = '_2010-smooth5'
    #dem = path + '/DEM/Clip_Pdf-Est_Lidar_2010_5m_complete.asc'
    #dem_name = '_2020'

    # TODO : choose the name of the lava flow (flow_id) and the X, Y coordinates
    #csv_vent_file = '/Users/chevrel/GoogleDrive/Eruption_PdF/exercice_EMZ/fissure_exercice_EMZ.csv'
    #csv_vent_file = '/Users/chevrel/Documents/VIRUNGA/Nyiragongo/downflowgo_simu/new_fissure_hypo.csv'
    #csv_vent_file = '/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_090421/vent-position-110421.csv'
    #csv_vent_file = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_251019/vent_251019_thomas.csv"
    csv_vent_file ="/Users/chevrel/GoogleDrive/Eruption_PdF/exercice_EMZ/vent_approx_BB.csv"
    #csv_vent_file = "/Users/chevrel/Documents/iceland-simu/Newfissure-050421.csv"
    # TODO : choose the lava input parameter file for FLOWGO
    #template_json_file = "/Users/chevrel/Documents/VIRUNGA/Nyiragongo/Nyiragongo_template.json"
    template_json_file = "/Users/chevrel/GoogleDrive/Eruption_PdF/PdF_template.json"
    #template_json_file = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_221221/PdF_280418.json"

    run_outs_file_array = []

    with open(csv_vent_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')

        for row in csvreader:

            flow_id = str(row['flow_id'])
            lat = str(row['X'])
            long = str(row['Y'])
            # Run DOWNFLOW
            name_folder = path_to_results +'/' + flow_id + dem_name
            #os.mkdir(name_folder)
            os.chdir(name_folder)
            #downflow.get_one_downflow_profile(lat, long, dem, path)
            #downflow.get_downflow_profile(lat, long, dem, path)

            #downflow2.get_downflow_probabilities(lat, long, dem, path)
            #downflow2.get_downflow_filled_dem(lat, long, dem, path)
            downflow2.get_downflow_losd(lat, long, path)
            print('*********************************  FLOW ID =', flow_id)

            # Run FLOWGO

            simulation = run_flowgo_effusion_rate_array.StartFlowgo()

            path_to_folder = name_folder + '/'
            print(path_to_folder)
            slope_file = path_to_folder + "profile_00000.txt"

            json_file_new = path_to_folder + 'parameters_' + flow_id + ".json"

            simulation.make_new_json(template_json_file, flow_id, slope_file, json_file_new)

            simulation.run_flowgo_effusion_rate_array(json_file_new, path_to_folder, slope_file)

    print("************************************** THE END *************************************")
