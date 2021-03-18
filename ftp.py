import os
import pysftp
import sys

import config


class FTP:
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
            host=config.FTP_HOST,
            username=config.FTP_USER,
            password=config.FTP_PWD,
            cnopts=self.cnopts,
        )
        self.file_names = ["Student.csv", "Service.csv"]

    def get_directory_names(self, remotedir):
        """
        Return a list of all the directory names. For SEIS, the directory names are the school names.

        Params:
            remotedir (str): path of the remote directory.

        Return:
            list: string names of the directories.
        """
        self.directory_names = self.ftpsrv.listdir(remotedir)
        return self.directory_names

    def download_all(self, remotedir, localdir):
        """
        Loop through all sub-directories and download the files defined in init.

        Params:
            remotedir (str): path of the remote directory.
            localdir (str): path of the local directory.

        Return:
            none
        """
        for school in self.directory_names:
            for file_name in self.file_names:
                self.ftpsrv.get(
                    f"{remotedir}/{school}/{file_name}",
                    f"{localdir}/{school}_{file_name}",
                    preserve_mtime=True,
                )

    def _archive_file(self, file):
        """
        Place the file in an 'archive' folder within its directory.

        Params:
            file (str): path and name of the file that will be archived.

        Return:
            none
        """
        self.ftpsrv.rename(
            file, file.replace(self.remotedir, f"{self.remotedir}/archive")
        )

    def _do_nothing(self, file):
        """
        Used for files and unknown file types.

        Params:
            file (str): path and name of the file that will be ignored.

        Return:
            none
        """
        pass

    def archive_remote_files(self, remotedir):
        """
        Archive all of the files in the specified remote directory.

        Params:
            file (str): path of the remote directory (ie. the FTP directory)

        Return:
            none
        """
        self.remotedir = remotedir
        self.ftpsrv.walktree(
            self.remotedir,
            fcallback=self._archive_file,
            dcallback=self._do_nothing,
            ucallback=self._do_nothing,
            recurse=False,
        )
