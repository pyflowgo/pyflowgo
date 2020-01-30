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
import run_flowgo_effusion_rate_array



if __name__ == "__main__":

    # -------------------------------------------------- RUN FLOWGO  ---------------------------------------------------

    # TODO: enter the path where to store the results

    path_to_folder = os.path.abspath('')

    # TODO: enter the json file you want to run

    json_file = './resource/template.json'
    # *************** instanciate flowgo runner and run it ***************
    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)

    # *************** instanciate flowgo runner and run it for many effusion rate ***************

    #simulation = run_flowgo_effusion_rate_array.StartFlowgo()
    #slope_file = "resource/DEM_MaunaLoa1984.txt"
    #simulation.run_flowgo_effusion_rate_array(json_file, path_to_folder, slope_file)
