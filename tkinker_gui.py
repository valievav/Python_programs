from tkinter import Tk, Label, Button, Entry, StringVar, filedialog
import sys


window = Tk()
window.title("Input parameters")
window.minsize(500, 200)

ENTRY_TYPE = "Entry"
FILE_TYPE = "Filedialog"
params = [["File Keyword", "Entry", "file"],
          ["Search keywords", "Entry", "Castle, Final Fantasy"],
          ["Sheet Name", "Entry", "sheet"],
          ["Working directory", "Filedialog", "D:\\PYTHON Practice"],
          ["Exclusion folder name", "Entry", "Top Secret"]]


def click_folder_path():
    select_directory = filedialog.askdirectory()
    button.configure(text=select_directory)  # TODO getting global button param??


def click_submit():
    pass


# build 2-column grid with params label-input
for i in range(len(params)):
    param_name = params[i][0]
    param_input_type = params[i][1]
    param_default_value = params[i][2]

    # insert labels in the 1st column
    label = Label(window, text=param_name)
    label.grid(row=i, sticky='E')

    # insert input in the 2nd column
    if param_input_type == ENTRY_TYPE:
        default_value = StringVar(window, value=param_default_value)
        entry = Entry(window, width=50, textvariable=default_value)
        entry.grid(row=i, column=1)
    elif param_input_type == FILE_TYPE:
        button = Button(window, text="Select PATH", command=click_folder_path, width=42)   # TODO if path too long - truncate and display part
        button.grid(row=i, column=1, sticky='W')
    else:
        print(f"Unexpected input type '{param_input_type}' for parameter '{param_name}'. "
              f"Accepted only {ENTRY_TYPE}, {FILE_TYPE}.")
        sys.exit()

submit_button = Button(window, text="SUBMIT", width=10, command=click_submit)
submit_button.grid(row=10, column=1)


window.mainloop()

