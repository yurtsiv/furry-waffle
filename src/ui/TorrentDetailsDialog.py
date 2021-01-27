from PyQt5.QtCore import QObject, pyqtSlot
from utils.files import url_to_path

"""
Torrent details dialog controller, which is responsible
for getting torrent file path and download directory from the user.
"""
class TorrentDetailsDialog(QObject):
    def __init__(self, torrent_client, on_details_accepted):
        super().__init__()

        # late init
        self.window = None

        self.__on_details_accepted = on_details_accepted
        self.__torrent_client = torrent_client

        self.__file_url = None
        self.download_dir = None

        self.__file_path_field = None
        self.__download_dir_field = None

    def open(self, file_url):
        """
        Show torrent details dialog
        """
        if self.window is None:
            return

        self.__file_url = file_url

        dialog = self.window.findChild(QObject, "torrentDetailsDialog")
        self.__file_path_field = dialog.findChild(QObject, "torrentFilePath")
        self.__file_path_field.setProperty("text", url_to_path(file_url))

        self.__download_dir_field = dialog.findChild(QObject, "downloadDir")

        self.download_dir = self.__torrent_client.get_session(
        )._fields['download_dir'].value
        self.__download_dir_field.setProperty(
            'text',
            self.download_dir
        )

        dialog.open()

    @pyqtSlot(str)
    def on_change_file(self, torrent_file_url):
        """
        QtSlot.
        Update internal state on torrent file path change
        """
        self.__file_url = torrent_file_url
        self.__file_path_field.setProperty(
            "text", url_to_path(torrent_file_url))

    @pyqtSlot(str)
    def on_change_download_dir(self, download_dir_url):
        """
        QtSlot.
        Update internal state on download directory change
        """
        self.download_dir = url_to_path(download_dir_url)
        self.__download_dir_field.setProperty("text", self.download_dir)

    @pyqtSlot()
    def on_accept(self):
        """
        QtSlot.
        Handle torrent details acceptance
        """
        self.__on_details_accepted(self.__file_url, self.download_dir)
