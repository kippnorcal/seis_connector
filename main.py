import logging
import traceback
import os

import numpy as np
import pandas as pd
from sqlsorcery import MSSQL

import config
from ftp import FTP
from mailer import Mailer


class Connector:
    """
    Data connector for Extracting data, Transforming into dataframes,
    and Loading into a database.
    """

    def __init__(self):
        self.sql = MSSQL()
        self.ftp = FTP()
        self.localdir = "files"
        self.remotedir = "seis"
        self.table_prefix = "SEIS"
        self.schools = self.ftp.get_directory_names(self.remotedir)

    def remove_local_files(self):
        """
        Remove any leftover files from local project directory.
        """
        filelist = [f for f in os.listdir(self.localdir)]
        for filename in filelist:
            if "gitkeep" not in filename:
                os.remove(os.path.join(self.localdir, filename))

    def get_files_from_ftp(self):
        """
        Loop through folders and download files from FTP.
        """
        self.remove_local_files()
        self.ftp.download_all(self.remotedir, self.localdir)
        self.filenames = [f for f in os.listdir(self.localdir) if f.endswith(".csv")]
        logging.info(f"{len(self.filenames)} files downloaded. ")

    def read_files_into_df(self, file_name):
        """
        Given the file name (Student or Service), read the files and concat into one DataFrame.
        """
        dfs = []
        for school in self.schools:
            path = os.path.join(self.localdir, f"{school}_{file_name}.csv")
            df = pd.read_csv(
                path, sep=",", quotechar='"', doublequote=True, dtype=str, header=0
            )
            dfs.append(df)
        merged = pd.concat(dfs)
        merged.replace(np.nan, "", regex=True, inplace=True)
        return merged

    def insert_df_into_db(self, df, table_name):
        """
        Insert DataFrame into database with given table name.
        """
        table = f"{self.table_prefix}_{table_name}"
        self.sql.insert_into(table, df, if_exists="replace")
        logging.info(f"Inserted {len(df)} records into {table}.")


def main():
    config.set_logging()
    connector = Connector()
    connector.get_files_from_ftp()
    students = connector.read_files_into_df("Student")
    services = connector.read_files_into_df("Service")
    connector.insert_df_into_db(students, "Students")
    connector.insert_df_into_db(services, "Services")


if __name__ == "__main__":
    try:
        main()
        error_message = None
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
    if config.ENABLE_MAILER:
        Mailer("SEIS Connector").notify(error_message=error_message)
