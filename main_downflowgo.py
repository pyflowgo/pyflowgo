import csv
import os
import math
import matplotlib.pyplot as plt
import downflow
import downflow2
import downflowcpp
import run_flowgo_effusion_rate_array
import os
import fiona
import pandas as pd
import txt_to_shape
import shutil

if __name__ == "__main__":

    #  ------------------------------------------------ RUN DOWNFLOW  -------------------------------------------------

# ------------>   choose the path to the working folder   <------------
    path = os.path.abspath('')
    #path_to_results = "/Users/chevrel/GoogleDrive/Eruption_PdF/exercice_EMZ"
    #path_to_results = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_exercice_EMZ"
    #path_to_results = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_090421"
    #path_to_results = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_221221"

    path_to_results ="/Users/chevrel/GoogleDrive/Eruption_PdF/030523"
    #path_to_results = "/Users/chevrel/Documents/iceland-simu"
    #path_to_results = "/Users/chevrel/Documents/VIRUNGA/Nyiragongo/downflowgo_simu/scenarios"

# ------------>   choose the path to the DEM   <------------

    #dem = path + '/DEM/Clip_Pdf_NE_Lidar2010_5m_complete.asc'
    #dem_name = '_2010NE_testdownflow2'

    dem = path + '/DEM/MNT-post-20220919_5m.asc'
    dem_name = '_MNT2022_test_downflowcpp'

    #dem = path + '/DEM/Clip_DEM_update_oct2010_aug2015_nosea.asc'
    #dem_name = '_2010modified_testdownflowcpp'


    #dem = path + '/DEM/clip_MNT_ENCLOS_2017_5m.asc'
    #dem_name = '_2017_5m_TL'
    #dem = path + '/DEM/MNT-10m-post20200210.asc'
    #dem_name = '_2020'
    #dem = path + '/DEM/Clip_MNT-5m-post20200210-coulee0421.asc'
    #dem_name = '_post20200210-coulee0421'

    #dem = path + '/DEM/MNT-PRE-20220919-5m.asc'
    #dem_name = '_MNT_pre_20220919-test'

    #dem = path + '/DEM/Clip_plaine-palmistes_Lidar_2010_5m_complete.asc'
    #dem_name = '_2010'    #dem = path + '/DEM/dem_complete_fournaise_5m_SE.asc'
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

# ------------>   choose the name of the lava flow (flow_id) and the X, Y coordinates <------------

    #csv_vent_file = '/Users/chevrel/GoogleDrive/Eruption_PdF/exercice_EMZ/fissure_exercice_EMZ.csv'
    #csv_vent_file = '/Users/chevrel/Documents/VIRUNGA/Nyiragongo/downflowgo_simu/new_fissure_hypo.csv'
    #csv_vent_file = '/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_090421/vent-position-110421.csv'
    csv_vent_file = "/Users/chevrel/GoogleDrive/Eruption_PdF/vent_hypothetic.csv"
    #csv_vent_file ="/Users/chevrel/GoogleDrive/Eruption_PdF/exercice_EMZ/vent_approx_BB.csv"
    #csv_vent_file = "/Users/chevrel/Documents/iceland-simu/Newfissure-050421.csv"

# ----->>  TODO : choose json file for FLOWGO <------------

    #template_json_file = "/Users/chevrel/Documents/VIRUNGA/Nyiragongo/Nyiragongo_template.json"
    template_json_file = "/Users/chevrel/GoogleDrive/Eruption_PdF/PdF_template.json"
    #template_json_file = "/Volumes/Macintosh HD/OryaStorage/Eruption_PdF/Pdf_221221/PdF_280418.json"

    run_outs_file_array = []

    # ------------>   choose parameter file and N and Dh for DOWNFLOW  <------------

    parameter_file_downflow = path + '/DOWNFLOW/parameters_range.txt'
    #parameter_file_downflow = path + '/prova_DOWNFLOW/parameters_DOWNFLOW.txt'
    n_path = '10000'
    DH = '2'

    with open(parameter_file_downflow) as f:
        l = list(f)
    with open(parameter_file_downflow, 'w') as output:
        for line in l:
            if line.startswith('DH'):
                output.write('DH ' + DH + '\n')
            elif line.startswith('n_path'):
                output.write('n_path ' + n_path + '\n')
            else:
                output.write(line)

    with open(csv_vent_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')

        for row in csvreader:

            flow_id = str(row["flow_id"])
            lat = str(row['X'])
            long = str(row['Y'])

            # Run DOWNFLOW /home/ingv/prog/DOWNFLOW/src/DOWNFLOW parameters_range.txt

            name_folder = path_to_results + '/' + flow_id + dem_name
            path_to_folder = name_folder + '/'
            os.mkdir(name_folder)
            os.chdir(name_folder)

         #downflow.get_downflow_profile(lat, long, dem, path)

        #    downflowcpp.run_downflow(parameter_file_downflow, path)

            # this returns an asc file with the lava flow path probabilities
            #downflow2.get_downflow_probabilities(lat, long, dem, path, parameter_file_downflow)
            downflowcpp.get_downflow_probabilities(lat, long, dem, path, parameter_file_downflow)

            print("******************* DOWNFLOW probability executed: sim.asc created **************************")

            #downflow2.get_downflow_filled_dem(lat, long, dem, path)  # this returns an asc file with new DEM
            downflowcpp.get_downflow_filled_dem(lat, long, dem, path, parameter_file_downflow)  # this returns an asc file with new (filled) DEM
            print("************************ DOWNFLOW filled DEM done *********")
            #downflow2.get_downflow_losd(lat, long, path)  # this returns a shp file with the losd and the profile.txt

            filled_dem = 'dem_filled_DH0.001_N1000.asc'
            downflowcpp.get_downflow_losd(lat, long, filled_dem, path, parameter_file_downflow)  # this returns the profile.txt
            os.remove(path_to_folder + "/dem_filled_DH0.001_N1000.asc")
            map = path_to_folder + 'map'
            os.mkdir(map)
            shutil.move(path_to_folder+'sim.asc', map + '/sim_' + flow_id+'.asc')

            print("**************** DOWNFLOW slope profile executed for FLOW ID =", flow_id, '*********')

            print("************************ Start FLOWGO for FLOW ID =", flow_id, '*********')
            # Run FLOWGO
            simulation = run_flowgo_effusion_rate_array.StartFlowgo()
            slope_file = path_to_folder + "profile_00000.txt"
            json_file_new = path_to_folder + 'parameters_' + flow_id + ".json"
            simulation.make_new_json(template_json_file, flow_id, slope_file, json_file_new)
            simulation.run_flowgo_effusion_rate_array(json_file_new, path_to_folder, slope_file)
            print('*********** FLOWGO executed and results stored in:', path_to_folder, '***********')

            # convert profile to shape line
            txt_to_shape.get_path_shp(slope_file, path_to_folder, flow_id)
            print('*********** shape file is saved in:', map, '/path_'+flow_id+'.shp', '***********')

            # convert profile to shape line
            run_outs = path_to_folder + 'run_outs_'+flow_id+'.csv'
            txt_to_shape.get_runouts_shp(run_outs, path_to_folder, flow_id)
            print('*********** run outs file is saved in:', map, '/run_outs_'+flow_id+'.shp', '***********')

    print("************************************** THE END *************************************")
