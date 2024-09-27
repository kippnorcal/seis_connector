import logging
import traceback
import os
import sys

from job_notifications import create_notifications
import numpy as np
import pandas as pd
from sqlsorcery import MSSQL

from ftp import FTP
from mailer import Mailer

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


def __init__(self):
    self.sql = MSSQL()
    self.ftp = FTP()
    self.schools = self.ftp.get_directory_names(self.remotedir)


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


def read_files_into_df(file_name):
    """
    Given the file name (eg. Student or Service), read the files and concat into one DataFrame.

    Params:
        file_name (str): name of the file that you are trying to combine.

    Return:
        DataFrame: combined data from all files with the same name (ie. same type of data)
    """
    dfs = []
    for school in schools:
        path = os.path.join(LOCAL_DIR, f"{school}_{file_name}.csv")
        df = pd.read_csv(
            path, sep=",", quotechar='"', doublequote=True, dtype=str, header=0
        )
        dfs.append(df)
    merged = pd.concat(dfs)
    merged.replace(np.nan, "", regex=True, inplace=True)
    return merged


def insert_df_into_db(df, table_name):
    """
    Insert DataFrame into database with given table name.

    Params:
        df (DataFrame): data to insert into the database.
        table_name (str): name of the database table that you want to update.

    Return:
        none
    """
    table = f"{self.table_prefix}_{table_name}"
    self.sql.insert_into(table, df, if_exists="replace")
    logging.info(f"Inserted {len(df)} records into {table}.")


def main():
    config.set_logging()
    connector = Connector()
    ftp = FTP()
    remove_local_files()
    get_files_from_ftp(ftp)
    students = connector.read_files_into_df("Student")
    services = connector.read_files_into_df("Service")
    connector.insert_df_into_db(students, "Students")
    connector.insert_df_into_db(services, "Services")


if __name__ == "__main__":
    try:
        main()
        notifications.notify()
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
        notifications.notify(error_message=error_message)
