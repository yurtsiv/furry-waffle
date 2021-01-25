from PyQt5.QtCore import QObject, pyqtSlot

from ui.utils import show_error

class PeerLimitDialog(QObject):
    def __init__(self, torrent_client):
        super().__init__()

        self.window = None

        self.__torrent_client = torrent_client
        self.__dialog = None
        self.__limit = 0
        self.__limit_input = None
        self.__torrent = None

    def open(self, torrent_id):
        if self.window is None:
            return

        self.__limit_input = self.window.findChild(QObject, "peerLimitInput")

        try:
            self.__torrent = self.__torrent_client.get_torrent(torrent_id)
            self.__limit_input.setProperty(
                "text",
                str(self.__torrent.peer_limit)
            )
        except Exception as e:
            show_error('Torrent not found')
            return


        self.__dialog = self.window.findChild(QObject, "peerLimitDialog")
        self.__dialog.open()
    
    @pyqtSlot()
    def on_save(self):
        self.__torrent.peer_limit = self.__limit
        self.__torrent.update()
        self.__dialog.close()

    @pyqtSlot(str)
    def on_input_change(self, value):
        if not value or int(value) <= 0:
            self.__limit = self.__torrent.peer_limit
        else:
            self.__limit = int(value)
