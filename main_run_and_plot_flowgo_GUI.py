import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pyflowgo.run_flowgo as run_flowgo
import pyflowgo.plot_flowgo_results as plot_flowgo_results
import pyflowgo.run_flowgo_effusion_rate_array as run_flowgo_effusion_rate_array
import json
import tempfile
import csv
from edit_json import open_editor  # import your function

def select_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        json_path_var.set(file_path)

def select_results_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        results_folder_var.set(folder_path)

def select_field_data_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        field_data_var.set(file_path)


def add_field_data(lava_properties, field_file):

    flow_length = None

    if field_file and os.path.exists(field_file):

        field_distance_temp = []
        field_temp = []

        field_distance_crystals = []
        field_crystals = []

        field_distance_bubbles = []
        field_bubbles = []

        field_distance_visco = []
        field_visco = []

        field_distance_width = []
        field_width = []

        with open(field_file) as csvf:
            csvreader = csv.DictReader(csvf, delimiter=";")

            for row in csvreader:

                distance = row.get("Distance(m)", "").strip()

                if not distance:
                    continue

                distance = float(distance)

                # Last valid distance = observed runout
                flow_length = distance

                # Temperature
                value = row.get("glass_temp", "").strip()
                if value:
                    field_distance_temp.append(distance)
                    field_temp.append(float(value))

                # Crystal fraction
                value = row.get("crystal_fraction", "").strip()
                if value:
                    field_distance_crystals.append(distance)
                    field_crystals.append(float(value))

                # Bubble fraction
                value = row.get("bubble_fraction", "").strip()
                if value:
                    field_distance_bubbles.append(distance)
                    field_bubbles.append(float(value))

                # Viscosity
                value = row.get("Viscosity(Pas)", "").strip()
                if value:
                    field_distance_visco.append(distance)
                    field_visco.append(float(value))

                # Width
                value = row.get("width(m)", "").strip()
                if value:
                    field_distance_width.append(distance)
                    field_width.append(float(value))

        if field_temp:
            lava_properties.axes[0].plot(
                field_distance_temp, field_temp, "ro", label="Field data"
            )

        if field_crystals:
            lava_properties.axes[1].plot(
                field_distance_crystals, field_crystals, "ro", label="Field data"
            )

        if field_bubbles:
            lava_properties.axes[2].plot(
                field_distance_bubbles, field_bubbles, "ro", label="Field data"
            )

        if field_visco:
            lava_properties.axes[3].plot(
                field_distance_visco, field_visco, "ro", label="Field data"
            )

        if field_width:
            lava_properties.axes[6].plot(
                field_distance_width, field_width, "ro", label="Field data"
            )

    return flow_length

def add_runout_line(figures, flow_length):

    for fig in figures:
        for ax in fig.axes:
            ax.axvline(x=flow_length,color="red",linestyle="--",label="Runout")

            # Remove any existing axis legend
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()

        # ------------------------------------------------------------
        # ONE legend only for the Lava Properties figure
        # ------------------------------------------------------------
        lava_properties = figures[0]

        handles = []
        labels = []

        for ax in lava_properties.axes:
            h, l = ax.get_legend_handles_labels()

            for handle, label in zip(h, l):
                if label not in labels and not label.startswith("_"):
                    handles.append(handle)
                    labels.append(label)
        lava_properties.subplots_adjust(right=0.84)
        lava_properties.legend( handles,labels,loc="center left",bbox_to_anchor=(0.85, 0.5),fontsize=8,frameon=True)

def select_width_field_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        width_field_var.set(file_path)

def run_flowgo_single():
    json_file = json_path_var.get()
    path_to_folder = results_folder_var.get()

    if not json_file or not path_to_folder:
        messagebox.showerror("Error", "Please select a JSON file and results folder")
        return

    try:
        single_effusion_rate = float(single_eff_rate_var.get())
    except ValueError:
        messagebox.showerror("Error", "Single effusion rate must be a numeric value.")
        return

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    with open(json_file, "r") as f:
        json_data = json.load(f)

    # GUI value has priority for Single Effusion.
    # The original JSON file is never modified.
    json_data["effusion_rate_init"] = single_effusion_rate

    json_dir = os.path.dirname(os.path.abspath(json_file))
    fd, temp_json_file = tempfile.mkstemp(
        prefix="_temp_single_flowgo_",
        suffix=".json",
        dir=json_dir
    )
    os.close(fd)

    try:
        with open(temp_json_file, "w") as f:
            json.dump(json_data, f, indent=4)

        print(f"Single effusion mode: using effusion_rate_init = {single_effusion_rate}")

        flowgo = run_flowgo.RunFlowgo()
        flowgo.run(temp_json_file, path_to_folder)

        filename_results = flowgo.get_file_name_results(
            path_to_folder,
            temp_json_file
        )
        filename_array = [filename_results]

        figures = plot_flowgo_results.plot_all_results(
            path_to_folder,
            filename_array,
            temp_json_file
        )

        lava_properties = figures[0]

        # Add field data and get observed runout
        flow_length = add_field_data(
            lava_properties,
            field_data_var.get()
        )

        # Add observed runout to ALL plots
        if flow_length is not None:
            add_runout_line(figures, flow_length)

        if field_data_var.get():
            lava_properties.savefig(
                os.path.join(path_to_folder, "lava_properties_with_field_data.png"),
                dpi=300,
                bbox_inches="tight"
            )

        plot_flowgo_results.plt.show()
        plot_flowgo_results.plt.close("all")

        messagebox.showinfo(
            "Success",
            f"FLOWGO simulation completed successfully at {single_effusion_rate:g} m3/s!"
        )

    finally:
        if os.path.exists(temp_json_file):
            os.remove(temp_json_file)


