import csv
import json
import os

import run_flowgo
import plot_flowgo_results
import run_outs



class StartFlowgo:

    def make_vent_list(self, csv_vent_list):
        liste = []

        with open(csv_vent_list, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=';')

            for row in csvreader:
                eruption_name = '_' + str(row['flow_id'])
                liste.append(eruption_name)

        return liste

    def make_new_json(self, template_json_file, eruption_name, slope_file, output_file):
        read_json_data = None
        with open(template_json_file, "r") as data_file:
            read_json_data = json.load(data_file)
            read_json_data["lava_name"] = eruption_name
            read_json_data["slope_file"] = slope_file

        with open(output_file, 'w') as fp:
            json.dump(read_json_data, fp)

    def run_flowgo_effusion_rate_array(self, json_file: str, path_to_folder, slope_file):
        """
        This method allows running pyFLOWGO for various eruption rate and given an eruption name

        """
        filename_array = []

        for effusion_rate_init in range(5, 65, 5):
            # update and write the effusion rate in configuration file
            file_directory = os.path.dirname(json_file)
            file_name = os.path.splitext(os.path.basename(json_file))[0]
            file_extension = os.path.splitext(os.path.basename(json_file))[1]

            updated_json_file = path_to_folder + file_name + "_" + str(effusion_rate_init) + "m3s" + file_extension

            with open(json_file, "r") as data_file:
                data = json.load(data_file)
                data["effusion_rate_init"] = effusion_rate_init

            with open(updated_json_file, 'w') as fp:
                json.dump(data, fp)

            # instanciate flowgo runner and run it
            flowgo = run_flowgo.RunFlowgo()
            flowgo.run(updated_json_file, path_to_folder)

            lava_name = data["lava_name"]
            filename = path_to_folder + 'results_flowgo_' + lava_name + "_" + str(effusion_rate_init) + "m3s.csv"

            # print(filename)
            print('^^^^^^^^^^^^^^^^^^^^^^ End  for ' + str(effusion_rate_init) + "_m3s ^^^^^^^^^^^^^^^^^^^^^^^^")
            filename_array.append(filename)

        flow_id = lava_name

        plot_flowgo_results.plot_all_results(path_to_folder, filename_array)

        run_outs.get_run_outs(path_to_folder, filename_array, slope_file, flow_id)

        #run_outs_file_array = []
        #run_outs_file_array.append(run_outs.run_outs_get_file_name(path_to_folder, flow_id))

        #for run_outs_file in run_outs_file_array:
            #run_outs.plot_run_outs(path_to_folder, run_outs_file)

        print("******************************  End of the eruption rates loop ******************************")













