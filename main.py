import logging
import traceback
import os
import sys

from gbq-connector import CloudStorageClient
from job_notifications import create_notifications
from slugify import slugify

from ftp import FTP

"""Configure logging level and outputs"""
logging.basicConfig(
    handlers=[
        logging.FileHandler(filename="app.log", mode="w+"),
        logging.StreamHandler(sys.stdout),
    ],
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p %Z",
)


LOCAL_DIR = "files"
REMOTE_DIR = "seis"

notifications = create_notifications("SEIS Connector", "Mailgun", "app.log")


def remove_local_files():
    """Remove any leftover files from local project directory."""
    filelist = [f for f in os.listdir(LOCAL_DIR)]
    for filename in filelist:
        if "gitkeep" not in filename:
            os.remove(os.path.join(LOCAL_DIR, filename))


def get_files_from_ftp(ftp):
    """Loop through all sub-folders and download files from FTP."""
    ftp.download_all(REMOTE_DIR, LOCAL_DIR)
    filenames = [f for f in os.listdir(LOCAL_DIR) if f.endswith(".csv")]
    logging.info(f"{len(filenames)} files downloaded. ")


def get_file_paths_and_rename(schools, file_kind):
    """
    Given the file name (eg. Student or Service), read the files and concat into one DataFrame.

    Params:
        file_name (str): name of the file that you are trying to combine.

    Return:
        DataFrame: combined data from all files with the same name (ie. same type of data)
    """
    files = {}
    for school in schools:
        source_path = os.path.join(LOCAL_DIR, f"{school}_{file_kind}.csv")
        new_file_name = f"{slugify(school, separator='_')}_{file_kind}"
        dest_path = os.path.join(LOCAL_DIR, f"{new_file_name}.csv")
        os.rename(source_path, dest_path)
        files[new_file_name] = dest_path
    return files


def insert_df_into_cloud(files, sub_folder):
    """
    Insert DataFrame into database with given table name.

    Params:
        df (DataFrame): data to insert into the database.
        table_name (str): name of the database table that you want to update.

    Return:
        none
    """
    bucket = os.getenv("BUCKET")
    cloud_conn = CloudStorageClient()
    for file, file_path in files:
        blob = f"seis/{sub_folder}/{file}.csv"
        cloud_conn.load_file_to_cloud(bucket, blob, file_path)


def main():
    ftp = FTP()
    remove_local_files()
    get_files_from_ftp(ftp)
    school_dir_names = ftp.get_directory_names(REMOTE_DIR)
    student_files = get_file_paths_and_rename(school_dir_names, "Student")
    service_files = get_file_paths_and_rename(school_dir_names, "Service")
    insert_df_into_cloud(student_files, "students")
    insert_df_into_cloud(service_files, "services")


if __name__ == "__main__":
    try:
        main()
        notifications.notify()
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
        notifications.notify(error_message=error_message)
