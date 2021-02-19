import os
import pysftp
import sys

import config


class FTP:
    def __init__(self):
        """
        Initialize FTP connection using pysftp.
        """
        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.ftpsrv = pysftp.Connection(
            host=config.FTP_HOST, username=config.FTP_USER, password=config.FTP_PWD, cnopts=self.cnopts
        )
        self.file_names = ["Student.csv", "Service.csv"]

    def get_directory_names(self, remotedir):
        """
        Return a list of all the directory names.
        
        For SEIS, the directory names are the school names.
        """
        self.directory_names = self.ftpsrv.listdir(remotedir)
        return self.directory_names

    def download_all(self, remotedir, localdir):
        """
        Recursively loop through all directories and get the two csv files.
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
        :param file: Path and name of the file that will be archived.
        :type file: String
        """
        self.ftpsrv.rename(
            file, file.replace(self.remotedir, f"{self.remotedir}/archive")
        )

    def _do_nothing(self, file):
        """
        Used for files and unknown file types.
        :param file: Path and name of the file that will be ignored.
        :type file: String
        """
        pass

    def archive_remote_files(self, remotedir):
        """
        Archive all of the files in the specified remote directory.

        :param remotedir: Path of the remote directory (ie. the FTP directory)
        :type remotedir: String
        """
        self.remotedir = remotedir
        self.ftpsrv.walktree(
            self.remotedir,
            fcallback=self._archive_file,
            dcallback=self._do_nothing,
            ucallback=self._do_nothing,
            recurse=False,
        )
