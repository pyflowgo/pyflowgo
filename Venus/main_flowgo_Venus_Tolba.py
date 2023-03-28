
# This file allow to run FLOWGO using the PyFLOWGO library, and specifically for the Mauna Ulu 1974 lava flow.
# Refer to Harris, Rowland and Chevrel 202X "Anatomy of a channel-fed 'a'a lava flow system"  submitted to Bul Volc.
#
# Copyright 2017 PyFLOWGO development team (Magdalena Oryaelle Chevrel and Jeremie Labroquere)
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


import math
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
import os
import run_flowgo

if __name__ == "__main__":

    # TODO: Enter the path to the main folder
    path_to_folder = ""
    # ------------------------------------------------------ RUN FLOWGO -----------------------------------------------
    # TODO: enter the json file you want to run
    json_file= path_to_folder + "Tolb_1975_Venus.json"

    # Instanciate flowgo runner and run it
    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)
    file_name_results = flowgo.get_file_name_results(path_to_folder, json_file)
    result_1 = file_name_results
    print("Results are now stored under :", "/results/"+result_1)

    # -------------------------------------------- LOAD RESULTS FROM OTHER RUNS --------------------------------------------
    # in order to plot several results on the same plot, use filename_array = ["Path_to_file1.csv","Path_to_file2.csv"]
    # TODO: Enter the path to other outputs files (csv file) that you want to compare with.
    #  The path must be writen as result_XX= " path to the results", and separate each path by a coma
    flow_length = 10870
    result_2 = "./results/results_flowgo_template_test_rad_lin_emi_700m3s.csv"
    #results_3 = "/Users/chevrel/Documents/GitHub/pyflowgo/Venus/results/results_flowgo_template_Snyder_700m3s.csv"
    name = ".results/results_flowgo_"
    filename_array = [
        result_1,
        result_2,
     #   results_3
                        ]
    # Here define the title of the graph if needed
    title = "Venus tolba 1975"
    # ------------------------------------------------- LOAD FIELD DATA ------------------------------------------------
    # define the field data arrays if any
    field_width = []
    field_distance = []

    # TODO: enter the field data you want to plot
    channel_width_field = path_to_folder + "field_data/field_width_2012.csv"

    # SLOPE
    slope_file = path_to_folder + 'field_data/venus_c_1.txt'

    with open(slope_file, "r") as f_slope :
        latitude = []
        longitude = []
        distance = []
        slope = []
        elevation = []
        latitude_column_number = 0
        longitude_column_number = 1
        elevation_column_number = 2
        distance_column_number = 3
        slope_column_number = 4
        f_slope.readline()

        for line in f_slope:
            split_line = line.strip('\n').split('\t')
            slope.append(float(split_line[slope_column_number]))
            distance.append(float(split_line[distance_column_number]))
