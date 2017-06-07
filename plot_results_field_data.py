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

import math
import matplotlib.pyplot as plt
import numpy as np
import csv

# ------------------------------------------------ PLOT RESULTS FROM CSV -----------------------------------------------

if __name__ == "__main__":

    # -------------------------------------------- LOAD RESULTS FROM CSV --------------------------------------------
    # TODO: Enter the path to the outputs (csv file). The path must be writen with " ", and separate each path by a coma
    # in order to plot several results on the same plot .
    # example: filename_array = ["Path_to_the_file1.csv","Path_to_the_file2.csv","Path_to_the_file2.csv"]
    filename_array = ["results_template_2_10m.csv"]
    # Here define the title of the graphs
    title = "lava name template"
    # ------------------------------------------------- LOAD FIELD DATA ------------------------------------------------
    # define the data arrays
    field_distance1 = []
    field_width = []
    field_distance2 = []
    field_distance3 = []
    field_distance4 = []
    field_distance5 = []
    field_tglass = []
    field_tglass_olivine = []
    field_xstals = []
    field_ys = []

    # TODO: Enter the path to the data
    with open("resource/field_data/field_temp_glass.csv") as csvf:
        csvreader = csv.DictReader(csvf, delimiter=',')
        for row in csvreader:
            field_distance1.append(float(row['Distance (m)']))
            field_tglass.append(float(row['Temperature C (glass method)']))

    with open("resource/field_data/field_xtals.csv") as csvf:
        csvreader = csv.DictReader(csvf, delimiter=',')
        for row in csvreader:
            field_distance2.append(float(row['Distance (m)']))
            field_xstals.append(float(row['Total xtals']))

    with open("resource/field_data/field_width.csv") as csvf:
        csvreader = csv.DictReader(csvf, delimiter=',')
        for row in csvreader:
            field_distance3.append(float(row['Distance (m)']))
            field_width.append(float(row['Measured Width (m)']))

    # plot figure 1: here define the positions of the graphs in figure 1
    fig1 = plt.figure()
    plot1_fig1 = fig1.add_subplot(321)
    plot2_fig1 = fig1.add_subplot(322)
    plot3_fig1 = fig1.add_subplot(323)
    plot4_fig1 = fig1.add_subplot(324)
    plot5_fig1 = fig1.add_subplot(325)
    plot6_fig1 = fig1.add_subplot(326)

    # plot figure 2: here define the positions of the graphs in figure 2
    fig2 = plt.figure()
    plot1_fig2 = fig2.add_subplot(311)
    plot2_fig2 = fig2.add_subplot(312)
    plot3_fig2 = fig2.add_subplot(313)
    # plot4_fig2 = fig3.add_subplot(324)
    # plot5_fig2 = fig3.add_subplot(325)
    # plot6_fig2 = fig3.add_subplot(326)

    # plot figure 3: here define the positions of the graphs in figure 3
    fig3 = plt.figure()
    plot1_fig3 = fig3.add_subplot(411)
    plot2_fig3 = fig3.add_subplot(412)
    plot3_fig3 = fig3.add_subplot(413)
    plot4_fig3 = fig3.add_subplot(414)


    # plot figure 4: here define the positions of the graphs in figure 4
    fig4 = plt.figure()
    plot1_fig4 = fig4.add_subplot(111)

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
        flowgofluxforcedconvectionheat_array = []
        flowgofluxconductionheat_array = []
        flowgofluxradiationheat_array = []
        flowgofluxheatlossrain_array = []
        flowgofluxviscousheating_array = []


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
                time_array.append(float(row['current_time']))
                effusion_rate.append(float(row['effusion_rate']))
                crust_temperature_array.append(float(row['crust_temperature']))
                effective_cover_fraction_array.append(float(row['effective_cover_fraction']))
                crystallization_rate_array.append(float(row['dphi_dtemp']))
                crystallization_down_flow_array.append(float(row['dphi_dx']))
                characteristic_surface_temperature_array.append(float(row['characteristic_surface_temperature']))
                effective_radiation_temperature_array.append(float(row['effective_radiation_temperature']))
                flowgofluxforcedconvectionheat_array.append(float(row['flowgofluxforcedconvectionheat']))
                flowgofluxconductionheat_array.append(float(row['flowgofluxconductionheat']))
                flowgofluxradiationheat_array.append(float(row['flowgofluxradiationheat']))
                #flowgofluxheatlossrain_array.append(float(row['flowgofluxheatlossrain']))
                #flowgofluxviscousheating_array.append(float(row['flowgofluxviscousheating']))

        run_out_distance = (max(distance_array) / 1000.0)
        step_size = distance_array[1]
        # convert radians to degree
        slope_degrees =[]
        for i in range (0,len(slope_array)):
            slope_degrees.append(math.degrees(slope_array[i]))

        # convert time to minutes
        duration = (max(time_array)/ 60.)
        time_minutes= []
        for i in range (0,len(time_array)):
            time_minutes.append(time_array[i] / 60.0)

        #convert Kelvin to celcius
        temperature_celcius = []
        for i in range (0,len(temperature_array)):
            temperature_celcius.append(temperature_array[i]-273.15)

        crust_temperature_celcius = []
        for i in range(0, len(crust_temperature_array)):
            crust_temperature_celcius.append(crust_temperature_array[i] - 273.15)

        characteristic_surface_temperature_celcius = []
        for i in range(0, len(characteristic_surface_temperature_array)):
            characteristic_surface_temperature_celcius.append(characteristic_surface_temperature_array[i] - 273.15)

        effective_radiation_temperature_celcius = []
        for i in range(0, len(crust_temperature_array)):
            effective_radiation_temperature_celcius.append(effective_radiation_temperature_array[i] - 273.15)

        # Initial effusion rate
        effusion_rate_init =[]
        for i in range (0,len(effusion_rate)):
            effusion_rate_init.append(effusion_rate[0])

        #Here enter the label for data
        label = filename.replace("results_","").strip(".csv")

        plot1_fig1.set_title(str(title))
        plot1_fig1.plot(distance_array, temperature_celcius, '-', label=label)
        plot1_fig1.set_ylabel('Core Temperature (°C)')
        # plot1_fig1.set_xlim(xmax=500)
        plot1_fig1.grid(True)
        plot1_fig1.get_yaxis().get_major_formatter().set_useOffset(False)

        # text_run_out ="The run out distance is {:3.2f} km in {:3.2f} min".format(float(run_out_distance),float(duration))
        # axis2_f1.text(100, 0.8, text_run_out)

        plot2_fig1.plot(distance_array, v_mean_array, '-', label=label)
        # plot2_fig1.set_xlim(xmax=1000)
        # plot2_fig1.legend(loc=3, prop={'size': 8})
        plot2_fig1.set_ylabel('Mean velocity (m/s)')
        plot2_fig1.grid(True)
        # title2 = "Solution for a constant effusion rate of {:3.2f} m\u00b3/s and \n at-source channel width of
        # {:3.1f} m and {:3.2f} deep".format(float(effusion_rate[0]), width_array[0], 0.)
        # plot2_fig1.set_title(title2, ha='center')
        # plot2_fig1.set_xlim(xmin=0)
        # plot2_fig1.set_ylim(ymin=0, ymax=100)

        plot3_fig1.plot(distance_array, viscosity_array, '-', label=label)
        # plot3_fig1.set_xlabel('Distance (m)')
        plot3_fig1.set_ylabel('Viscosity (Pa s)')
        plot3_fig1.set_ylim(ymin=1, ymax=1000000)
        # plot3_fig1.set_xlim(xmax=4000)
        plot3_fig1.set_yscale('log')
        plot3_fig1.grid(True)

        plot4_fig1.plot(distance_array, yieldstrength_array, '-',  label= label)
        # plot4_fig1.set_xlabel('Distance (m)')
        plot4_fig1.set_ylabel('Yield strength (Pa)')
        plot4_fig1.set_yscale('log')
        plot4_fig1.grid(True)
        # plot4_fig1.set_ylim(ymin=0.001,ymax=100000)
        # plot4_fig1.set_xlim(xmax=4000)

        plot5_fig1.plot(distance_array, width_array, '-',  label=label)
        plot5_fig1.set_xlabel('Distance (m)')
        plot5_fig1.set_ylabel('Width (m)')
        plot5_fig1.grid(True)
        # plot5_fig1.legend(loc=2, prop={'size': 8})
        # axis1_f2.set_xlim(xmin=0)
        plot5_fig1.set_ylim(ymin=0, ymax=200)
        plot5_fig1.set_xlim(xmax=1000)

        plot6_fig1.plot(distance_array, crystal_fraction_array, '-', label=label)
        #plot6_fig1.legend(loc=2, prop={'size': 8})
        plot6_fig1.set_xlabel('Distance (m)')
        plot6_fig1.set_ylabel('Crystal fraction')
        plot6_fig1.grid(True)
        # plot6_fig1.set_ylim(ymin=0, ymax=0.6)
        # plot6_fig1.set_xlim(xmax=500)

        # figure 2
        plot1_fig2.plot(distance_array, flowgofluxforcedconvectionheat_array, '-', label=label)
        plot1_fig2.set_xlabel('Distance (m)')
        plot1_fig2.set_ylabel('Qconv (W/m)')
        plot1_fig2.set_yscale('log')
        plot1_fig2.legend()
        plot1_fig2.set_ylim(ymin=0, ymax=100000000)
        #plot1_fig2.set_xlim(xmax=1000)
        plot1_fig2.grid(True)

        plot2_fig2.plot(distance_array, flowgofluxconductionheat_array, '-', label=label)
        plot2_fig2.set_xlabel('Distance (m)')
        plot2_fig2.set_ylabel('Qcond (W/m)')
        plot2_fig2.set_yscale('log')
        plot2_fig2.set_ylim(ymin=0, ymax=100000000)
        #plot2_fig2.set_xlim(xmax=1000)
        plot2_fig2.grid(True)

        plot3_fig2.plot(distance_array, flowgofluxradiationheat_array, '-', label=label)
        plot3_fig2.set_xlabel('Distance (m)')
        plot3_fig2.set_ylabel('Qrad (W/m)')
        plot3_fig2.set_yscale('log')
        plot3_fig2.set_ylim(ymin=0, ymax=100000000)
        #plot3_fig2.set_xlim(xmax=1000)
        plot3_fig2.grid(True)

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


        plot1_fig3.set_title("Crustal and surface conditions for " + str(title))
        plot1_fig3.plot(distance_array, effective_cover_fraction_array, '-', label=label)
        plot1_fig3.set_xlabel('Distance (m)')
        plot1_fig3.set_ylabel('f crust')
        #plot1_fig4.set_xlim(xmax=1000)

        plot2_fig3.plot(distance_array, crust_temperature_celcius, '-', label=label)
        plot2_fig3.set_xlabel('Distance (m)')
        plot2_fig3.set_ylabel(' T crust (°C)')
        #plot1_fig3.set_xlim(xmax=1000)

        plot3_fig3.plot(distance_array, effective_radiation_temperature_celcius, '-', label=label)
        plot3_fig3.set_xlabel('Distance (m)')
        plot3_fig3.set_ylabel('T eff (°C)')
        # plot1_fig3.set_xlim(xmax=1000)

        plot4_fig3.plot(distance_array, characteristic_surface_temperature_celcius, '-', label=label)
        plot4_fig3.set_xlabel('Distance (m)')
        plot4_fig3.set_ylabel('T conv(°C)')
        # plot1_fig3.set_xlim(xmax=1000)

        plot1_fig4.plot(distance_array, slope_degrees, '-',  label = label)
        plot1_fig4.set_xlabel('Distance (m)')
        plot1_fig4.set_ylabel('Slope (°)')
        plot1_fig4.grid(True)
        plot1_fig4.set_title("Slope profile for " + str(title))

    plot1_fig1.plot(field_distance1, field_tglass, 'ro', label='Field data')
    plot6_fig1.plot(field_distance2, field_xstals, 'ro')
    plot5_fig1.plot(field_distance3, field_width, 'ro')

    plot2_fig1.legend(loc=0, prop={'size': 8})
    plot1_fig2.legend(loc=0, prop={'size': 8})
    plot1_fig3.legend(loc=0, prop={'size': 8})
    plot1_fig4.legend(loc=0, prop={'size': 8})

#   plt.savefig(str(lava_name).replace(" ", "_").lower() + ".pdf", dpi=600, format='pdf')

    plt.show()
