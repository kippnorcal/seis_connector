import os
import sys
import pysftp

# A class groups functions with a similar objective
class FTP:

    # init initializes the class. Once you create an object, it will run through all the init lines
    def __init__(self):
        FTP_HOST = os.getenv("FTP_HOST")
        FTP_USER = os.getenv("FTP_USER")
        FTP_PWD = os.getenv("FTP_PWD")

        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.ftpsrv = pysftp.Connection(
            host=FTP_HOST, username=FTP_USER, password=FTP_PWD, cnopts=self.cnopts
        )

    def testFTP(self, remotedir):
        self.data = self.ftpsrv.listdir(remotedir)
        self.ftpsrv.close()

        for i in self.data:
            print(i)

        return 1

    def download_all_files(self, sourcedir, destinationdir):
        self.sourcedir = sourcedir
        result = self.ftpsrv.get_d(self.sourcedir, destinationdir, preserve_mtime=True)

    def delete_files_remotedir(self, remotedir):
        self.remotefiles = self.ftpsrv.listdir(remotedir)
        if len(self.remotefiles) > 0:
            for filename in self.remotefiles:
                self.ftpsrv.remove(f"{remotedir}/{filename}")
    
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