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
import pyflowgo.run_flowgo_effusion_rate_array as run_flowgo_effusion_rate_array
import pyflowgo.plot_flowgo_results as plot_flowgo_results



if __name__ == "__main__":


    """ Instanciate Flowgo via run flowgo (either for one effusion rate or for many effusion rates
    for the given input paramters (json file) and log the results in a define folder 
    json file : e.g 'template.json'
    path to the result folder, e.g './results_flowgo/'
    
    """
    #path_to_folder = os.path.abspath('')
    path_to_folder = "./results_flowgo/"
    json_file = './resource/template_2.json'

    # *****************************
    """Instanciate flowgo via run-flowgo for the given json """

    flowgo = run_flowgo.RunFlowgo()
    #flowgo.run(json_file, path_to_folder)

    # ******************************
    """Instanciate flowgo and run it for a range of effusion rates using a given slope file 
    For that you must define 
    -> the range of effusion rates
    -> the slope file """

    effusion_rates = {
        "first_eff_rate": 5,
        "last_eff_rate": 35,
        "step_eff_rate": 5
    }
    slope_file = "resource/DEM_MaunaLoa1984.txt"
    simulation = run_flowgo_effusion_rate_array.StartFlowgo()
    simulation.run_flowgo_effusion_rate_array(json_file, path_to_folder, slope_file, effusion_rates)
