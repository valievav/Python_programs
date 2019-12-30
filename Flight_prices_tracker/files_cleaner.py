import datetime
import logging
import os

import send2trash
from custom_logger import get_logger


@get_logger
def files_cleaner(extension: str, logger: logging.Logger, to_keep_number: int = 3) -> None:
    """
    Cleans up old files and keeps the passed number of files only
    """

    # find all files
    current_dir = os.getcwd()
    files = [file for file in os.listdir(current_dir) if file.endswith(extension)]
    logger.debug(f"Detected {len(files)} {extension} files")

    if len(files) <= to_keep_number:  # do nothing if low number of files
        logger.debug("Nothing to delete")
        return None

    # get created date for files
    files_with_dates = []
    for file in files:
        epoch_date = os.path.getctime(os.path.join(os.getcwd(), file))
        str_date = datetime.datetime.fromtimestamp(epoch_date).strftime('%Y-%m-%d %H:%M:%S')
        files_with_dates.append([file, str_date])

    sorted_files_with_dates = [data for data in sorted(files_with_dates, key=lambda elem: elem[1], reverse=True)]

    # create to_keep list with file names only
    files_to_keep = [file_data[0] for file_data in sorted_files_with_dates[0:to_keep_number]]
    del sorted_files_with_dates[0:to_keep_number]
    logger.debug(f"Remained {len(files_to_keep)} {extension} files  - {files_to_keep}")

    # create to_delete list with file names only
    files_to_delete = [file_data[0] for file_data in sorted_files_with_dates]
    del sorted_files_with_dates
    for file in files_to_delete:
        send2trash.send2trash(os.path.join(current_dir, file))
    logger.debug(f"Deleted {len(files_to_delete)} {extension} files - {files_to_delete}")

