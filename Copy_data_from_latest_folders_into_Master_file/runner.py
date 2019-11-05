import datetime
import logging
import os

from master_file_from_latest_folder import find_all_latest_folders, copy_data_into_master_file

from Tkinter_GUI_form.one_elem_str_param_from_list import one_elem_str_param_from_list
from Tkinter_GUI_form.tkinker_gui import get_user_parameters_with_gui


def main():

    # prepare input structure for GUI form
    params_input = {"source_path": ["FILE", os.path.join(os.getcwd(), "Test_data", "Source_folder")],
                    "file_keywords": ["ENTRY", ["data"]],
                    "sheet_keywords": ["ENTRY", ["detailed", "general"]],
                    "skip_folders": ["ENTRY", ["Space skipper"]],
                    "priority_keyword": ["ENTRY", "updated"],
                    "destination_path": ["FILE", os.path.join(os.getcwd(), "Test_data", "Destination_folder")],
                    "destination_file": ["ENTRY", "Master_file.xlsx"],
                    }

    params_output = get_user_parameters_with_gui(params_input)

    # extracting parameter values
    source_path = params_output["source_path"]
    file_keywords = params_output["file_keywords"]
    sheet_keywords = params_output["sheet_keywords"]
    skip_folders = params_output["skip_folders"]
    priority_keyword = one_elem_str_param_from_list(params_output["priority_keyword"])
    destination_path = params_output["destination_path"]
    destination_file = one_elem_str_param_from_list(params_output["destination_file"])

    print("Received input parameters from GUI form:")
    print(f">> source_path - {source_path},\n"
          f">> file_keywords - {file_keywords},\n"
          f">> sheet_keywords - {sheet_keywords},\n"
          f">> skip_folders - {skip_folders},\n"
          f">> priority_keyword - {priority_keyword},\n"
          f">> destination_path - {destination_path},\n"
          f">> destination_file - {destination_file}")

    print("Process started...")
    start = datetime.datetime.now()
    logging.basicConfig(level=logging.WARNING, format=' %(asctime)s - %(levelname)s - %(message)s')

    # collect latest folders date and path
    latest_folders_data = find_all_latest_folders(cwd=source_path,
                                                  exclude_folders=skip_folders,
                                                  priority_keyword=priority_keyword,
                                                  )

    # copy data from matched files into Master file
    copy_data_into_master_file(cwd=source_path,
                               target_folders_data=latest_folders_data,
                               file_keywords=file_keywords,
                               sheet_keywords=sheet_keywords,
                               master_file_path=destination_path,
                               master_file=destination_file,
                               )

    finish = datetime.datetime.now()
    print(f"Process finished. Time spent {finish - start}")


if __name__ == "__main__":
    main()

