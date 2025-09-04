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

import pyflowgo.run_flowgo as run_flowgo
import os.path
import pyflowgo.plot_flowgo_results as plot_flowgo_results
import pyflowgo.run_flowgo_effusion_rate_array as run_flowgo_effusion_rate_array
import os
import json


if __name__ == "__main__":
    """ Instanciate Flowgo via run_flowgo.py (either for one effusion rate or for many effusion rates
    for the given input parameters (json file) and log the results in a define folder 
    json file : e.g 'template.json'
    path to the result folder, e.g './results_flowgo/'
    """

    path_to_folder = os.path.join(os.path.abspath(''), "results_flowgo")
    json_file = os.path.join(os.path.abspath(''), 'resource', 'template_2.json')
    with open(json_file, "r") as file:
        json_data = json.load(file)
        slope_file = json_data.get('slope_file')



    # ******** Instanciate flowgo via run flowgo for the given json *********************

    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)

    # ******** PLOT THE RESULTS *********************
    filename_results = flowgo.get_file_name_results(path_to_folder, json_file)
    file_to_compare = os.path.join(os.path.abspath(''),'results_flowgo', 'results_flowgo_template2_10m3s_valid.csv')
    filename_array = [filename_results, file_to_compare]
    plot_flowgo_results.plot_all_results(path_to_folder, filename_array, json_file)
    plot_flowgo_results.plt.show()
    plot_flowgo_results.plt.close()


    # *************** Instanciate flowgo via run_flowgo_effusion_rate_array for various effusion rate *********************
    """Instanciate flowgo and run it for a range of effusion rates using a given slope file
    For that you must define
    -> the range of effusion rates
    -> the slope file """

    effusion_rates = {
        "first_eff_rate": 5,
        "last_eff_rate": 35,
        "step_eff_rate": 5
    }
    #simulation = run_flowgo_effusion_rate_array.StartFlowgo()
    #simulation.run_flowgo_effusion_rate_array(json_file, path_to_folder, slope_file, effusion_rates)
    # ******** PLOT THE RESULTS *********************
    plot_flowgo_results.plt.show()
    plot_flowgo_results.plt.close()
