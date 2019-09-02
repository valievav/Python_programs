import openpyxl, os, datetime
from openpyxl.utils.cell import get_column_letter


def generate_schedule(file_name, file_data, iterations_gap, iterations_number, cwd=None):

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
            all_tasks.setdefault(task, [date])
        if date > all_tasks[task][0]:  # overwrite with most recent date
            all_tasks[task] = [date]

    # calculate the next execution day
    for task in all_tasks.keys():
        for i in range(iterations_number):
            date = all_tasks[task][i]
            next_date = date + iterations_gap
            while next_date.weekday() in (0, 5, 6):  # do not schedule for Monday and weekend
                next_date += datetime.timedelta(1)
            all_tasks[task].append(next_date)

    # create new sheet for results
    sheet_name = "Tasks_and_execution_dates"
    if sheet_name not in wb.sheetnames:
        wb.create_sheet(sheet_name)
        print(f"Created new sheet '{sheet_name}' in '{file_name}'")
    result_sheet = wb[sheet_name]

    # record all tasks in new sheet
    n = 1
    for task in all_tasks.keys():
        result_sheet[f"A{n}"] = task
        for i in range(1, len(all_tasks[task])+1):
            result_sheet[f"{get_column_letter(i+1)}{n}"] = all_tasks[task][i-1]
        n += 1
    print(f"Recorded results into '{sheet_name}' sheet")
    wb.save(file_name)


working_directory = "D:\\Practice Python\\Tasks schedule generator"
file_name = "Tasks_schedule.xlsx"
file_data = {"sheet_name": "Schedule", "tasks_col": 1, "date_col": 2}
iterations_gap = datetime.timedelta(90)
iterations_number = 2

generate_schedule(file_name, file_data, iterations_gap, iterations_number, working_directory)

