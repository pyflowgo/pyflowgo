import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from collections import OrderedDict
def open_editor(root, json_path_var):
    file_path = json_path_var.get()
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "No valid JSON file selected.")
        return

    try:
        with open(file_path, "r") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON: {e}")
        return

    editor_win = tk.Toplevel(root)
    editor_win.title("Edit JSON")
    editor_win.geometry("700x700")

    canvas = tk.Canvas(editor_win)
    scrollbar = tk.Scrollbar(editor_win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    labels = {}
    row = 0

    def render_json(d, parent_key=None):
        nonlocal row
        for key, value in d.items():
            display_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                section_label = tk.Label(scroll_frame, text=key, font=("Helvetica", 12, "bold"))
                section_label.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 0))
                row += 1
                render_json(value, key)
            else:
                key_label = tk.Label(scroll_frame, text=key)
                key_label.grid(row=row, column=0, sticky="w", padx=20, pady=2)

                entry = tk.Entry(scroll_frame, width=60)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=5, pady=2)

                labels[display_key] = entry
                row += 1

    render_json(data)

    def rebuild_dict(data, parent_key=None):
        new_data = OrderedDict()
        for key, value in data.items():
            display_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                new_data[key] = rebuild_dict(value, key)
            else:
                entry_widget = labels.get(display_key)
                if entry_widget:
                    text = entry_widget.get()
                    try:
                        val = json.loads(text)
                    except:
                        val = text
                    new_data[key] = val
        return new_data

    def save_changes():
        try:
            new_data = rebuild_dict(data)
            with open(file_path, "w") as f:
                json.dump(new_data, f, indent=4)
            messagebox.showinfo("Success", "JSON saved successfully.")
            editor_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON: {e}")

    def save_as():
        new_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if new_path:
            try:
                new_data = rebuild_dict(data)
                with open(new_path, "w") as f:
                    json.dump(new_data, f, indent=4)
                json_path_var.set(new_path)
                messagebox.showinfo("Success", "JSON saved successfully.")
                editor_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save JSON: {e}")

    button_frame = tk.Frame(editor_win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Save", width=12, command=save_changes).pack(pady=2)
    tk.Button(button_frame, text="Save As", width=12, command=save_as).pack(pady=2)

    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
