from tkinter import Tk, Label, Button, Entry, StringVar

window = Tk()
window.title("Input parameters")
window.minsize(400, 200)

params = [["File Keyword", "Entry", "file"],
          ["Search keywords", "Entry", "Castle, Final Fantasy"],
          ["Sheet Name", "Entry", "sheet"],
          ["Working directory", "Filedialog", "D:\\PYTHON Practice"],
          ["Exclusion folder name", "Entry", "Top Secret"]]

# build 2-column layout with params labels-values
for i in range(len(params)):
    filed_type = params[i][1]
    if filed_type == "Entry":
        label = Label(window, text=params[i][0])
        default_value = StringVar(window, value=params[i][2])
        entry = Entry(window, textvariable=default_value)
        label.grid(row=i)
        entry.grid(row=i, column=1)
    elif filed_type == "Filedialog":
        pass  # TODO add file directory button
    else:
        print("Unexpected type")
        break

window.mainloop()