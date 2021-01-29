from PyQt5.QtCore import QObject, pyqtSlot

class AppMenu(QObject):
    """
    A controller for the application menu, which
    is reponsible for handling all the available options
    (some handlers are delegated to ContextManager).
    """

    def __init__(self, on_default_download_dir_open, on_file_selected, on_logs_open, torrent_client):
        super().__init__()

        self.__on_file_selected = on_file_selected
        self.__on_logs_open = on_logs_open
        self.__torrent_client = torrent_client
        self.__on_default_download_dir_open = on_default_download_dir_open

    @pyqtSlot()
    def on_default_download_dir(self):
        """
        QtSlot
        """
        self.__on_default_download_dir_open()

    @pyqtSlot(str)
    def on_file_open(self, file_url):
        """
        QtSlot
        """
        self.__on_file_selected(file_url)
 
    @pyqtSlot()
    def on_logs_open(self):
        """
        QtSlot
        """
        self.__on_logs_open()

    @pyqtSlot()
    def on_pause_all(self):
        """
        QtSlot.
        Pause all currently downloading torrents
        """
        torrents = self.__torrent_client.get_torrents()

        for torrent in torrents:
            if torrent.status == 'downloading' or torrent.status == 'seeding':
                torrent.stop()

    @pyqtSlot()
    def on_resume_all(self):
        """
        QtSlot.
        Resume all currently stopped torrents
        """
        torrents = self.__torrent_client.get_torrents()

        for torrent in torrents:
            if torrent.status == 'stopped':
                torrent.start()
