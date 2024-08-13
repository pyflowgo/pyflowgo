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

import run_flowgo
import os.path
import plot_flowgo_results
import os.path
import run_flowgo_effusion_rate_array

if __name__ == "__main__":
    """ Instanciate Flowgo via run_flowgo.py (either for one effusion rate or for many effusion rates
    for the given input paramters (json file) and log the results in a define folder 
    json file : e.g 'template.json'
    path to the result folder, e.g './results_flowgo/'
    """
    # path_to_folder = os.path.abspath('')
    path_to_folder = "./results_flowgo/"
    #json_file = './resource/template_2.json'
    #json_file= '/Users/chevrel/Documents/GitHub/pyflowgo/resource/input_parameters_MaunaUlu74_tests.json'
    json_file = '/Users/chevrel/Documents/ICELAND/Jonas-holurhaun-2014/flowgo/Holuhraun14.json'

    # ******** Instanciate flowgo via run flowgo for the given json *********************

    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)

    # ******** PLOT THE RESULTS *********************
    filename_results = flowgo.get_file_name_results(path_to_folder, json_file)
    print("filename_results", filename_results)
    #filename_array = [filename_results, "./results_flowgo/results_flowgo_template2_mp_10m3s.csv"]
    filename_array = [filename_results,"/Users/chevrel/Documents/ICELAND/Jonas-holurhaun-2014/flowgo/results/results_flowgo_Holurhaun_lin_emi_biren_tir_350m3s.csv"]


   # filename_array = [filename_results,"/Users/chevrel/Documents/GitHub/pyflowgo/MaunaUlu74/results_flowgo_Mauna Ulu June 1974 Best fit_165m3s.csv",
   #                   "/Users/chevrel/Documents/GitHub/pyflowgo/results_flowgo/results_flowgo_Mauna Ulu June 1974 Best fit mp_165m3s.csv"]
    plot_flowgo_results.plot_all_results(path_to_folder, filename_array)


