from PyQt5.QtWidgets import QMessageBox

from ui.AppMenu import AppMenu
from ui.TorrentsListModel import TorrentsListModel
from ui.TorrentDetailsDialog import TorrentDetailsDialog

class ContextManager():
    def __init__(self, torrent_client):
        super().__init__()

        self.torrent_client = torrent_client
        self.torrents_list_model = TorrentsListModel(torrent_client)
        self.torrent_details_dialog = TorrentDetailsDialog(torrent_client=torrent_client, on_details_accepted=self.on_details_accepted)

        self.app_menu = AppMenu(on_file_selected=self.on_file_selected)

    def on_file_selected(self, file_url):
        self.torrent_details_dialog.open(file_url)

    def _showError(self, errMsg):
        msg = QMessageBox()
        msg.setText(errMsg)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def on_details_accepted(self, file_url, download_dir):
        try:
            torrent = self.torrent_client.add_torrent(file_url, download_dir=download_dir)
            self.torrents_list_model.add_item(torrent)
        except FileNotFoundError:
            self._showError('Torrent file not found. Please try again')
        except Exception as err:
            self._showError(str(err))

    def set_window(self, window):
        self.torrent_details_dialog.window = window

    def clean_up(self):
        self.torrents_list_model.clean_up()
