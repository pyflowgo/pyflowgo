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
import run_flowgo_effusion_rate_array
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import json
import os

# Conditional to call the main function
if __name__ == "__main__":

    # Load the CSV data into a DataFrame
    # Path to your CSV file
    results_path = '/Users/chevrel/Documents/GitHub/pyflowgo/Tolbachik/results/results_flowgo_2012_w30-er-278m3s_2emi_test_cont_278m3s copie.csv'  # Update with your actual file path

    def compute_spectral_radiance(results_path):
        # Load the CSV data into a DataFrame
        df = pd.read_csv(results_path)

        # Constants
        l_pixel = 30  # pixel length
        a_pixel = l_pixel * l_pixel
        atmospheric_transmissivity = 0.8
        epsilon_3 = 0.1  # emissivity of snow
        lamda = 0.8675e-6  # micrometers
        h = 6.6256e-34  # Js
        c = 2.9979e8  # ms-1
        c1 = 2 * math.pi * h * c ** 2  # W.m^2
        kapa = 1.38e-23  # JK-1
        c2 = h * c / kapa  # m K
        background_temperature = 258  # K


        effective_cover_fraction = df['effective_cover_fraction']
        crust_temperature = df['crust_temperature']
        molten_material_temperature = df['molten_material_temperature']
        channel_width = df['channel_width']
        epsilon_effective = df['epsilon_effective']

        a_lava = l_pixel * channel_width  # Area cover by lava
        a_hot = a_lava * (1 - effective_cover_fraction)  # Area cover by molten lava
        a_crust = a_lava * effective_cover_fraction  # Area cover by crust
        p_hot = a_hot / a_pixel  # portion of pixel cover by molten lava
        p_crust = a_crust / a_pixel  # portion of pixel cover by crust

        # spectral radiance of the crust component
        crust_spectral_radiance = (c1 * lamda ** (-5)) / (np.exp(c2 / (lamda * crust_temperature)) - 1)
        # spectral radiance of the molten component
        molten_spectral_radiance = c1 * lamda ** (-5) / (np.exp(c2 / (lamda * molten_material_temperature)) - 1)
        # spectral radiance of  background component
        background_spectral_radiance = c1 * lamda ** (-5) / (np.exp(c2 / (lamda * background_temperature)) - 1)

        # equation radiance W/m2/m
        spectral_radiance_m = atmospheric_transmissivity * (emissivity_molten * p_hot * molten_spectral_radiance +
                                                            emissivity_crust * p_crust * crust_spectral_radiance +
                                                            (1 - p_hot - p_crust) * epsilon_3 * background_spectral_radiance)

        # equation radiance W/m2/micro
        spectral_radiance = spectral_radiance_m * 1e-6
        # Add the spectral radiance as a new column to the DataFrame
        df['spectral_radiance'] = spectral_radiance

        # Save the modified DataFrame back to the same CSV file
        df.to_csv(results_path, index=False)

        print(f"Modified file saved to: {results_path}")

    # Compute spectral radiance and get the modified DataFrame
    spectral_radiance_values = compute_spectral_radiance(results_path)
