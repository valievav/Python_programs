from tkinter import Tk, Label, Button, Entry, StringVar, filedialog
import sys
import os
import itertools


def click_folder_path(param_name):
    dir_name = filedialog.askdirectory(initialdir=param_default_value if os.path.isdir(param_default_value) else os.getcwd())
    button_changed_output[param_name] = dir_name if param_name in button_changed_output.keys() else button_changed_output.setdefault(param_name, dir_name)


def get_gui_info():

    for param_name, (param_input_type, param_default_value, elem_object) in params_input.items():

        if param_input_type == ENTRY_TYPE:
            params_output.setdefault(param_name, elem_object.get().strip())
        elif param_input_type == FILE_TYPE:
            if param_name in button_changed_output.keys():  # if file button was changed
                params_output.setdefault(param_name, button_changed_output[param_name])
            else:  #if it stayed default
                params_output.setdefault(param_name, param_default_value)

    print(f"Param OUTPUT - {params_output}, {button_changed_output}\n")
    window.destroy()


params_input = {"File Keyword": [0, "file"],
                "Search keywords": [0, "Castle, Final Fantasy"],
                "Sheet Name": [0, "sheet"],
                "Working directory": [1, "D:\PYTHON Practice"],
                "Exclusion folder name": [0, "Top Secret"],
                }

# create window
window = Tk()
window.title("Input parameters")
window.minsize(450, 100)

ENTRY_TYPE = 0
FILE_TYPE = 1

params_output = {}
button_changed_output = {}

# build 3-column grid with label-input-button
grid_row = itertools.count()

for param_name, (param_input_type, param_default_value) in params_input.items():
    row = next(grid_row)

    # insert labels in the 1st column
    label = Label(window, text=param_name)
    label.grid(row=row, sticky='E', padx=5)

    value = StringVar()
    value_default = value.set(param_default_value)

    # insert inputs in the 2nd column
    if param_input_type == ENTRY_TYPE:
        elem = Entry(window, width=50, textvariable=value)

    elif param_input_type == FILE_TYPE:
        elem = Button(window, text="Select PATH", command=lambda param_name=param_name: click_folder_path(param_name), width=42, anchor="w")
    else:
        print(f"Unexpected input type '{param_input_type}' for parameter '{param_name}'. "
              f"Accepted only {ENTRY_TYPE}, {FILE_TYPE}.")
        sys.exit()

    elem.grid(row=row, column=1, sticky='W', padx=10)
    params_input[param_name].append(elem)


# collect all parameters when pressed submit button
submit_button = Button(window, text="SUBMIT", width=10, command=get_gui_info)
submit_button.grid(row=len(params_input), column=1, sticky='E', pady=20, padx=10)

window.mainloop()

