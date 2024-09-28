import os
from typing import List

import pysftp


FTP_HOST = os.getenv("FTP_HOST")
FTP_USER = os.getenv("FTP_USER")
FTP_PWD = os.getenv("FTP_PWD")


class FTPConnection:
    """
    An FTP server connection object for downloading and managing files on an FTP server.
    """

    def __init__(self):
        """
        Initialize FTP connection using pysftp.
        """
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.ftpsrv = pysftp.Connection(
            host=FTP_HOST,
            username=FTP_USER,
            password=FTP_PWD,
            cnopts=self.cnopts,
        )

    def get_directory_names(self, remote_dir_path: str) -> List[str]:
        """
        Return a list of all the directory names. For SEIS, the directory names are the school names.

        Params:
            remotedir (str): path of the remote directory.

        Return:
            list: string names of the directories.
        """
        return self.ftpsrv.listdir(remote_dir_path)

    def download_all(
            self,
            remote_dir_path: str,
            local_dir_path: str,
            sub_dir_names: List[str],
            file_names: List[str]
    ) -> None:
        """
        Loop through all sub-directories and download the files defined in init.
        """
        for school in sub_dir_names:
            for file_name in file_names:
                self.ftpsrv.get(
                    f"{remote_dir_path}/{school}/{file_name}",
                    f"{local_dir_path}/{school}_{file_name}",
                    preserve_mtime=True,
                )
