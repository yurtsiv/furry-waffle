from PyQt5.QtCore import QObject, pyqtSlot
from utils.files import url_to_path

"""
Torrent details dialog controller, which is responsible
for getting torrent file path and download directory from the user.
"""
class TorrentDetailsDialog(QObject):
    def __init__(self, torrent_client, on_details_accepted):
        super().__init__()

        self.on_details_accepted = on_details_accepted
        self.torrent_client = torrent_client
        self.window = None

        self.file_url = None
        self.download_dir = None

        self.file_path_field = None
        self.download_dir_field = None

    def open(self, file_url):
        """
        Show torrent details dialog
        """
        if self.window is None:
            return

        self.file_url = file_url

        dialog = self.window.findChild(QObject, "torrentDetailsDialog")
        self.file_path_field = dialog.findChild(QObject, "torrentFilePath")
        self.file_path_field.setProperty("text", url_to_path(file_url))

        self.download_dir_field = dialog.findChild(QObject, "downloadDir")
        
        self.download_dir = self.torrent_client.get_session()._fields['download_dir'].value
        self.download_dir_field.setProperty(
            "text",
            self.download_dir
        )

        dialog.open()

    @pyqtSlot(str)
    def on_change_file(self, torrent_file_url):
        """
        QtSlot.
        Update internal state on torrent file path change
        """
        self.file_url = torrent_file_url
        self.file_path_field.setProperty("text", url_to_path(torrent_file_url))

    @pyqtSlot(str)
    def on_change_download_dir(self, download_dir_url):
        """
        QtSlot.
        Update internal state on download directory change
        """
        self.download_dir = url_to_path(download_dir_url)
        self.download_dir_field.setProperty("text", self.download_dir)

    @pyqtSlot()
    def on_accept(self):
        """
        QtSlot.
        Handle torrent details acceptance
        """
        self.on_details_accepted(self.file_url, self.download_dir)
