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
    sections = {}
    row = 0

    # --- Function to render JSON recursively ---
    def render_json(d, parent_key=None):
        nonlocal row
        for key, value in d.items():
            display_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, dict):
                # Section label
                section_label = tk.Label(scroll_frame, text=key, font=("Helvetica", 12, "bold"))
                section_label.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 0))

                # Track section start/end and dict reference
                sections[display_key] = {"row_start": row, "row_end": row, "dict_ref": value}

                row += 1
                render_json(value, display_key)
                sections[display_key]["row_end"] = row - 1

            else:
                key_label = tk.Label(scroll_frame, text=key)
                key_label.grid(row=row, column=0, sticky="w", padx=20, pady=2)

                entry = tk.Entry(scroll_frame, width=60)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=5, pady=2)

                labels[display_key] = entry

                if parent_key and parent_key in sections:
                    sections[parent_key]["row_end"] = row

                row += 1

    render_json(data)

    # --- Dropdown to select section ---
    button_frame = tk.Frame(editor_win)
    button_frame.pack(pady=10)

    section_var = tk.StringVar()
    section_keys = list(sections.keys())
    if section_keys:
        section_var.set(section_keys[0])
    section_menu = tk.OptionMenu(button_frame, section_var, *section_keys)
    section_menu.pack(pady=2)

    # --- Function to add a new entry to a section ---
    def add_new_entry_to_section():
        section_key = section_var.get()
        if not section_key:
            return

        section_info = sections[section_key]
        insert_row = section_info["row_end"] + 1

        # Shift widgets below the insert row
        for widget in scroll_frame.grid_slaves():
            r = int(widget.grid_info()["row"])
            if r >= insert_row:
                widget.grid(row=r + 1, column=int(widget.grid_info()["column"]))

        # Create new key/value entry
        key_entry = tk.Entry(scroll_frame, width=30)
        key_entry.grid(row=insert_row, column=0, padx=20, pady=2)
        value_entry = tk.Entry(scroll_frame, width=60)
        value_entry.grid(row=insert_row, column=1, padx=5, pady=2)

        temp_key = f"{section_key}.new_entry_{insert_row}"
        labels[temp_key] = (key_entry, value_entry)

        # Update section row_end and global row
        section_info["row_end"] += 1
        nonlocal row
        row += 1

        scroll_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    tk.Button(button_frame, text="Add Entry", width=12, command=add_new_entry_to_section).pack(pady=2)

    # --- Rebuild the JSON including new entries ---
    def rebuild_dict(data, parent_key=None):
        new_data = OrderedDict()
        for key, value in data.items():
            display_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                new_data[key] = rebuild_dict(value, display_key)
            else:
                entry_widget = labels.get(display_key)
                if entry_widget:
                    text = entry_widget.get()
                    try:
                        val = json.loads(text)
                    except:
                        val = text
                    new_data[key] = val

        # Handle new entries safely
        for temp_key, widget_pair in labels.items():
            if isinstance(widget_pair, tuple):  # this is a new entry
                key_text = widget_pair[0].get().strip()
                value_text = widget_pair[1].get().strip()
                if not key_text:
                    continue
                try:
                    val = json.loads(value_text)
                except:
                    val = value_text

                parent_section_key = temp_key.rsplit(".new_entry_", 1)[0]
                parent_dict = new_data
                found = True
                if parent_section_key:
                    for part in parent_section_key.split("."):
                        if part in parent_dict:
                            parent_dict = parent_dict[part]
                        else:
                            found = False
                            break

                if found and isinstance(parent_dict, dict):
                    parent_dict[key_text] = val
                # If parent not found, skip entry (optionally show a warning)

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
        new_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
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

    tk.Button(button_frame, text="Save", width=12, command=save_changes).pack(pady=2)
    tk.Button(button_frame, text="Save As", width=12, command=save_as).pack(pady=2)

    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
