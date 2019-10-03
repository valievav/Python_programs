import os
import openpyxl
import logging


def find_files_with_keyword_values(cell_keywords, cwd=None, exclusion_folder=None, file_name_keyword="", search_sheet=None):
    """
    Finds excel files that contain certain keyword values.\n
    It iterates through all files from the specified directory including subfolders.\n
    It can run search in all files as well as in file with specific keyword in file name.
    It can also search values in all spreadsheets as well as in specific spreadsheet.\n
    :param cell_keywords: list
    :param cwd: absolute path, optional
    :param exclusion_folder: str, optional
    :param file_name_keyword: str, optional (if not passed, function processes all excel files)
    :param search_sheet: str, optional (if not passed, function processes all worksheets)
    :return:
    """

    def search_keyword_in_file(wb, sheet_name, cell_keywords, abs_path):

        for cell_keyword in cell_keywords:
            for row in wb[sheet_name].values:
                for cell in row:
                    if cell_keyword.lower() in str(cell).lower():
                        print(f"    >>> Found keyword '{cell_keyword}': cell value '{cell}', sheet '{sheet_name}', file '{abs_path}'")

    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

    # switch to cwd if passed as param
    if cwd:
        os.chdir(cwd)
    
    # walk the directory tree
    print("Process started...")
    for active_folder, subfolders, files in os.walk('.'):

        # skip exclusion folder from search if passed as param
        if exclusion_folder:
            if exclusion_folder in active_folder.split(os.sep):
                print(f"Excluded '{active_folder}' from search as it contains exclusion folder '{exclusion_folder}'")
                continue

        for file in files:
            file_path = os.path.join(active_folder, file)
            abs_path = os.path.abspath(file_path)  # get abs path to open file

            # search for excel files only
            if file.endswith('xlsx'):
                logging.debug(f"Processing {abs_path} ...")

                # search for files with keyword in name
                if file_name_keyword.lower() in file.lower():

                    # open file
                    try:
                        wb = openpyxl.load_workbook(abs_path)
                    except FileNotFoundError as err:
                        print(f"{err} for file '{file}'")
                    else:

                        # search keyword in excel values for specific sheet or for all sheets
                        if search_sheet:
                            if search_sheet in wb.sheetnames:
                                search_keyword_in_file(wb, search_sheet, cell_keywords, abs_path)
                        else:
                            for active_sheet in wb.sheetnames:
                                search_keyword_in_file(wb, active_sheet, cell_keywords, abs_path)

    print("Process finished.")


if __name__ == "__main__":
    file_keyword = "file"
    search_keywords = ["Castlevania", "Final Fantasy"]
    sheet_name = "Sheet1"
    working_directory = "D:\\Practice Python"
    exclusion_folder_name = "Top Secret"

    logging.disable(logging.DEBUG)
    find_files_with_keyword_values(search_keywords, cwd=working_directory, exclusion_folder=exclusion_folder_name)

