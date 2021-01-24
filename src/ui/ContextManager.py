from PyQt5.QtWidgets import QMessageBox

from ui.AppMenu import AppMenu
from ui.TorrentsListModel import TorrentsListModel
from ui.TorrentDetailsDialog import TorrentDetailsDialog
from ui.LogsDialog import LogsDialog
from ui.LogsListModel import LogsListModel
from ui.utils import show_error
from logs.Logs import Logs

class ContextManager():
    def __init__(self, torrent_client):
        super().__init__()

        self.torrent_client = torrent_client

        self.logs = Logs()
        self.logs_dialog = LogsDialog()
        self.logs_list_model = LogsListModel(logs=self.logs)
        self.torrents_list_model = TorrentsListModel(torrent_client=torrent_client, logs=self.logs)
        self.torrent_details_dialog = TorrentDetailsDialog(torrent_client=torrent_client, on_details_accepted=self.on_details_accepted)
        self.app_menu = AppMenu(on_file_selected=self.on_file_selected, on_logs_open=self.on_logs_open)

    def on_file_selected(self, file_url):
        self.torrent_details_dialog.open(file_url)

    def on_logs_open(self):
        if self.logs.working:
            self.logs_list_model.refresh()
            self.logs_dialog.open()
        else:
            show_error('Failed to open logs')

    def on_details_accepted(self, file_url, download_dir):
        try:
            torrent = self.torrent_client.add_torrent(file_url, download_dir=download_dir)
            self.torrents_list_model.add_item(torrent)
            self.logs.log_torrent_added(torrent)
        except FileNotFoundError:
            self._show_error('Torrent file not found. Please try again')
        except Exception as err:
            show_error(str(err))

    def set_window(self, window):
        self.torrent_details_dialog.window = window
        self.logs_dialog.window = window

    def clean_up(self):
        self.torrents_list_model.clean_up()
        self.logs.save_logs()