#           elevation.append(float(split_line[elevation_column_number]))
#           latitude.append(float(split_line[latitude_column_number]))
#           longitude.append(float(split_line[longitude_column_number]))

    # ------------------------------------------------- PLOT FIGURES ------------------------------------------------
    # plot the figures and define the positions of the graphs

    fig1 = plt.figure(figsize=(10,8)) #Temperaure, crustal content, width and velosity
    plot1_fig1 = fig1.add_subplot(221)
    plot6_fig1 = fig1.add_subplot(222)
    plot5_fig1 = fig1.add_subplot(223)
    plot2_fig1 = fig1.add_subplot(224)

    fig2 = plt.figure(figsize=(10,4)) #Viscosity and yield strength
    plot3_fig2 = fig2.add_subplot(121)
    plot4_fig2 = fig2.add_subplot(122)

    fig3 = plt.figure() #heat loss
    plot1_fig3 = fig3.add_subplot(411)
    plot2_fig3 = fig3.add_subplot(412)
    plot3_fig3 = fig3.add_subplot(413)
    plot6_fig3= fig3.add_subplot(414)
    # plot4_fig3 = fig3.add_subplot(324)
    # plot5_fig3 = fig3.add_subplot(325)
    # plot6_fig3 = fig3.add_subplot(326)

    fig4 = plt.figure(figsize=(6,7)) #crust and surface temperature
    plot1_fig4 = fig4.add_subplot(511)
    plot2_fig4 = fig4.add_subplot(512)
    plot3_fig4 = fig4.add_subplot(513)
    plot4_fig4 = fig4.add_subplot(514)
    plot5_fig4= fig4.add_subplot(515)

    fig5 = plt.figure() #: the slope
    plot1_fig5 = fig5.add_subplot(111)

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
        flowgofluxsnyderheat_array= []


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
#                time_array.append(float(row['current_time']))
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


        run_out_distance = (max(distance_array) / 1000.0)
        step_size = distance_array[1]
        # convert radians to degree
        slope_degrees =[]
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
        print(filename_array)
        label = filename.strip(name).strip(".csv")
        #plot1_fig1.set_title(str(title))
        plot1_fig1.plot(distance_array, temperature_array, '-', label=label)
        plot1_fig1.set_ylabel('Core Temperature (K)')
        #plot1_fig1.set_xlim(xmax=12000)
        plot1_fig1.grid(True)
        plot1_fig1.get_yaxis().get_major_formatter().set_useOffset(False)

        # text_run_out ="The run out distance is {:3.2f} km in {:3.2f} min".format(float(run_out_distance),float(duration))
        # axis2_f1.text(100, 0.8, text_run_out)

        plot2_fig1.plot(distance_array, v_mean_array, '-', label=label)

        #plot2_fig1.set_xlim(xmax=12000)
        plot2_fig1.set_xlabel('Distance (m)')
        # plot2_fig1.legend(loc=3, prop={'size': 8})
        plot2_fig1.set_ylabel('Mean velocity (m/s)')
        plot2_fig1.grid(True)
        # title2 = "Solution for a constant effusion rate of {:3.2f} m\u00b3/s and \n at-source channel width of
        # {:3.1f} m and {:3.2f} deep".format(float(effusion_rate[0]), width_array[0], 0.)
        # plot2_fig1.set_title(title2, ha='center')
        # plot2_fig1.set_xlim(xmin=0)
        # plot2_fig1.set_ylim(ymin=0, ymax=100)

        plot5_fig1.plot(distance_array, width_array, '-',  label=label)
        plot5_fig1.set_xlabel('Distance (m)')
        plot5_fig1.set_ylabel('Width (m)')
        plot5_fig1.grid(True)
        # plot5_fig1.legend(loc=2, prop={'size': 8})
        # axis1_f2.set_xlim(xmin=0)
        plot5_fig1.set_ylim(ymin=0, ymax=600)
        plot5_fig1.set_xlim(xmin=0)
        #plot5_fig1.set_xlim(xmax=12000)

        plot6_fig1.plot(distance_array, crystal_fraction_array, '-', label=label)
        #plot6_fig1.legend(loc=2, prop={'size': 8})
        #plot6_fig1.set_xlabel('Distance (m)')
        plot6_fig1.set_ylabel('Crystal fraction')
        plot6_fig1.grid(True)
        # plot6_fig1.set_ylim(ymin=0, ymax=0.6)
        #plot6_fig1.set_xlim(xmax=12000)

        plot3_fig2.plot(distance_array, viscosity_array, '-', label=label)
        plot3_fig2.set_xlabel('Distance (m)')
        plot3_fig2.set_ylabel('Viscosity (Pa s)')
        #plot3_fig2.set_ylim(ymin=100, ymax=10000)
        #plot3_fig2.set_xlim(xmax=12000)
        plot3_fig2.set_yscale('log')
        plot3_fig2.grid(True)

        plot4_fig2.plot(distance_array, yieldstrength_array, '-',  label= label)
        plot4_fig2.set_xlabel('Distance (m)')
        plot4_fig2.set_ylabel('Yield strength (Pa)')
        plot4_fig2.set_yscale('log')
        plot4_fig2.grid(True)
        # plot4_fig1.set_ylim(ymin=0.001,ymax=100000)
        #plot4_fig2.set_xlim(xmax=12000)

        # figure 3
        plot2_fig3.plot(distance_array, flowgofluxforcedconvectionheat_array, '-', label=label)
        plot2_fig3.set_xlabel('Distance (m)')
        plot2_fig3.set_ylabel('Qconv (W/m)')
        plot2_fig3.set_yscale('log')
        #plot2_fig3.legend()
        plot2_fig3.set_ylim(ymax=100000000)
        #plot2_fig3.set_xlim(xmax=1000)
        plot2_fig3.grid(True)

        plot1_fig3.plot(distance_array, flowgofluxconductionheat_array, '-', label=label)
        plot1_fig3.set_xlabel('Distance (m)')
        plot1_fig3.set_ylabel('Qcond (W/m)')
        plot1_fig3.set_yscale('log')
        plot1_fig3.set_ylim(ymax=100000000)
        #plot2_fig3.set_xlim(xmax=1000)
        plot1_fig3.grid(True)

        plot3_fig3.plot(distance_array, flowgofluxradiationheat_array, '-', label=label)
        plot3_fig3.set_xlabel('Distance (m)')
        plot3_fig3.set_ylabel('Qrad (W/m)')
        plot3_fig3.set_yscale('log')
        plot3_fig3.set_ylim(ymax=100000000)
        #plot3_fig3.set_xlim(xmax=1000)
        plot3_fig3.grid(True)

        plot6_fig3.plot(distance_array, flowgofluxsnyderheat_array, '-', label=label)
        plot6_fig3.set_xlabel('Distance (m)')
        plot6_fig3.set_ylabel('Qsnyder (W/m)')
        plot6_fig3.set_yscale('log')
        plot6_fig3.legend()
        plot6_fig3.set_ylim(ymax=100000000)
        # plot1_fig3.set_xlim(xmax=1000)
        plot6_fig3.grid(True)

        # plot4_fig3.plot(distance_array, flowgofluxheatlossrain_array, '-', label=label)
        # plot4_fig3.set_xlabel('Distance (m)')
        # plot4_fig3.set_ylabel('Qrain (W/m)')
        # plot4_fig3.set_yscale('log')
        # plot4_fig3.set_ylim(ymin=0, ymax=100000000)
        # plot4_fig3.grid(True)
        #
        # plot5_fig3.plot(distance_array, flowgofluxviscousheating_array, '-', label=label)
        # plot5_fig3.set_xlabel('Distance (m)')
        # plot5_fig3.set_ylabel('Qvisc (W/m)')
        # plot5_fig3.set_yscale('log')
        # plot5_fig3.set_ylim(ymin=0, ymax=100000000)
        # plot5_fig3.grid(True)


        #plot1_fig4.set_title("Crustal and surface conditions for " + str(title))
        plot1_fig4.plot(distance_array, effective_cover_fraction_array, '-', label=label)
        plot1_fig4.set_xlabel('Distance (m)')
        plot1_fig4.set_ylabel('f crust')
        #plot1_fig4.set_xlim(xmax=1000)

        plot2_fig4.plot(distance_array, crust_temperature_array, '-', label=label)
        plot2_fig4.set_xlabel('Distance (m)')
        plot2_fig4.set_ylabel(' T crust (K)')
        #plot2_fig4.set_xlim(xmax=12000)

        plot3_fig4.plot(distance_array, effective_radiation_temperature_array, '-', label=label)
        plot3_fig4.set_xlabel('Distance (m)')
        plot3_fig4.set_ylabel('T eff rad (K)')
        # plot1_fig4.set_xlim(xmax=1000)

        plot4_fig4.plot(distance_array, characteristic_surface_temperature_array, '-', label=label)
        plot4_fig4.set_xlabel('Distance (m)')
        plot4_fig4.set_ylabel('T conv (K)')
        # plot1_fig4.set_xlim(xmax=1000)

        plot5_fig4.plot(distance_array, effective_temperature_snyder_array, '-', label=label)
        plot5_fig4.plot(distance_array, effective_radiation_temperature_array, '--', label='Trad_'+label)
        plot5_fig4.set_xlabel('Distance (m)')
        plot5_fig4.set_ylabel('T eff snyder(K)')
        # plot1_fig4.set_xlim(xmax=1000)

        plot1_fig5.plot(distance, slope, '#7f7f7f', linewidth=0.5, label="Slope profile")
        plot1_fig5.plot(distance_array, slope_degrees, 'k-',  label = label)
        plot1_fig5.set_xlabel('Distance (m)')
        plot1_fig5.set_ylabel('Slope (°)')
        plot1_fig5.set_xlim(xmin=0)
        #plot1_fig5.set_xlim(xmax=12000)
        #plot1_fig5.grid(True)
       # plot1_fig5.set_title("Slope profile for " + str(title))
    plot1_fig5.plot([flow_length, flow_length], [0, max(slope_degrees)], 'r-', label='Runout')
    plot6_fig1.plot([flow_length, flow_length], [0, 1], 'r-', label='Runout')
    plot5_fig1.plot([flow_length, flow_length], [0, 600], 'r-', label='Runout')
    plot1_fig1.plot([flow_length, flow_length], [min(temperature_array), max(temperature_array)], 'r-', label='Runout')
    plot2_fig1.plot([flow_length, flow_length], [0, max(v_mean_array)], 'r-', label='Runout')
    #plot2_fig1.legend(loc=0, prop={'size': 8})
    plot1_fig3.legend(loc=0, prop={'size': 8})
    plot1_fig4.legend(loc=0, prop={'size': 8})
    plot1_fig5.legend(loc=0, prop={'size': 8})
    plot1_fig1.legend(loc=0, prop={'size': 8})
    plot5_fig1.legend(loc=0, prop={'size': 8})
    plot5_fig4.legend(loc=0, prop={'size': 8})


    fig1.tight_layout()
    fig1.savefig(path_to_folder + "./results/fig1.png")
    fig2.tight_layout()
    fig2.savefig(path_to_folder + "./results/fig2.png")
    fig3.tight_layout()
    fig3.savefig(path_to_folder + "./results/fig3.png")
    fig4.tight_layout()
    fig4.savefig(path_to_folder + "./results/fig4.png")
    fig5.tight_layout()
    fig5.savefig(path_to_folder + "./results/fig5.png")
    plt.show()
    plt.close()


    plt.show()