import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import json

class JsonEditorApp:
    def __init__(self, root):
        self.root = root
        self.json_file_path = tk.StringVar(value=None)
        self.labels = {}
        self.rows = 5
        self.canvas= None

        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        open_button = tk.Button(frame, text="Open JSON File", command=self.open_json_file)
        open_button.grid(row=0, column=0, padx=10, pady=10)

        self.save_button = tk.Button(frame, text="Save JSON File", command=self.save_json_file, state=tk.DISABLED)
        self.save_button.grid(row=0, column=1, padx=10, pady=10)

        self.load_button = tk.Button(frame, text="Load JSON File", command=self.load_json_data, state=tk.DISABLED)
        self.load_button.grid(row=0, column=2, padx=10, pady=10)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def open_json_file(self):
        self.canvas.delete("all")
        self.canvas_frame.update_idletasks()

        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

                for key, value in data.items():
                    if key in ["lava_name", "slope_file", "step_size", "effusion_rate_init"]:
                        label = tk.Label(self.canvas, text=key)
                        self.canvas.create_window(10, self.rows, anchor="w", window=label)
                        if isinstance(value, (int, float)):
                            entry_var = tk.DoubleVar()
                            entry_var.set(value)
                            entry = tk.Entry(self.canvas, textvariable=entry_var, width=20)
                        else:
                            entry = tk.Entry(self.canvas, width=20)
                            entry.insert(0, value)
                        self.canvas.create_window(200, self.rows, anchor="w", window=entry)
                        self.labels[key] = entry
                        self.rows += 25
                    elif key == "slope_smoothing_active":
                        label = tk.Label(self.canvas, text=key)
                        self.canvas.create_window(10, self.rows, anchor="w", window=label)
                        entry_var = tk.BooleanVar(value=value)
                        entry = tk.Checkbutton(self.canvas, variable=entry_var)
                        self.canvas.create_window(200, self.rows, anchor="w", window=entry)
                        self.labels[key] = entry
                        self.rows += 25
                    else:
                        label = tk.Label(self.canvas, text=key, font=("Helvetica", 12, "bold"))
                        self.canvas.create_window(10, self.rows, anchor="w", window=label)
                        self.rows += 25
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                label = tk.Label(self.canvas, text=subkey)
                                self.canvas.create_window(10, self.rows, anchor="w", window=label)
                                if isinstance(subvalue, (int, float)):
                                    entry_var = tk.DoubleVar()
                                    entry_var.set(subvalue)
                                    entry = tk.Entry(self.canvas, textvariable=entry_var, width=20)
                                else:
                                    entry = tk.Entry(self.canvas, width=20)
                                    entry.insert(0, subvalue)
                                self.canvas.create_window(200, self.rows, anchor="w", window=entry)
                                self.labels[(key, subkey)] = entry
                                self.rows += 25
                        else:
                            label = tk.Label(self.canvas, text=str(value))
                            self.canvas.create_window(10, self.rows, anchor="w", window=label)
                            self.rows += 25

                self.canvas.config(scrollregion=self.canvas.bbox("all"))
                self.save_button.config(state=tk.NORMAL)
                self.load_button.config(state=tk.NORMAL)
            self.json_file_path.set(file_path)

    def save_json_file(self):
        new_data = {}

        for key, entry in self.labels.items():
            if key in ["lava_name", "slope_file", "step_size", "effusion_rate_init"]:
                new_data[key] = entry.get()
            elif isinstance(entry, tk.Entry):
                section, subkey = key
                if section not in new_data:
                    new_data[section] = {}
                if subkey == "slope_smoothing_active":
                    new_data[section][subkey] = entry.get() == "true"
                else:
                    try:
                        new_data[section][subkey] = float(entry.get())
                    except ValueError:
                        new_data[section][subkey] = entry.get()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as json_file:
                json.dump(new_data, json_file, indent=4)

            print("JSON File saved as:", file_path)

        self.json_file_path.set(file_path)

    def load_json_data(self):
        file_path = self.json_file_path.get()
        if file_path:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                print("JSON File is:", file_path)
                print("JSON File is:", file_path)
                return file_path
        else:
            return None


if __name__ == "__main__":
    app = tk.Tk()
    app.title("JSON Editor")
    editor = JsonEditorApp(app)
    app.mainloop()
