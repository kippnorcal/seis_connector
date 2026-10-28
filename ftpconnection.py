import os
from typing import List

import paramiko


FTP_HOST = os.getenv("FTP_HOST")
FTP_PORT = int(os.getenv("FTP_PORT", 22))
FTP_USER = os.getenv("FTP_USER")
FTP_PWD = os.getenv("FTP_PWD")
HOST_KEYS_PATH = ""
CONNECTION_TIMEOUT = 30


class FTPConnection:
    """
    An FTP server connection object for downloading and managing files on an FTP server.
    """

    def __init__(self):
        """
        Initialize SFTP connection using paramiko. The server's host key must be present in the
        known hosts file at HOST_KEYS_PATH, otherwise the connection is rejected.
        """
        self.client = paramiko.SSHClient()
        self.client.load_host_keys(HOST_KEYS_PATH)
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
        self.client.connect(
            hostname=FTP_HOST,
            port=FTP_PORT,
            username=FTP_USER,
            password=FTP_PWD,
            timeout=CONNECTION_TIMEOUT,
            banner_timeout=CONNECTION_TIMEOUT,
            look_for_keys=False,
            allow_agent=False,
        )
        self.ftpsrv = self.client.open_sftp()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def close(self) -> None:
        """
        Close the SFTP session and the underlying SSH connection.
        """
        self.ftpsrv.close()
        self.client.close()

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
                )