def run_flowgo_effusion():
    json_file = json_path_var.get()
    path_to_folder = results_folder_var.get()

    if not json_file or not path_to_folder:
        messagebox.showerror("Error", "Please select a JSON file and results folder")
        return

    try:
        effusion_rates = {
            "first_eff_rate": int(float(first_eff_rate_var.get())),
            "last_eff_rate": int(float(last_eff_rate_var.get())),
            "step_eff_rate": int(float(step_eff_rate_var.get()))
        }
    except ValueError:
        messagebox.showerror("Error", "Effusion rates must be numeric values.")
        return

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    with open(json_file, "r") as file:
        json_data = json.load(file)
        slope_file = json_data.get("slope_file")
        lava_name = json_data.get("lava_name")

    simulation = run_flowgo_effusion_rate_array.StartFlowgo()

    original_dir = os.getcwd()

    try:
        filename_results = simulation.run_flowgo_effusion_rate_array(
            json_file,
            path_to_folder,
            slope_file,
            effusion_rates
        )
    finally:
        os.chdir(original_dir)

    if not filename_results:
        messagebox.showwarning("Warning","No PyFLOWGO result CSV was generated.")
        return

    print("\nResult files:")
    for filename in filename_results:
        print("  -", os.path.basename(filename))

    # Plot ONLY the files generated by this run
    figures = plot_flowgo_results.plot_all_results(
        path_to_folder,
        filename_results,
        json_file
    )

    lava_properties = figures[0]

    # Add field observations exactly as in the webapp
    add_field_data(
        lava_properties,
        field_data_var.get()
    )

    # Add field data and get observed runout
    flow_length = add_field_data(
        lava_properties,
        field_data_var.get()
    )

    # Add observed runout to ALL plots
    if flow_length is not None:
        add_runout_line(figures, flow_length)

    if field_data_var.get():
        lava_properties.savefig(
            os.path.join(path_to_folder, "lava_properties_with_field_data.png"),
            dpi=300,
            bbox_inches="tight"
        )

    # Show every Matplotlib figure:
    # lava properties, heat fluxes, crustal conditions,
    # plus any effusion-rate/distance figure created by the array routine.
    plot_flowgo_results.plt.show()
    plot_flowgo_results.plt.close("all")

    messagebox.showinfo(
        "Success",
        "Effusion rate simulation completed successfully!"
    )


# Setup Tkinter window
root = tk.Tk()
root.title("FLOWGO Simulation GUI")
root.geometry("700x430")

json_path_var = tk.StringVar()
results_folder_var = tk.StringVar()
field_data_var = tk.StringVar()
width_field_var = tk.StringVar()
single_eff_rate_var = tk.StringVar(value="500")
first_eff_rate_var = tk.StringVar(value="5")
last_eff_rate_var = tk.StringVar(value="35")
step_eff_rate_var = tk.StringVar(value="5")

frame = tk.Frame(root)
frame.pack(pady=10)

# JSON file selection
tk.Label(frame, text="Select JSON File:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=json_path_var, width=40).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_json_file).grid(row=0, column=2)
tk.Button(frame, text="Edit Json", command=lambda: open_editor(root, json_path_var)).grid(row=0, column=3)
# Results folder selection
tk.Label(frame, text="Select Results Folder:").grid(row=1, column=0, sticky="w")
tk.Entry(frame, textvariable=results_folder_var, width=40).grid(row=1, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_results_folder).grid(row=1, column=2)

# Field data
tk.Label(frame, text="Field Data:").grid(row=2, column=0, sticky="w")
tk.Entry(frame, textvariable=field_data_var, width=40).grid(row=2, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_field_data_file).grid(row=2, column=2)


# Effusion rate input fields
tk.Label(frame, text="Single Effusion Rate:").grid(row=4, column=0, sticky="w")
tk.Entry(frame, textvariable=single_eff_rate_var, width=10).grid(row=4, column=1, sticky="w")

tk.Label(frame, text="First Effusion Rate:").grid(row=5, column=0, sticky="w")
tk.Entry(frame, textvariable=first_eff_rate_var, width=10).grid(row=5, column=1, sticky="w")

tk.Label(frame, text="Last Effusion Rate:").grid(row=6, column=0, sticky="w")
tk.Entry(frame, textvariable=last_eff_rate_var, width=10).grid(row=6, column=1, sticky="w")

tk.Label(frame, text="Step Effusion Rate:").grid(row=7, column=0, sticky="w")
tk.Entry(frame, textvariable=step_eff_rate_var, width=10).grid(row=7, column=1, sticky="w")


# Run FlowGo buttons
tk.Button(root, text="Run FlowGo (Single Effusion)", command=run_flowgo_single).pack(pady=5)
tk.Button(root, text="Run FlowGo (Effusion Rate Array)", command=run_flowgo_effusion).pack(pady=5)

root.mainloop()
