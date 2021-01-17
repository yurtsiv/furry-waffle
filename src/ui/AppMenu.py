from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

class AppMenu(QObject):
    def __init__(self, torrentsListModel, torrentClient):
        super().__init__()

        self.torrentsListModel = torrentsListModel
        self.torrentClient = torrentClient

    def _showError(self, errMsg):
        msg = QMessageBox()
        msg.setText(errMsg)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    @pyqtSlot(str)
    def onFileOpen(self, file_url):
        try:
            torrent = self.torrentClient.add_torrent(file_url)

            self.torrentsListModel.addItem(torrent)
        except FileNotFoundError:
            self._showError('Torrent file not found. Please try again')
        except Exception as err:
            self._showError(str(err))