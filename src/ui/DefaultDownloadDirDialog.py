from PyQt5.QtCore import QObject, pyqtSlot
from utils.files import url_to_path

"""
Default download directory dialog controller, which is responsible
for setting the default download directory for each new torrent.
"""
class DefaultDownloadDirDialog(QObject):
    def __init__(self, torrent_client):
        super().__init__()

        # late init
        self.window = None

        self.__torrent_client = torrent_client
        self.__dir_url = None
        self.__dir_path = None
        self.__dir_path_field = None

    def open(self):
        """
        Show default download directory dialog
        """
        if self.window is None:
            return

        dialog = self.window.findChild(QObject, "defaultDownloadDirDialog")
        self.__dir_path_field = dialog.findChild(QObject, "defaultDownloadDir")
        session = self.__torrent_client.get_session()
        self.__dir_path_field.setProperty(
            'text',
            session._fields['download_dir'].value
        )

        dialog.open()

    @pyqtSlot(str)
    def on_change_dir(self, dir_url):
        """
        QtSlot.
        Update internal state on download directory change
        """
        self.__dir_path = url_to_path(dir_url)
        self.__dir_path_field.setProperty("text", self.__dir_path)

    @pyqtSlot()
    def on_accept(self):
        """
        QtSlot.
        Handle torrent details acceptance
        """
        self.__torrent_client.set_session(download_dir=self.__dir_path)
