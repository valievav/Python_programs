import os, openpyxl


def find_files_with_keyword_values(cell_keywords, cwd=None, file_name_keyword="", search_sheet=None):
    """
    Finds excel files that contain keyword values.\n
    Function processes only files that have certain keyword in the file name and '.xlsx' extension.\n
    It iterates through all files from the specified directory including subfolders.\n
    :param cell_keywords: list
    :param cwd: absolute path, optional
    :param file_name_keyword: str, optional (if not passed, function processes all excel files)
    :param search_sheet: str, optional (if not passed, function processes all worksheets)
    :return:
    """


    def search_keyword_in_file(sheet, cell_keywords, abs_path):

        for cell_keyword in cell_keywords:
            for row in sheet.values:
                for cell in row:
                    if cell_keyword.lower() in str(cell).lower():
                        print(f"    >>> Found keyword '{cell_keyword}'. See file {abs_path}.")


    # switch to cwd if passed as param
    if cwd:
        os.chdir(cwd)
    
    # walk the directory tree
    for active_folder, subfolders, files in os.walk('.'):

        for file in files:
            file_path = os.path.join(active_folder, file)
            abs_path = os.path.abspath(file_path)  # get abs path to open file

            # search for excel files only
            if file.endswith('xlsx'):
                print(f"Processing {abs_path} ...")

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
                                sheet = wb[sheet_name]
                                search_keyword_in_file(sheet, cell_keywords, abs_path)
                        else:
                            for active_sheet in wb.sheetnames:
                                sheet = wb[active_sheet]
                                search_keyword_in_file(sheet, cell_keywords, abs_path)



file_keyword = "file"
cell_keyword_list = ["Castlevania", "Final Fantasy"]
sheet_name = "Sheet1"
working_directory = "D:\\Practice Python"

find_files_with_keyword_values(cell_keyword_list, working_directory)

