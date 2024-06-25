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
import compute_spectral_radiance
import numpy as np
import csv
import json
import os
#import tkinter as tk
#from edit_json_gui import JsonEditorApp

if __name__ == "__main__":
    """ Instanciate Flowgo via run flowgo (either for one effusion rate or for many effusion rates
    for the given input parameters (json file) and log the results in a define folder 
    json file : e.g 'template.json'
    path to the result folder, e.g './results_flowgo/'
    """
    # TODO: Enter the path to the main folder
    path_to_folder = "/Users/chevrel/Documents/ICELAND/Jonas-holurhaun-2014/flowgo/"

    # ------------------------------------------------------ RUN FLOWGO -----------------------------------------------
    # TODO: enter the json file you want to run
    json_file = path_to_folder + "Holuhraun14.json"
    print(json_file)

    # Or you can open the JSON editor app
    #app = tk.Tk()
    #app.title("JSON editor")
    #editor = JsonEditorApp(app)
    #app.mainloop()
    #json_file = editor.load_json_data()

    flow_length = 9550

    # *****************************
    """Instanciate flowgo via run_flowgo.py for the given json """

    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)
    # Calculate Spectral Radiance and add column

    file_name_results = flowgo.get_file_name_results(path_to_folder, json_file)

    # ******************************
    """Instanciate flowgo via run_flowgo_effusion_rate_array.py and run it for many effusion rate using a given slope file 
    For that: define the slope file execute the simulation"""

    #slope_file = "resource/DEM_MaunaLoa1984.txt"
    #simulation = run_flowgo_effusion_rate_array.StartFlowgo()
    #simulation.run_flowgo_effusion_rate_array(json_file, path_to_folder, slope_file)

    name_folder = path_to_folder+"results/"
    path_to_results = name_folder
    result_1 = file_name_results.replace(path_to_folder, path_to_results)
    print("Results are now stored under :", path_to_results)
    os.replace(file_name_results, result_1)

    # ------------------------------------------------ PLOT RESULTS FROM CSV -----------------------------------------
    # -------------------------------------------- LOAD RESULTS FROM CSV --------------------------------------------
    # in order to plot several results on the same plot, use filename_array = ["Path_to_file1.csv","Path_to_file2.csv"]
    # TODO: Enter the path to other outputs files (csv file) that you want to compare with.
    #  The path must be writen as result_XX= " path to the results", and separate each path by a coma

    result_2 = path_to_folder + "/results/results_flowgo_Holurhaun_lin_emi_biren_swir_350m3s.csv"
    result_3 = path_to_folder + "/results/results_flowgo_Holurhaun_lin_emi_350m3s.csv"
    result_4 = path_to_folder + "/results/results_flowgo_Holurhaun_basic_350m3s.csv"

   # results_3 = path_to_folder + "/results/results_flowgo_Sierra Negra F3 - pre 30m - ML84_60m3s.csv"

    filename_array = [
        result_1,
        result_2,
        result_3,
        result_4
                        ]
    # Here define the title of the graph if needed
    title = "Holuhraun"
    # ------------------------------------------------- LOAD FIELD DATA ------------------------------------------------

    # Load field data enter the field data you want to plot
    channel_width_field = path_to_folder + "Channel_width_channel_Aufar.csv"
    channel_width_field_2 = path_to_folder + "Chanel_width_centerline-channel_aufar_image_points_50m.csv"
    channel_width_field_20140906 = path_to_folder + "Lava channel 20140906_width.csv"
    slope_file = path_to_folder +'slope_Transects_centerline-channel_aufar_image_points_50m.csv'
    slope_file_20140906 = path_to_folder + 'sommet_centerline_Lava channel 20140906.csv'
    spectral_radiance = path_to_folder + "Spectral_radiance_test.csv"

    # define the field data arrays if any and load the data
    field_width = []
    field_distance_width = []
    field_width_20140906 = []
    field_width_2 = []
    field_distance_width_2 = []
    field_distance_width_20140906 = []
    field_distance_slope = []
    field_slope = []
    field_distance_slope_20140906 = []
    field_slope_20140906 = []
    field_distance_spectral_radiance = []
    field_spectral_radiance = []

    with open(channel_width_field) as csvf:
        csvreader = csv.DictReader(csvf, delimiter=';')
        for row in csvreader:
            field_distance_width.append(float(row['Distance (m)']))
            field_width.append(float(row['Width (m)']))

    with open(channel_width_field_20140906) as csvf:
        csvreader = csv.DictReader(csvf, delimiter=';')
        for row in csvreader:
            field_distance_width_20140906.append(float(row['Distance (m)']))
            field_width_20140906.append(float(row['Width (m)']))

    with open(channel_width_field_2) as csvf:
        csvreader = csv.DictReader(csvf, delimiter=';')
        for row in csvreader:
            field_distance_width_2.append(float(row['Distance (m)']))
            field_width_2.append(float(row['Width (m)']))


    with open(slope_file, "r") as csvf:
        csvreader = csv.DictReader(csvf, delimiter=';')
        for row in csvreader:
            field_distance_slope.append(float(row['Distance (m)']))
            field_slope.append(float(row['Slope']))
    with open(slope_file_20140906, "r") as csvf:
        csvreader = csv.DictReader(csvf, delimiter=';')
        for row in csvreader:
            field_distance_slope_20140906.append(float(row['Distance (m)']))
            field_slope_20140906.append(float(row['Slope']))

    with open(spectral_radiance, "r") as csvf:
        csvreader = csv.DictReader(csvf, delimiter=';')
        for row in csvreader:
            field_distance_spectral_radiance.append(float(row['Distance (m)']))
            field_spectral_radiance.append(float(row['Spectral_radiance (W/m^2 micron)']))

    # ------------------------------------------------- PLOT FIGURES ------------------------------------------------
    # plot the figures and define the positions of the graphs

    # Temperature, crystal content, viscosity, slope
    fig1 = plt.figure(figsize=(10,8))
    plot_temperature = fig1.add_subplot(221)
    plot_crystals = fig1.add_subplot(222)
    plot_viscosity = fig1.add_subplot(223)
    plot_slope = fig1.add_subplot(224)

    fig2 = plt.figure(figsize=(15,4))
    plot_velocity = fig2.add_subplot(121)
    plot_width = fig2.add_subplot(122)

    #plot_spectral_radiance = fig2.add_subplot(133)


    fig3 = plt.figure(figsize=(10,8))
    plot_crust_temperature = fig3.add_subplot(321)
    plot_crustfraction = fig3.add_subplot(322)
    plot_effective_radiation_temperature = fig3.add_subplot(323)
    plot_epsilon_effective = fig3.add_subplot(324)
    plot_Qrad = fig3.add_subplot(325)


    # load data from results
    for filename in filename_array:
        distance_array = []
        slope_array = []
        temperature_array = []
        v_mean_array = []
        viscosity_array = []
        crystal_fraction_array = []
        width_array = []
        depth_array = []
        time_array = []
        effusion_rate = []
        yieldstrength_array = []
        shear_stress_array = []
        crust_temperature_array = []
        effective_cover_fraction_array = []
        epsilon_effective_array = []
        crystallization_rate_array = []
        crystallization_down_flow_array = []
        characteristic_surface_temperature_array = []
        effective_radiation_temperature_array = []
        effective_temperature_snyder_array = []
        flowgofluxforcedconvectionheat_array = []
        flowgofluxconductionheat_array = []
        flowgofluxradiationheat_array = []
        flowgofluxheatlossrain_array = []
        flowgofluxviscousheating_array = []
        flowgofluxsnyderheat_array = []
        spectral_radiance_array = []


        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')

            for row in csvreader:
                distance_array.append(float(row['position']))
                slope_array.append(float(row['slope']))
                temperature_array.append(float(row['core_temperature']))
                v_mean_array.append(float(row['mean_velocity']))
                viscosity_array.append(float(row['viscosity']))
                yieldstrength_array.append(float(row['tho_0']))
                shear_stress_array.append(float(row['tho_b']))
                crystal_fraction_array.append(float(row['crystal_fraction']))
                width_array.append(float(row['channel_width']))
                depth_array.append(float(row['channel_depth']))
                epsilon_effective_array.append(float(row['epsilon_effective']))
                effusion_rate.append(float(row['effusion_rate']))
                crust_temperature_array.append(float(row['crust_temperature']))
                effective_cover_fraction_array.append(float(row['effective_cover_fraction']))
                crystallization_rate_array.append(float(row['dphi_dtemp']))
                crystallization_down_flow_array.append(float(row['dphi_dx']))
            # surface temperature
                characteristic_surface_temperature_array.append(float(row['characteristic_surface_temperature']))
                effective_radiation_temperature_array.append(float(row['effective_radiation_temperature']))
                effective_temperature_snyder_array.append(float(row['effective_temperature_snyder']))
            # heat flux
                flowgofluxforcedconvectionheat_array.append(float(row['flowgofluxforcedconvectionheat']))
                flowgofluxradiationheat_array.append(float(row['flowgofluxradiationheat']))
                flowgofluxconductionheat_array.append(float(row['flowgofluxconductionheat']))
                flowgofluxsnyderheat_array.append(float(row['flowgofluxsnyderheat']))
                #flowgofluxheatlossrain_array.append(float(row['flowgofluxheatlossrain']))
                #flowgofluxviscousheating_array.append(float(row['flowgofluxviscousheating']))
            # Spectral radiance
                spectral_radiance_array.append(float(row['spectral_radiance']))

        run_out_distance = (max(distance_array) / 1000.0)
        step_size = distance_array[1]
        # convert radians to degree
        slope_degrees = []
        for i in range (0,len(slope_array)):
            slope_degrees.append(math.degrees(slope_array[i]))

        #convert Kelvin to celcius
        #temperature_celcius = []
        #for i in range (0,len(temperature_array)):
        #    temperature_celcius.append(temperature_array[i]-273.15)

        #crust_temperature_celcius = []
        #for i in range(0, len(crust_temperature_array)):
        #    crust_temperature_celcius.append(crust_temperature_array[i] - 273.15)
        #
        #characteristic_surface_temperature_celcius = []
        #for i in range(0, len(characteristic_surface_temperature_array)):
        #    characteristic_surface_temperature_celcius.append(characteristic_surface_temperature_array[i] - 273.15)
        #
        #effective_radiation_temperature_celcius = []
        #for i in range(0, len(crust_temperature_array)):
        #    effective_radiation_temperature_celcius.append(effective_radiation_temperature_array[i] - 273.15)
        #
        #effective_temperature_snyder_array_celcius = []
        #for i in range(0, len(crust_temperature_array)):
        #    effective_temperature_snyder_array_celcius.append(effective_temperature_snyder_array[i] - 273.15)

        # Initial effusion rate
        effusion_rate_init =[]
        for i in range (0,len(effusion_rate)):
            effusion_rate_init.append(effusion_rate[0])

        #Here enter the label for data

        label = "result"+filename.strip(name_folder).strip(".csv")
        print("label=",label)

        #plot1_fig1.set_title(str(title))
        plot_temperature.plot(distance_array, temperature_array, '-', label=label)
        plot_temperature.set_ylabel('Core Temperature (K)')
        #plot_temperature.set_xlim(xmax=12000)
        plot_temperature.grid(True)
        plot_temperature.get_yaxis().get_major_formatter().set_useOffset(False)

        # text_run_out ="The run out distance is {:3.2f} km in {:3.2f} min".format(float(run_out_distance),float(duration))
        # axis2_f1.text(100, 0.8, text_run_out)

        plot_velocity.plot(distance_array, v_mean_array, '-', label=label)
        #plot_velocity.set_xlim(xmax=12000)
        plot_velocity.set_xlabel('Distance (m)')
        # plot_velocity.legend(loc=3, prop={'size': 8})
        plot_velocity.set_ylabel('Mean velocity (m/s)')
        plot_velocity.grid(True)
        # title2 = "Solution for a constant effusion rate of {:3.2f} m\u00b3/s and \n at-source channel width of
        # {:3.1f} m and {:3.2f} deep".format(float(effusion_rate[0]), width_array[0], 0.)
        # plot_velocity.set_title(title2, ha='center')
        # plot_velocity.set_xlim(xmin=0)
        # plot_velocity.set_ylim(ymin=0, ymax=100)

        plot_width.plot(distance_array, width_array, '-',  label=label)
        plot_crystals.plot(distance_array, crystal_fraction_array, '-', label=label)
        #plot_crystals.legend(loc=2, prop={'size': 8})
        #plot_crystals.set_xlabel('Distance (m)')
        plot_crystals.set_ylabel('Crystal fraction')
        plot_crystals.grid(True)
        #plot_crystals.set_ylim(ymin=0, ymax=0.6)
        #plot_crystals.set_xlim(xmax=12000)

        plot_viscosity.plot(distance_array, viscosity_array, '-', label=label)
        plot_viscosity.set_xlabel('Distance (m)')
        plot_viscosity.set_ylabel('Viscosity (Pa.s)')
        #plot_viscosity.set_ylim(ymin=100, ymax=10000)
        #plot3_fig2.set_xlim(xmax=12000)
        plot_viscosity.set_yscale('log')
        plot_viscosity.grid(True)

        #plot_yieldstrength.plot(distance_array, yieldstrength_array, '-',  label= label)
        #plot_yieldstrength.set_xlabel('Distance (m)')
        #plot_yieldstrength.set_ylabel('Yield strength (Pa)')
        #plot_yieldstrength.set_yscale('log')
        #plot_yieldstrength.grid(True)
        #plot_yieldstrength.set_ylim(ymin=0.001,ymax=100000)
        #plot_yieldstrength.set_xlim(xmax=12000)


        #plot_Qconv.plot(distance_array, flowgofluxforcedconvectionheat_array, '-', label=label)
        #plot_Qconv.set_xlabel('Distance (m)')
        #plot_Qconv.set_ylabel('Qconv (W/m)')
        #plot_Qconv.set_yscale('log')
        #plot_Qconv_fig3.legend()
        #plot_Qconv.set_ylim(ymax=100000000)
        #plot_Qconv.set_xlim(xmax=1000)
        #plot_Qconv.grid(True)

        #plot_Qcond.plot(distance_array, flowgofluxconductionheat_array, '-', label=label)
        #plot_Qcond.set_xlabel('Distance (m)')
        #plot_Qcond.set_ylabel('Qcond (W/m)')
        #plot_Qcond.set_yscale('log')
        #plot_Qcond.set_ylim(ymax=100000000)
        #plot_Qcond.set_xlim(xmax=1000)
        #plot_Qcond.grid(True)

        plot_Qrad.plot(distance_array, flowgofluxradiationheat_array, '-', label=label)
        plot_Qrad.set_xlabel('Distance (m)')
        plot_Qrad.set_ylabel('Qrad (W/m)')
        plot_Qrad.set_yscale('log')
        plot_Qrad.set_ylim(ymax=10000000)
        #plot_Qrad.set_xlim(xmax=1000)
        plot_Qrad.grid(True)

        #plot_Qsnyderheat.plot(distance_array, flowgofluxsnyderheat_array, '-', label=label)
        #plot_Qsnyderheat.set_xlabel('Distance (m)')
        #plot_Qsnyderheat.set_ylabel('Qsnyder (W/m)')
        #plot_Qsnyderheat.set_yscale('log')
        #plot_Qsnyderheat.legend()
        #plot_Qsnyderheat.set_ylim(ymax=100000000)
        #plot_Qsnyderheat.set_xlim(xmax=1000)
        #plot_Qsnyderheat.grid(True)

        #plot_Qrain.plot(distance_array, flowgofluxheatlossrain_array, '-', label=label)
        #plot_Qrain.set_xlabel('Distance (m)')
        #plot_Qrain.set_ylabel('Qrain (W/m)')
        #plot_Qrain.set_yscale('log')
        #plot_Qrain.set_ylim(ymin=0, ymax=100000000)
        #plot_Qrain.grid(True)
        #
        #plot_Qvisc.plot(distance_array, flowgofluxviscousheating_array, '-', label=label)
        #plot_Qvisc.set_xlabel('Distance (m)')
        #plot_Qvisc.set_ylabel('Qvisc (W/m)')
        #plot_Qvisc.set_yscale('log')
        #plot_Qvisc.set_ylim(ymin=0, ymax=100000000)
        #plot_Qvisc.grid(True)

    #    plot_spectral_radiance.plot(distance_array, spectral_radiance_array, '-', label=label)
    #    plot_spectral_radiance.set_xlabel('Distance (m)')
    #    plot_spectral_radiance.set_ylabel('Spectral Radiance (W/m)')
    #    plot_spectral_radiance.set_yscale('log')
        #plot_spectral_radiance.set_ylim(ymin=0, ymax=5000)

        #plot1_fig4.set_title("Crustal and surface conditions for " + str(title))
        plot_crustfraction.plot(distance_array, effective_cover_fraction_array, '-', label=label)
        plot_crustfraction.set_xlabel('Distance (m)')
        plot_crustfraction.set_ylabel('f crust')
        #plot_crustfraction.set_xlim(xmax=1000)

        plot_crust_temperature.plot(distance_array, crust_temperature_array, '-', label=label)
        plot_crust_temperature.set_xlabel('Distance (m)')
        plot_crust_temperature.set_ylabel(' T crust (K)')
        #plot_crust_temperature.set_xlim(xmax=12000)

        plot_epsilon_effective.plot(distance_array, epsilon_effective_array, '-', label=label)
        plot_epsilon_effective.set_xlabel('Distance (m)')
        plot_epsilon_effective.set_ylabel('Epsilon effective')
        #plot_crust_temperature.set_xlim(xmax=12000)

        plot_effective_radiation_temperature.plot(distance_array, effective_radiation_temperature_array, '-', label=label)
        plot_effective_radiation_temperature.set_xlabel('Distance (m)')
        plot_effective_radiation_temperature.set_ylabel('T eff rad (K)')
        #plot_effective_radiation_temperature4.set_xlim(xmax=1000)


        #plot_surface_temperature_conv.plot(distance_array, characteristic_surface_temperature_array, '-', label=label)
        #plot_surface_temperature_conv.set_xlabel('Distance (m)')
        #plot_surface_temperature_conv.set_ylabel('T conv (K)')
        # #plot_surface_temperature_conv.set_xlim(xmax=1000)

        #plot_effective_temperature_snyder.plot(distance_array, effective_temperature_snyder_array, '-', label=label)
        #plot_effective_temperature_snyder.plot(distance_array, effective_radiation_temperature_array, '--', label='Trad_'+label)
        #plot_effective_temperature_snyder.set_xlabel('Distance (m)')
        #plot_effective_temperature_snyder.set_ylabel('T eff snyder(K)')
        #plot_effective_temperature_snyder.set_xlim(xmax=1000)

        plot_slope.plot(distance_array, slope_degrees, label = label)


    plot_width.plot(field_distance_width, field_width, 'k.', label='channel width')
    plot_width.plot(field_distance_width_20140906, field_width_20140906, 'b.', label='channel width _20140906')
    plot_width.plot([flow_length, flow_length], [0, 600], 'r-', label='Runout')
    plot_width.set_xlabel('Distance (m)')
    plot_width.set_ylabel('Width (m)')
    plot_width.grid(True)
    plot_width.set_ylim(ymin=0, ymax=400)
    plot_width.set_xlim(xmin=0)
    # bbox_to_anchor=(1.05, 0.5) places the legend outside the plot area to the right

    plot_width.legend(bbox_to_anchor=(1.05, 0.5))
    #fig2.subplots_adjust(right=0.8, wspace=1)

    plot_slope.plot([flow_length, flow_length], [0, max(slope_file)], 'r-', label='Runout')
    plot_slope.plot(field_distance_slope, field_slope, 'k-', linewidth=0.5, label="Slope profile aufar")  # 7f7f7f
    plot_slope.plot(field_distance_slope_20140906, field_slope_20140906, 'b-', linewidth=0.5, label="Slope profile_20140906")  # 7f7f7f
    plot_slope.legend()
    plot_slope.set_xlabel('Distance (m)')
    plot_slope.set_ylabel('Slope (°)')
    # plot_slope.set_xlim(xmin=0)
    plot_slope.set_ylim(ymax=10)
    plot_slope.set_ylim(ymin=-2)
    plot_slope.set_yticks([-2, -1, 0, 1, 2, 3, 4, 5, 6])
    plot_slope.set_yticklabels(['-2', '-1', '0', '1', '2', '3', '4', '5', '6'])
    plot_slope.set_xlim(xmax=flow_length + 100)
    plot_slope.grid(True)
    # plot_slope.set_title("Slope profile for " + str(title))

    plot_crystals.plot([flow_length, flow_length], [0, 1], 'r-', label='Runout')




    #    plot_width.set_ylim(xmax=flow_length + 300)
    plot_temperature.plot([flow_length, flow_length], [min(temperature_array), max(temperature_array)], 'r-', label='Runout')
    plot_velocity.plot([flow_length, flow_length], [0, max(v_mean_array)], 'r-', label='Runout')
#    plot_spectral_radiance.plot(field_distance_spectral_radiance, field_spectral_radiance, 'r.', label="Spectral radiance SWIR")

    #plot2_fig1.legend(loc=0, prop={'size': 8})
    plot_temperature.legend()
#    plot_spectral_radiance.legend()



    fig1.tight_layout()
    fig1.savefig(path_to_folder + "./results/fig_1.png")
    fig2.tight_layout()
    fig2.savefig(path_to_folder + "./results/fig_2.png")
    fig3.tight_layout()
    fig3.savefig(path_to_folder + "./results/fig_3.png")
#    fig4.tight_layout()
 #   fig4.savefig(path_to_folder + "./results/fig_4.png")

    plt.show()
    plt.close()