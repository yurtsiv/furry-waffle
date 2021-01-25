from PyQt5.QtCore import QObject, pyqtSlot

class AppMenu(QObject):
    def __init__(self, on_file_selected, on_logs_open, torrent_client):
        super().__init__()

        self.on_file_selected = on_file_selected
        self.on_logs_open = on_logs_open
        self.__torrent_client = torrent_client

    @pyqtSlot(str)
    def on_file_open(self, file_url):
        self.on_file_selected(file_url)
 
    @pyqtSlot()
    def on_logs_open(self):
        self.on_logs_open()

    @pyqtSlot()
    def on_pause_all(self):
        torrents = self.__torrent_client.get_torrents()

        for torrent in torrents:
            if torrent.status == 'downloading' or torrent.status == 'seeding':
                torrent.stop()

    @pyqtSlot()
    def on_resume_all(self):
        torrents = self.__torrent_client.get_torrents()

        for torrent in torrents:
            if torrent.status == 'stopped':
                torrent.start()
