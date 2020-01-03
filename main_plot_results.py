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

import plot_flowgo_results

if __name__ == "__main__":

    """ 
    PLOT RESULTS FROM CSV
    Enter the path to the outputs (csv file).
    example: filename_array = ["Path_to_the_file1.csv","Path_to_the_file2.csv","Path_to_the_file2.csv"]
    
    """

    # TODO: enter the CSV file you want to plot
    path_to_folder =  "./"

    filename_array = ["./results_main_flowgo_template_3m3s.csv",
                      "./results_main_flowgo_template_10m3s.csv"]

    plot_flowgo_results.plot_all_results(path_to_folder, filename_array)


