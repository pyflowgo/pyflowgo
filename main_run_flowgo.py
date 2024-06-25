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
import tkinter as tk
from tkinter import filedialog
import numpy as np
root = tk.Tk()
root.withdraw() # Hide the main window




if __name__ == "__main__":


    """ Instanciate Flowgo via run flowgo (either for one effusion rate or for many effusion rates
    for the given input paramters (json file) and log the results in a define folder 
    json file : e.g 'template.json'
    path to the result folder, e.g './results_flowgo/'
    
    """
    #path_to_folder = os.path.abspath('')
    #path_to_folder = "/Users/chevrel/Documents/GitHub/pyflowgo/resource/"
    #json_file = "/Users/chevrel/Documents/GitHub/pyflowgo/resource/template.json"

    # Select a file
    fichier = filedialog.askopenfilename(
        title='Select a json file',
        filetypes=(("Json file", "*.json"), ("All files", "*.*")))
    # Close the Tkinter root window
    root.destroy()
    # Extract the directory and file name
    path_to_folder = os.path.dirname(fichier)+"/"
    json_file = os.path.basename(fichier)
    Wd = (path_to_folder)
    print(path_to_folder)
    os.chdir(Wd)

    # *****************************
    """Instanciate flowgo via run_flowgo.py for the given json """

    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)

    # ******************************
    """Instanciate flowgo ia run_flowgo_effusion_rate_array.py and run it for many effusion rate using a given slope file 
    For that: define the slope file execute the simulation"""

    # slope_file = "resource/DEM_MaunaLoa1984.txt"
    #simulation = run_flowgo_effusion_rate_array.StartFlowgo()
    #simulation.run_flowgo_effusion_rate_array(json_file, path_to_folder, slope_file)
