import csv
import os
import math
import matplotlib.pyplot as plt
import downflow
import run_flowgo_effusion_rate_array


if __name__ == "__main__":

    #  ------------------------------------------------ RUN DOWNFLOW  -------------------------------------------------
    path = os.path.abspath('')
    # TODO : choose the path

    path_to_results = "wherever/you/want/to/put/your/data"

    # TODO : choose the DEM
    dem = path +'/DEM/CLIP_completed_2010_SE_5pt0_nullSea_32740.asc'

    # TODO : choose the name of the lava flow (flow_id) and the X, Y coordinates
    csv_vent_file = 'wherever is vent_coordinates.csv'

    # TODO : choose the lava input parameter file for FLOWGO
    template_json_file = "wherever is template.json"

    run_outs_file_array = []

    with open(csv_vent_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')

        for row in csvreader:

            flow_id = str(row['flow_id'])
            lat = str(row['X'])
            long = str(row['Y'])
            # Run DOWNFLOW
            name_folder = path_to_results +'/' + flow_id
            #os.mkdir(name_folder)
            os.chdir(name_folder)
            downflow.get_downflow_profile(lat, long, dem, path)
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
