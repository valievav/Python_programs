import os, datetime


def find_diff_between_folders(primary_folder, secondary_folder):
    """
    Compares secondary_folder against primary_folder and returns list of common and diff folders.
    :param primary_folder: abs path
    :param secondary_folder: abs path
    :return:
    """

    start_run = datetime.datetime.now()
    common_folders = []
    diff_folders = []

    # check params validity
    if not (os.path.isabs(primary_folder) and os.path.isabs(secondary_folder)):
        print("Please provide absolute path for both folders.")
        return

    for active_folder, subfolders, files in os.walk(secondary_folder):

        for subfolder in subfolders:
            subfolder_path = os.path.join(active_folder, subfolder)

            subfolder_path = os.path.relpath(subfolder_path, secondary_folder)
            primary_folder_path = os.path.join(primary_folder, subfolder_path)
            if os.path.isdir(primary_folder_path):
                common_folders.append(primary_folder_path)
            else:
                diff_folders.append(primary_folder_path)

    print(f"COMMON folders:")
    for path in common_folders:
        print(path)

    print(f"DIFF folders:")
    for path in diff_folders:
        print(path)

    end_run = datetime.datetime.now()
    diff_time = end_run - start_run
    print(f"Process finished. Execution time - {diff_time}")


primary_folder = "C:\\Users\\Venus\\Downloads\\Folder 1"
secondary_folder = "D:\\Folder 2"

find_diff_between_folders(primary_folder, secondary_folder)

