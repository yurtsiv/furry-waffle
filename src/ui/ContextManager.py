from ui.AppMenu import AppMenu
from ui.TorrentsListModel import TorrentsListModel
from ui.TorrentDetailsDialog import TorrentDetailsDialog
from ui.LogsDialog import LogsDialog
from ui.LogsListModel import LogsListModel
from ui.Footer import Footer
from ui.PeerLimitDialog import PeerLimitDialog
from ui.DefaultDownloadDirDialog import DefaultDownloadDirDialog

from utils.files import open_torrent_file
from ui.utils import show_error
from logs.Logs import Logs

"""
A central place for managing all the
controllers and glueing them together.
"""


class ContextManager():
    def __init__(self, torrent_client):
        super().__init__()

        self.__torrent_client = torrent_client

        self.__logs = Logs()
        self.__logs_dialog = LogsDialog()
        self.__default_download_dir_dialog = DefaultDownloadDirDialog(
            torrent_client=torrent_client)
        self.__logs_list_model = LogsListModel(logs=self.__logs)
        self.__peer_limit_dialog = PeerLimitDialog(
            torrent_client=torrent_client)
        self.__torrents_list_model = TorrentsListModel(
            torrent_client=torrent_client, logs=self.__logs, on_peer_limit=self.__peer_limit_dialog.open)
        self.__torrent_details_dialog = TorrentDetailsDialog(
            torrent_client=torrent_client, on_details_accepted=self.on_details_accepted)
        self.__app_menu = AppMenu(
            on_default_download_dir_open=self.__default_download_dir_dialog.open,
            on_file_selected=self.on_file_selected, on_logs_open=self.on_logs_open, torrent_client=torrent_client)
        self.__footer = Footer(torrent_client=torrent_client)

    @property
    def context_props(self):
        """
        Context properties which can be used in QML
        """
        return {
            'app_menu': self.__app_menu,
            'torrents_list_model': self.__torrents_list_model,
            'torrent_details_dialog': self.__torrent_details_dialog,
            'logs_list_model': self.__logs_list_model,
            'peer_limit_dialog': self.__peer_limit_dialog,
            'default_download_dir_dialog': self.__default_download_dir_dialog
        }

    def on_file_selected(self, file_url):
        self.__torrent_details_dialog.open(file_url)

    def on_logs_open(self):
        try:
            _ = self.__logs.all_logs
            self.__logs_list_model.refresh()
            self.__logs_dialog.open()
        except:
            show_error('Failed to open logs')

    def on_details_accepted(self, file_url, download_dir):
        try:
            torrent = self.__torrent_client.add_torrent(
                open_torrent_file(file_url), download_dir=download_dir)
            self.__torrents_list_model.add_item(torrent)
            self.__logs.add_log(torrent, 'Torrent added')
        except FileNotFoundError:
            show_error('Torrent file is not found. Please try again')
        except Exception as err:
            show_error(str(err))

    def set_window(self, window):
        """
        Propagate window object to individual controllers
        """
        self.__torrent_details_dialog.window = window
        self.__logs_dialog.window = window
        self.__footer.window = window
        self.__peer_limit_dialog.window = window
        self.__logs_list_model.window = window
        self.__default_download_dir_dialog.window = window

    def clean_up(self):
        """
        Clear all resources/timers
        """
        self.__torrents_list_model.clean_up()
        self.__footer.clean_up()
        self.__logs.save_logs()

    @property
    def app_menu(self):
        return self.__app_menu

    @property
    def torrents_list_model(self):
        return self.__torrents_list_model

    @property
    def torrent_details_dialog(self):
        return self.__torrent_details_dialog

    @property
    def logs_list_model(self):
        return self.__logs_list_model

    @property
    def peer_limit_dialog(self):
        return self.__peer_limit_dialog
