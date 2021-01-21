import logging
import traceback

import pandas as pd
from sqlsorcery import MSSQL

import config
from mailer import Mailer

from ftp import FTP

# Pull file from FTP to local
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

    #Must include 'self' in the paranthesis so you can call anything in the class earlier
    def readftp(self):
        self.ftp.testFTP("seis")

def main():
    config.set_logging()
    connector = Connector()

if __name__ == "__main__":
    try:
        main()
        error_message = None
    except Exception as e:
        logging.exception(e)
        error_message = traceback.format_exc()
    if config.ENABLE_MAILER:
        Mailer("SEIS Connector").notify(error_message=error_message)
