import openpyxl, os, datetime


def generate_schedule(file_name, file_data, occurence_in_days, future_iterations, cwd=None):

    # switch to cwd if passes as argument
    if cwd:
        if not os.path.isdir(cwd):
            os.mkdir(cwd)
        os.chdir(cwd)

    sheet_name = file_data["sheet_name"]
    tasks_col = file_data["tasks_col"]
    date_col = file_data["date_col"]

    # find all tasks and the last execution date
    wb = openpyxl.load_workbook(file_name)
    sheet = wb[sheet_name]

    all_tasks = {}
    max_row = sheet.max_row
    for i in range(2, max_row+1):  # skip header
        task = sheet.cell(row=i, column=tasks_col).value
        date = sheet.cell(row=i, column=date_col).value
        if task not in all_tasks.keys():  # record unique tasks
            all_tasks.setdefault(task, date)
        if date > all_tasks[task]:  # overwrite with most recent date
            all_tasks[task]= date

    # create new sheet and record all_tasks
    unique_tasks_sheet = "Tasks_and_last_execution_date" #TODO
    if unique_tasks_sheet not in wb.sheetnames:
        wb.create_sheet(unique_tasks_sheet)

    tasks_sheet = wb[unique_tasks_sheet]
    n = 1
    for value in all_tasks.keys():
        tasks_sheet[f"A{n}"] = value
        tasks_sheet[f"B{n}"] = all_tasks[value]
        n += 1

    wb.save(file_name)

    # calculate next execution day
    # TODO - include future_iterations
    for task, date in all_tasks.items():
        delta_days = datetime.timedelta(occurence_in_days)
        next_date = date + delta_days
        while next_date.weekday() in (0, 5, 6):  # do not schedule for Monday and weekend
                next_date += datetime.timedelta(1)
    # TODO record next_date
        print(next_date.weekday(), task, next_date)





working_directory = "D:\\Practice Python\\Tasks schedule generator"
file_name = "Tasks_schedule.xlsx"
file_data = {"sheet_name": "Schedule", "tasks_col": 1, "date_col": 2}
occurence_days = 90
future_iterations = 3

generate_schedule(file_name, file_data, occurence_days, future_iterations, working_directory)

