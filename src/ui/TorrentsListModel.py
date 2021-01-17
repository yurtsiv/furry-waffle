from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt

class TorrentsListModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    ProgressRole = Qt.UserRole + 6

    roles = {
        IdRole: 'id'.encode('utf-8'),
        NameRole: 'name'.encode('utf-8'),
        ProgressRole: 'progress'.encode('utf-8')
    }

    def __init__(self, torrent_client):
        QAbstractListModel.__init__(self)

        self.torrents = torrent_client.get_torrents()

    def data(self, index, role=None):
        row = index.row()
        if role == self.IdRole:
            return self.torrents[row].id
        if role == self.NameRole:
            return self.torrents[row].name
        if role == self.ProgressRole:
            return self.torrents[row].progress

        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.torrents)

    def roleNames(self):
        return self.roles

    def addItem(self, torrent):
        if next((t for t in self.torrents if t.id == torrent.id), None):
            return

        row = 0
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.torrents.insert(0, torrent)
        self.endInsertRows()