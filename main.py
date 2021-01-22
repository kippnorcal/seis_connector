import logging
import traceback
import os
import pandas as pd
from sqlsorcery import MSSQL
import config
from mailer import Mailer
from ftp import FTP

# Pull file from FTP to local
# Confirm that files have been downloaded; if not, throw an error
# Archive files in FTP
# Transform files from FTP into dataframe
# [TBD] Compare file from FTP to what's in our database; write errors somewhere
# Import into database

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

    #Must include 'self' in the paranthesis so you can call anything in the class earlier
    def get_files_from_ftp(self):
        filelist = [f for f in os.listdir(self.localdir)]
        for f in filelist:
            os.remove(os.path.join(self.localdir, f))

        self.ftp.download_all_files(self.remotedir,self.localdir)
        
        self.filenames = os.listdir(self.localdir)
        logging.info(f"{len(self.filenames)} files downloaded")
    
    def read_into_df(self):
        dfs = []
        for filename in self.filenames:
            # path = f"{self.localdir}/{filename}"
            path = os.path.join(self.localdir, filename)
            df = pd.read_csv(
                path, sep=",", quotechar='"', doublequote=True, dtype=str, header=0
            )
            print(df)
            dfs.append(df)
        # df.fillna(value=nan_fields, inplace=True)
    
    def archive_files(self):
        self.ftp.archive_remote_files(self.remotedir)

def main():
    config.set_logging()
    connector = Connector()
    connector.get_files_from_ftp()
    connector.read_into_df()
    connector.archive_files()

if __name__ == "__main__":
    try:
        main()
        error_message = None
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
    if config.ENABLE_MAILER:
        Mailer("SEIS Connector").notify(error_message=error_message)