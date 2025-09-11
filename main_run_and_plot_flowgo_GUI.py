import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pyflowgo.run_flowgo as run_flowgo
import pyflowgo.plot_flowgo_results as plot_flowgo_results
import pyflowgo.run_flowgo_effusion_rate_array as run_flowgo_effusion_rate_array
import json
from edit_json import open_editor  # import your function

def select_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        json_path_var.set(file_path)

def select_results_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        results_folder_var.set(folder_path)


def run_flowgo_single():
    json_file = json_path_var.get()
    path_to_folder = results_folder_var.get()

    if not json_file or not path_to_folder:
        messagebox.showerror("Error", "Please select a JSON file and results folder")
        return

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    flowgo = run_flowgo.RunFlowgo()
    flowgo.run(json_file, path_to_folder)

    filename_results = flowgo.get_file_name_results(path_to_folder, json_file)
    filename_array = [filename_results]

    plot_flowgo_results.plot_all_results(path_to_folder, filename_array, json_file)
    plot_flowgo_results.plt.show()
    plot_flowgo_results.plt.close()
    messagebox.showinfo("Success", "FLOWGO simulation completed successfully!")


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
        slope_file = json_data.get('slope_file')

    simulation = run_flowgo_effusion_rate_array.StartFlowgo()

    # Change folder temporarly to save in the right folder
    original_dir = os.getcwd()
    #os.chdir(path_to_folder)

    try:
        simulation.run_flowgo_effusion_rate_array(json_file, path_to_folder, slope_file, effusion_rates)
    finally:
        os.chdir(original_dir)

    plot_flowgo_results.plt.show()
    plot_flowgo_results.plt.close()
    messagebox.showinfo("Success", "Effusion rate simulation completed successfully!")


# Setup Tkinter window
root = tk.Tk()
root.title("FLOWGO Simulation GUI")
root.geometry("700x300")

json_path_var = tk.StringVar()
results_folder_var = tk.StringVar()
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

# Effusion rate input fields
tk.Label(frame, text="First Effusion Rate:").grid(row=2, column=0, sticky="w")
tk.Entry(frame, textvariable=first_eff_rate_var, width=10).grid(row=2, column=1, sticky="w")

tk.Label(frame, text="Last Effusion Rate:").grid(row=3, column=0, sticky="w")
tk.Entry(frame, textvariable=last_eff_rate_var, width=10).grid(row=3, column=1, sticky="w")

tk.Label(frame, text="Step Effusion Rate:").grid(row=4, column=0, sticky="w")
tk.Entry(frame, textvariable=step_eff_rate_var, width=10).grid(row=4, column=1, sticky="w")

# Run FlowGo buttons
tk.Button(root, text="Run FlowGo (Single Effusion)", command=run_flowgo_single).pack(pady=5)
tk.Button(root, text="Run FlowGo (Effusion Rate Array)", command=run_flowgo_effusion).pack(pady=5)

root.mainloop()
