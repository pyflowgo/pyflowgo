import math
import matplotlib.pyplot as plt
import csv
import os.path

def plot_all_results(path_to_folder, filename_array):
    # Initialiser les figures
    fig1, axes1 = plt.subplots(3, 2, figsize=(8, 8))
    fig2, axes2 = plt.subplots(3, 1, figsize=(8, 8))
    fig3, axes3 = plt.subplots(4, 1, figsize=(8, 8))
    fig4, plot_slope = plt.subplots(figsize=(8, 8))

    # Configuration des axes pour les figures
    axes1 = axes1.flatten()
    axes2 = axes2.flatten()
    axes3 = axes3.flatten()

    plot_core_temp = axes1[0]
    plot_mean_vel = axes1[1]
    plot_viscosity = axes1[2]
    plot_yield_strength = axes1[3]
    plot_width = axes1[4]
    plot_crystal = axes1[5]

    plot_Qconv = axes2[0]
    plot_Qcond = axes2[1]
    plot_Qrad = axes2[2]

    plot_Tcrust = axes3[0]
    plot_fcrust = axes3[1]
    plot_Teff = axes3[2]
    plot_Tconv = axes3[3]

    flow_id = os.path.abspath(path_to_folder)
    title = os.path.basename(flow_id)

    for filename in filename_array:
        label = filename.replace(path_to_folder + "results_flowgo_", "").strip(".csv")

        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            data = {col: [] for col in csvreader.fieldnames}

            for row in csvreader:
                for col in csvreader.fieldnames:
                    if col in row:
                        data[col].append(float(row[col]))

        distance_array = data.get('position', [])
        if not distance_array:
            print("no distance_array")

        temperature_array = data.get('core_temperature', [])
        v_mean_array = data.get('mean_velocity', [])
        viscosity_array = data.get('viscosity', [])
        yieldstrength_array = data.get('tho_0', [])
        width_array = data.get('channel_width', [])
        crystal_fraction_array = data.get('crystal_fraction', [])
        crust_temperature_array = data.get('crust_temperature', [])
        effective_cover_fraction_array = data.get('effective_cover_fraction', [])
        effective_radiation_temperature_array = data.get('effective_radiation_temperature', [])
        characteristic_surface_temperature_array= data.get('characteristic_surface_temperature', [])
        flowgofluxforcedconvectionheat_array = data.get('flowgofluxforcedconvectionheat', [])
        flowgofluxconductionheat_array = data.get('flowgofluxconductionheat', [])
        flowgofluxradiationheat_array = data.get('flowgofluxradiationheat', [])
        flowgofluxheatlossrain_array = data.get('flowgofluxheatlossrain', [])
        flowgofluxviscousheating_array= data.get('flowgofluxviscousheating', [])
        slope_array = data.get('slope', [])
        effusion_rate = data.get('effusion_rate', [])

        run_out_distance = (max(distance_array) / 1000.0)
        print("run_out_distance (km)= ", run_out_distance)
        step_size = distance_array[1]

        # Initial effusion rate
        effusion_rate_init =[]
        for i in range (0,len(effusion_rate)):
            effusion_rate_init.append(effusion_rate[0])

        # convert radians to degree
        slope_degrees = []
        for i in range(0, len(slope_array)):
            slope_degrees.append(math.degrees(slope_array[i]))
        plot_slope.plot(distance_array, slope_degrees, '-', label=label)
        plot_slope.set_xlim(xmin=0, xmax=max(distance_array) + 1000)
        plot_slope.set_ylabel('Slope (°)')
        plot_slope.set_xlabel('Distance (m)')
        plot_slope.grid(True)

        # convert Kelvin to celcius
        temperature_celcius = []
        for i in range(0, len(temperature_array)):
            temperature_celcius.append(temperature_array[i] - 273.15)

        crust_temperature_celcius = []
        for i in range(0, len(crust_temperature_array)):
            crust_temperature_celcius.append(crust_temperature_array[i] - 273.15)
        plot_Tcrust.plot(distance_array, crust_temperature_celcius, '-', label=label)
        plot_Tcrust.set_ylabel('T crust (°C)')
        plot_Tcrust.grid(True)

        plot_core_temp.plot(distance_array, temperature_celcius, '-', label=label)
        plot_core_temp.set_ylabel('Core Temperature (°C)')
        plot_core_temp.grid(True)
        plot_core_temp.get_yaxis().get_major_formatter().set_useOffset(False)

        plot_fcrust.plot(distance_array, effective_cover_fraction_array, '-', label=label)
        plot_fcrust.set_ylabel('Effective crust fraction')
        plot_fcrust.grid(True)

        plot_mean_vel.plot(distance_array, v_mean_array, '-', label=label)
        plot_mean_vel.set_ylabel('Mean velocity (m/s)')
        plot_mean_vel.grid(True)

        plot_viscosity.plot(distance_array, viscosity_array, '-', label=label)
        plot_viscosity.set_ylabel('Viscosity (Pa s)')
        plot_viscosity.set_ylim(ymin=1, ymax=1000000)
        plot_viscosity.set_yscale('log')
        plot_viscosity.grid(True)

        plot_yield_strength.plot(distance_array, yieldstrength_array, '-',  label= label)
        plot_yield_strength.set_ylabel('Yield strength (Pa)')
        plot_yield_strength.set_yscale('log')
        plot_yield_strength.grid(True)

        plot_width.plot(distance_array, width_array, '-',  label=label)
        plot_width.set_xlabel('Distance (m)')
        plot_width.set_ylabel('Width (m)')
        plot_width.grid(True)
        plot_width.set_ylim(ymin=0, ymax=200)

        plot_crystal.plot(distance_array, crystal_fraction_array, '-', label=label)
        #plot_crystal.legend(loc=2, prop={'size': 8})
        plot_crystal.set_xlabel('Distance (m)')
        plot_crystal.set_ylabel('Crystal fraction')
        plot_crystal.grid(True)

        if flowgofluxforcedconvectionheat_array:
            plot_Qconv.plot(distance_array, flowgofluxforcedconvectionheat_array, '-', label=label)
            plot_Qconv.set_ylabel('Qconv')
            plot_Qconv.grid(True)

        if characteristic_surface_temperature_array:
            characteristic_surface_temperature_celcius = []
            for i in range(0, len(characteristic_surface_temperature_array)):
                characteristic_surface_temperature_celcius.append(characteristic_surface_temperature_array[i] - 273.15)
            plot_Tconv.plot(distance_array, characteristic_surface_temperature_celcius, '-', label=label)
            plot_Tconv.set_xlabel('Distance (m)')
            plot_Tconv.set_ylabel('T surface conv (°C)')
            plot_Qconv.set_yscale('log')
            plot_Qconv.set_ylim(ymax=10000000)
            plot_Tconv.grid(True)

        if effective_radiation_temperature_array:
            effective_radiation_temperature_celcius = []
            for i in range(0, len(crust_temperature_array)):
                effective_radiation_temperature_celcius.append(effective_radiation_temperature_array[i] - 273.15)
            plot_Teff.plot(distance_array, effective_radiation_temperature_celcius, '-', label=label)
            plot_Teff.set_xlabel('Distance (m)')
            plot_Teff.set_ylabel('T eff rad (°C)')
            plot_Teff.grid(True)

        if flowgofluxconductionheat_array:
            plot_Qcond.plot(distance_array, flowgofluxconductionheat_array , '-', label=label)
            plot_Qcond.set_ylabel('Qcond')
            plot_Qcond.set_yscale('log')
            #plot_Qcond.set_ylim(ymax=10000000)
            plot_Qcond.grid(True)

        if flowgofluxradiationheat_array:
            plot_Qrad.plot(distance_array, flowgofluxradiationheat_array , '-', label=label)
            plot_Qrad.set_ylabel('Qrad')
            plot_Qrad.set_xlabel('Distance (m)')
            plot_Qrad.set_yscale('log')
            #plot_Qrad.set_ylim(ymax=10000000)
            plot_Qrad.grid(True)

        if flowgofluxheatlossrain_array:
            plot_Qrain.plot(distance_array, flowgofluxheatlossrain_array, '-', label=label)
            plot_Qrain.set_xlabel('Distance (m)')
            plot_Qrain.set_ylabel('Qrain (W/m)')
            plot_Qrain.set_yscale('log')
            #plot_Qrain.set_ylim(ymin=0, ymax=100000000)
            plot_Qrain.grid(True)

        if flowgofluxviscousheating_array:
            plot_Qvisc.plot(distance_array, flowgofluxviscousheating_array, '-', label=label)
            plot_Qvisc.set_xlabel('Distance (m)')
            plot_Qvisc.set_ylabel('Qvisc (W/m)')
            plot_Qvisc.set_yscale('log')
            #plot_Qvisc.set_ylim(ymin=0, ymax=100000000)
            plot_Qvisc.grid(True)

    # Configurations finales des figures
    plot_Qconv.set_title(str(title))
    plot_Qconv.legend(loc=1, prop={'size': 8})
    plot_Qconv.set_title("Heat fluxes for " + str(title))

    plot_Tcrust.set_title("Crustal and surface conditions for " + str(title))
    plot_Tcrust.legend(loc=0, prop={'size': 8})

    # Enregistrement des figures
    fig1.tight_layout()
    fig1.savefig("./lava_properties.png")

    fig2.tight_layout()
    fig2.savefig("./heat_fluxes.png")

    fig3.tight_layout()
    fig3.savefig("./crustal_conditions.png")

    fig4.savefig("./slope.png")
    plt.show()
