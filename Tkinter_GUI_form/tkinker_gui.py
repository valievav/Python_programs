from tkinter import Tk, Label, Button, Entry, StringVar, filedialog
import sys
import os
import itertools


def get_user_parameters_with_gui(params_input: dict):
    """
    Creates tkinter GUI window with parameters and default values. \n
    After user entered new parameters and hit 'Submit' button, it collects all values and returns params_output dict.\n
    :param params_input: dict
    :return: params_output dict
    """

    def click_folder_path(param_name: str):
        """
        Opens directory window and sets selected path to button_output dict.
        :param param_name: str
        :return:
        """
        default_dir = params_input[param_name][1]
        new_dir_name = filedialog.askdirectory(initialdir=default_dir if os.path.isdir(default_dir) else os.getcwd())

        # change button output if already provided (user re-selects path) or set a new value
        button_output[param_name] = new_dir_name if param_name in button_output.keys() else button_output.setdefault(param_name, new_dir_name)

    def get_gui_info():
        """
        Fetches all parameters outputs from user (for labels & buttons)
        :return:
        """

        for param_name, (param_input_type, param_default_value, elem_object) in params_input.items():
            if param_input_type == param_types['ENTRY_TYPE']:
                params_output.setdefault(param_name, elem_object.get().strip())
            elif param_input_type == param_types['FILE_TYPE']:

                # use new value if directory button was changed, else - use default
                if param_name in button_output.keys():
                    params_output.setdefault(param_name, button_output[param_name])
                else:
                    params_output.setdefault(param_name, param_default_value)

        window.destroy()

    # create tkinter window
    window = Tk()
    window.title("Input parameters")
    window.minsize(450, 100)

    param_types = {"ENTRY_TYPE": 0, "FILE_TYPE": 1}
    params_output = {}
    button_output = {}

    # build 2-column grid with label-input layout
    grid_row = itertools.count()

    for param_name, (param_input_type, param_default_value) in params_input.items():
        row = next(grid_row)

        # insert labels in the 1st column
        label = Label(window, text=param_name)
        label.grid(row=row, sticky='E', padx=5)

        # insert inputs in the 2nd column
        value = StringVar()
        value.set(param_default_value)

        if param_input_type == param_types['ENTRY_TYPE']:
            elem = Entry(window, width=50, textvariable=value)
        elif param_input_type == param_types['FILE_TYPE']:
            elem = Button(window, text="Select PATH", command=lambda param_name=param_name: click_folder_path(param_name), width=42, anchor="w")
        else:
            print(f"Unexpected input type '{param_input_type}' for parameter '{param_name}'. "
                  f"Accepted only {param_types['ENTRY_TYPE']}, {param_types['FILE_TYPE']}.")
            sys.exit()

        elem.grid(row=row, column=1, sticky='W', padx=10)
        params_input[param_name].append(elem)

    # collect user output for params
    submit_button = Button(window, text="SUBMIT", width=10, command=lambda: get_gui_info())
    submit_button.grid(row=len(params_input), column=1, sticky='E', pady=20, padx=10)

    window.mainloop()
    return params_output


def main():
    params_input = {"File Keyword": [0, "file"],
                    "Search keywords": [0, "Castle, Final Fantasy"],
                    "Sheet Name": [0, "sheet"],
                    "Working directory": [1, "D:\PYTHON Practice"],
                    "Exclusion folder name": [0, "Top Secret"],
                    }

    params_output = get_user_parameters_with_gui(params_input)

    if not bool(params_output):  # is values submission was cancelled (Exit button)
        print("Parameter values are empty. Exiting the program.")
    else:
        print(f"Param OUTPUT - {params_output}")


if __name__ == "__main__":
    main()

