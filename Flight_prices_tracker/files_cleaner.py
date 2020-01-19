import datetime
import logging
import os

import send2trash


def files_cleaner(path_to_clean: str, extension: str, logger: logging.Logger,
                  exception_file: str = None, to_keep_number: int = 5) -> None:
    """
    Cleans up old files and keeps the passed number of files only
    """

    stage_name = 'CLEANUP_FILES'
    os.chdir(path_to_clean)

    # find all files
    files = [file for file in os.listdir('.') if file.endswith(extension) and file != exception_file]
    logger.debug(f"{stage_name} - Found {len(files)} {extension} files")

    if len(files) <= to_keep_number:  # do nothing if low number of files
        logger.debug(f"{stage_name} - No {extension} files to delete")
        return None

    # get created date for files
    files_with_dates = []
    for file in files:
        epoch_date = os.path.getctime(os.path.join(os.getcwd(), file))
        str_date = datetime.datetime.fromtimestamp(epoch_date).strftime('%Y-%m-%d %H:%M:%S')
        files_with_dates.append([file, str_date])

    sorted_files_with_dates = sorted(files_with_dates, key=lambda elem: elem[1], reverse=True)

    # create to_keep list with file names only
    files_to_keep = [file_data[0] for file_data in sorted_files_with_dates[0:to_keep_number]]
    del sorted_files_with_dates[0:to_keep_number]
    logger.debug(f"{stage_name} - Remained {len(files_to_keep)} {extension} files  - {files_to_keep}")

    # create to_delete list with file names only
    files_to_delete = [file_data[0] for file_data in sorted_files_with_dates]
    del sorted_files_with_dates
    for file in files_to_delete:
        send2trash.send2trash(os.path.join(path_to_clean, file))
    logger.debug(f"{stage_name} - Deleted {len(files_to_delete)} {extension} files - {files_to_delete}")

