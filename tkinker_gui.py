from tkinter import Tk, Label, Button, Entry, StringVar, filedialog
import sys


def click_folder_path():
    select_directory = filedialog.askdirectory()
    # display selected path as button text (truncate if too long)
    button["text"] = select_directory if len(select_directory) < button["width"] \
        else select_directory[:button["width"]-3]+'...'  # TODO getting global button param??


def click_submit():
    pass


ENTRY_TYPE = "Entry"
FILE_TYPE = "Filedialog"
params = [["File Keyword", ENTRY_TYPE, "file"],
          ["Search keywords", ENTRY_TYPE, "Castle, Final Fantasy"],
          ["Sheet Name", ENTRY_TYPE, "sheet"],
          ["Working directory", FILE_TYPE, "D:\\PYTHON Practice"],
          ["Exclusion folder name", ENTRY_TYPE, "Top Secret"],
          ]

# create window
window = Tk()
window.title("Input parameters")
window.minsize(450, 100)

# build 2-column grid with label-input
for i in range(len(params)):
    param_name = params[i][0]
    param_input_type = params[i][1]
    param_default_value = params[i][2]

    # insert labels in the 1st column
    label = Label(window, text=param_name)
    label.grid(row=i, sticky='E', padx=5)

    # insert inputs in the 2nd column
    if param_input_type == ENTRY_TYPE:
        default_value = StringVar(window, value=param_default_value)
        entry = Entry(window, width=50, textvariable=default_value)
        entry.grid(row=i, column=1, sticky='W', padx=10)
    elif param_input_type == FILE_TYPE:
        button = Button(window, text="Select PATH", command=click_folder_path, width=42, anchor="w")
        button.grid(row=i, column=1, sticky='W', padx=10)
    else:
        print(f"Unexpected input type '{param_input_type}' for parameter '{param_name}'. "
              f"Accepted only {ENTRY_TYPE}, {FILE_TYPE}.")
        sys.exit()

submit_button = Button(window, text="SUBMIT", width=10, command=click_submit)
submit_button.grid(row=len(params), column=1, sticky='E', pady=20, padx=10)

window.mainloop()

