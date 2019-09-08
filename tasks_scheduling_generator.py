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

    # (re)create new sheet for results
    sheet_name = "Tasks_and_execution_dates"
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
        print(f"Removed previous '{sheet_name}' sheet in '{file_name}")

    wb.create_sheet(sheet_name)
    print(f"Created new sheet '{sheet_name}' in '{file_name}'")
    result_sheet = wb[sheet_name]

    # record headers
    headers = ["Tasks", "Last date", "Next date"]
    column = 0
    for column in range(1, len(headers)+1):
        result_sheet[f"{get_column_letter(column)}1"] = headers[column-1]
        column += 1
    iterations_delta = iterations_number - 1
    if iterations_delta != 0:
        for iteration in range(1, iterations_delta+1):
            result_sheet[f"{get_column_letter(column)}1"] = headers[-1]
            column += 1

    # record all tasks with dates in new sheet
    row = 2
    for task in all_tasks.keys():
        result_sheet[f"A{row}"] = task
        for i in range(1, len(all_tasks[task])+1):
            date_cell = result_sheet[f"{get_column_letter(i+1)}{row}"]
            date_cell.value = all_tasks[task][i-1]  # record value
            date_cell.number_format = "MM/DD/YYYY"  # set date format

        row += 1

    # set column width
    tasks_max_len = max(len(task) for task in all_tasks.keys())*1.5  # 1.5 - coefficient for extra space
    date_max_len = max(len(str(date)) for dates in all_tasks.values() for date in dates)  # list comprehension with nested loop
    result_sheet.column_dimensions["A"].width = tasks_max_len
    for i in range(2, iterations_number+3):
        result_sheet.column_dimensions[get_column_letter(i)].width = date_max_len

    print(f"Recorded results into '{sheet_name}' sheet")
    wb.save(file_name)


working_directory = r"D:\Practice Python\Tasks schedule generator"
file_name = "Tasks_schedule.xlsx"
file_data = {"sheet_name": "Schedule", "tasks_col": 1, "date_col": 2}
iterations_gap = datetime.timedelta(90)
iterations_number = 4

generate_schedule(file_name, file_data, iterations_gap, iterations_number, working_directory)

