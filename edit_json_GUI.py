import tkinter as tk
from tkinter import filedialog, messagebox
import os
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


# Setup Tkinter window
root = tk.Tk()
root.title("Edit JSON")
root.geometry("700x200")

json_path_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=10)

# JSON file selection
tk.Label(frame, text="Select JSON File:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=json_path_var, width=40).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Browse", command=select_json_file).grid(row=0, column=2)
tk.Button(frame, text="Edit Json", command=lambda: open_editor(root, json_path_var)).grid(row=0, column=3)


root.mainloop()
