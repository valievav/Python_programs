import datetime
import os
import re

import openpyxl
import send2trash


# TODO desc to the functions

def find_most_recent_folders(cwd: str, exclude_folders: list, same_date_priority_keyword: str):

    def exclude_folder_from_processing(current_folder: str, folders_to_exclude: list):

        exclude = False
        for folder in folders_to_exclude:
            if folder.lower() in [folder.lower() for folder in current_folder.split(os.sep)]:
                print(f"SKIPPING  path '{os.path.join(current_folder)}' because of the excluded folder '{folder}'")
                exclude = True
        return exclude

    def record_most_recent_folder(folders: list):

        def check_yyyymm_format(year_month: str, folder: str):
            year = int(year_month[:4])
            month = int(year_month[4:])
            if 0 == month > 12:
                print(f"DATE PARSING ERROR: actual YEAR - '{year}'', expected YEAR in range (2010-now). "
                      f"Skipping folder {folder}.")
                return False
            elif 2010 <= year > datetime.datetime.today().year:
                print(f"DATE PARSING ERROR: actual MONTH - '{month}'', expected MONTH in range (1-12)."
                      f"Skipping folder {folder}.")
                return False
            else:
                return True

        most_recent_folder = []
        for folder in (_ for _ in folders):  # folders generator

            # find YYYYMM match
            regex_match = re.match(r"^\d{6}", folder)
            if not regex_match:
                continue
            year_month = regex_match.group()
            yyyymm_match = check_yyyymm_format(year_month, folder)
            if not yyyymm_match:
                continue
            folder_date = datetime.datetime.strptime(year_month, "%Y%m").date()

            # determine most recent folder
            if not most_recent_folder or folder_date > most_recent_folder[0]:  # if empty or > than existing
                most_recent_folder = [folder_date, folder]
            elif folder_date == most_recent_folder[0]:  # if has the keyword for folders with the same date
                print(f"Detected folders with the same date - '{folder_date}'. "
                      f"Previous folder '{most_recent_folder[1]}', current folder '{folder}'")

                if same_date_priority_keyword in folder:
                    most_recent_folder = [folder_date, folder]
                    print(f"Found priority keyword '{same_date_priority_keyword}' in folder '{folder}'")
        return most_recent_folder

    # iterate through subfolders and files
    os.chdir(cwd)
    most_recent_folders_data = []
    for active_folder, subfolders, files in os.walk('.'):

        if exclude_folder_from_processing(active_folder, exclude_folders):
            continue

        most_recent_folder_data = record_most_recent_folder(subfolders)
        if most_recent_folder_data:
            most_recent_date = most_recent_folder_data[0]
            most_recent_folder = most_recent_folder_data[1]

            most_recent_folder_rel_path = os.path.relpath(os.path.join(active_folder, most_recent_folder), cwd)
            most_recent_folders_data.append(most_recent_folder_rel_path)
            print(f"    FOLDER '{active_folder}' -> recorded most recent DATE - '{most_recent_date}', "
                  f"most recent FOLDER NAME - '{most_recent_folder}'")
            print(f"COMPLETE SUBFOLDERS list - {subfolders}")
    return most_recent_folders_data


def find_files_and_copy_data(cwd: str, target_folders: list, file_keywords: list, sheet_keywords: list,
                             result_path: str, result_file_name: str, recreate_result_file=True):

    def keyword_match(elems, keywords: list):

        matches = {}
        if isinstance(elems, str):
            elems = [elems]  # list with 1 element - for file match case

        for keyword in keywords:
            for elem in elems:
                if keyword in elem:
                    matches.setdefault(keyword, elem)
        return matches

    def record_data_to_sheet(result_file_abs_path: str, from_file_abs_path: str,
                             sheet_name: str, data_to_record: iter):

        # remove old file only on the start of the program
        if recreate_result_file and os.path.isfile(result_file_abs_path):
            send2trash.send2trash(result_file_abs_path)
            print(f"MOVED TO TRASH old result file '{result_file_abs_path}'")

        try:
            result_file_wb = openpyxl.load_workbook(result_file_abs_path)
        except FileNotFoundError:
            result_file_wb = openpyxl.Workbook()
            print(f"CREATED new result file")

        # create sheet if not exists
        if sheet_name not in result_file_wb.sheetnames:
            result_file_wb.create_sheet(sheet_name, 0)
            print(f"CREATED new sheet - '{sheet_name}'")
        result_file_sheet = result_file_wb[sheet_name]

        # record data
        data_origin = (f"DATA SOURCE ->   {from_file_abs_path}",)  # casted to tuple for further concatenation
        for row in data_to_record:
            record_line = data_origin + row
            result_file_sheet.append(record_line)  # append works only with iterables
        result_file_sheet.append([""])  # empty row to separate the data from different files
        print(f"    RECORDED data from FILE '{from_file_abs_path}' to SHEET '{sheet_name}'")

        result_file_wb.save(result_file_abs_path)

    # iterate through target folders to find matched file, sheet and copy data
    os.chdir(cwd)
    for target_folder in (_ for _ in target_folders):  # target_folders generator
        for active_folder, subfolders, files in os.walk(target_folder):
            for file in (_ for _ in files):  # files generator

                # match file
                matched_file = keyword_match(elems=file, keywords=file_keywords)
                if matched_file:
                    abs_path = os.path.join(os.getcwd(), active_folder, file)
                    wb = openpyxl.load_workbook(abs_path, read_only=True)

                    # match sheets
                    sheets = wb.sheetnames
                    matched_sheets = keyword_match(elems=sheets, keywords=sheet_keywords)

                    for matched_keyword, matched_sheet in matched_sheets.items():

                        # read data from sheet
                        active_sheet = wb[matched_sheet]
                        row_data = active_sheet.values

                        # record data to result file sheet
                        file_abs_path = os.path.join(result_path, result_file_name)
                        record_data_to_sheet(result_file_abs_path=file_abs_path, from_file_abs_path=abs_path,
                                             sheet_name=matched_keyword, data_to_record=row_data)
                        recreate_result_file = False  # no dot recreate file (add data from processed files)


if __name__ == "__main__":
    init_path = r"D:\PYTHON Practice\Consolidate function folder"
    file_name_keywords = ["data"]
    sheet_name_keywords = ["detailed", "general"]
    skip_folders = ["Skipper"]
    priority_keyword = "redeliver"

    destination_path = r"D:\PYTHON Practice\Consolidate function folder - result"
    destination_file_name = "Consolidation results.xlsx"

    print("Process started...")
    start = datetime.datetime.now()
    most_recent_folders = find_most_recent_folders(cwd=init_path,
                                                   exclude_folders=skip_folders,
                                                   same_date_priority_keyword=priority_keyword,)
    find_files_and_copy_data(cwd=init_path,
                             target_folders=most_recent_folders,
                             file_keywords=file_name_keywords,
                             sheet_keywords=sheet_name_keywords,
                             result_path=destination_path,
                             result_file_name=destination_file_name,)

    finish = datetime.datetime.now()
    print(f"Process finished. Time spent {finish - start}")

