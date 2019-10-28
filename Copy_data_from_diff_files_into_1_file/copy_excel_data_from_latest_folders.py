import datetime
import logging
import os
import re

import openpyxl
import send2trash


def find_most_recent_folders(cwd: str, exclude_folders: list):

    def exclude_folder_from_processing(current_folder: str, folders_to_exclude: list):

        exclude = False
        for folder in folders_to_exclude:
            if folder.lower() in [folder.lower() for folder in current_folder.split(os.sep)]:
                print(f"Skipping  path '{os.path.join(current_folder)}' because of the excluded folder '{folder}'")
                exclude = True
        return exclude

    def find_most_recent_folder(folders: list):

        most_recent_folder = []
        for folder in (_ for _ in folders):  # folders generator
            regex_match = re.match(r"^\d{6}", folder)
            if not regex_match:
                continue
            folder_date = datetime.datetime.strptime(regex_match.group(), "%Y%m")

            if not most_recent_folder:  # populate if empty
                most_recent_folder = [folder_date, folder]
            elif folder_date > most_recent_folder[0]:  # populate if date is most recent
                most_recent_folder = [folder_date, folder]
            elif folder_date == most_recent_folder[0]:
                pass  # TODO - check if same max date - add redelivery logic

        if most_recent_folder:
            most_recent_date = most_recent_folder[0]
            most_recent_folder = most_recent_folder[1]
            return most_recent_date, most_recent_folder
        else:
            return None, None

    # iterate through subfolders and files
    most_recent_folders = []
    for active_folder, subfolders, files in os.walk(cwd):

        if exclude_folder_from_processing(active_folder, exclude_folders):
            continue
        most_recent_date, most_recent_subfolder = find_most_recent_folder(subfolders)

        if most_recent_date and most_recent_subfolder:
            most_recent_folder_path = os.path.join(active_folder, most_recent_subfolder)  # TODO relative path?
            most_recent_folders.append(most_recent_folder_path)
            print(f"    MOST RECENT DATE FOLDER for '{active_folder}' -> {most_recent_date}")
    return most_recent_folders


def find_files_and_copy_data(target_folders: list, file_keywords: list, sheet_keywords: list,
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
            print(f"OLD RESULT FILE '{result_file_abs_path} moved to trash")

        try:
            result_file_wb = openpyxl.load_workbook(result_file_abs_path)
        except FileNotFoundError:
            result_file_wb = openpyxl.Workbook()
            print("Created new result file")

        # create sheet if not exists
        if sheet_name not in result_file_wb.sheetnames:
            result_file_wb.create_sheet(sheet_name, 0)
            print(f"Created new sheet - '{sheet_name}'")
        result_file_sheet = result_file_wb[sheet_name]

        # record data
        data_origin = [f"Data file path {from_file_abs_path}"]
        result_file_sheet.append(data_origin)   # append works only with iterables
        [result_file_sheet.append(row) for row in data_to_record]
        empty_row = [""]
        result_file_sheet.append(empty_row)
        print(f"    RECORDED DATA from file '{from_file_abs_path}' to sheet '{sheet_name}'")

        result_file_wb.save(result_file_abs_path)

    # iterate through target folders to find matched file, sheet and copy data
    for target_folder in (_ for _ in target_folders):  # target_folders generator
        for active_folder, subfolders, files in os.walk(target_folder):
            for file in (_ for _ in files):  # files generator

                # match file
                matched_file = keyword_match(elems=file, keywords=file_keywords)
                if matched_file:
                    abs_path = os.path.join(active_folder, file)
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

    destination_path = r"D:\PYTHON Practice\Consolidate function folder - result"
    destination_file_name = "Consolidation results.xlsx"

    logging.basicConfig(level=logging.CRITICAL)

    print("Process started...")
    start = datetime.datetime.now()
    most_recent_folders = find_most_recent_folders(cwd=init_path,
                                                   exclude_folders=skip_folders,)
    find_files_and_copy_data(target_folders=most_recent_folders,
                             file_keywords=file_name_keywords,
                             sheet_keywords=sheet_name_keywords,
                             result_path=destination_path,
                             result_file_name=destination_file_name,)

    finish = datetime.datetime.now()
    print(f"Process finished. Time spent {finish - start}")

