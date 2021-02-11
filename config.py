import argparse
import logging
import os
import sys

parser = argparse.ArgumentParser(description="Pick which ones")
parser.add_argument("--debug", help="Enable debug logging", action="store_true")
ARGS, _ = parser.parse_known_args()

ENABLE_MAILER = int(os.getenv("ENABLE_MAILER", default=0))
DEBUG = ARGS.debug or int(os.getenv("DEBUG", default=0))

def set_logging():
    """Configure logging level and outputs"""
    logging.basicConfig(
        handlers=[
            logging.FileHandler(filename="app.log", mode="w+"),
            logging.StreamHandler(sys.stdout),
        ],
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s | %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %I:%M:%S%p %Z",
    )

def sftp_directory_names():
    """
    Return a list of the directory names set in the SFTP. There is one folder per school.
    """
    # SEIS could not name files based on the school, so we had to have separate directories.
    directory_names = [
        "KIPP Bayview Academy"
        , "KIPP Bayview Elementary"
        , "KIPP Bridge Academy"
        , "KIPP Esperanza High School"
        , "KIPP Excelencia Community Prep"
        , "KIPP Heartwood Academy"
        , "KIPP Heritage Academy"
        , "KIPP King Collegiate"
        , "KIPP Navigate College Prep"
        , "KIPP Prize Preparatory Academy"
        , "KIPP San Francisco Bay Academy"
        , "KIPP San Francisco College Preparatory"
        , "KIPP San Jose Collegiate"
        , "KIPP Summit Academy"
        , "KIPP Valiant Community Prep"
    ]
    return directory_names

def file_names():
    return ["Student.csv", "Service.csv"]
