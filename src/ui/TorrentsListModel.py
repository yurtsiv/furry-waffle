from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QVariant, QAbstractListModel, QObject, Qt, pyqtSignal, pyqtSlot

class TorrentsListModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2

    roles = {
        IdRole: 'id'.encode('utf-8'),
        NameRole: 'name'.encode('utf-8'),
    }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)

        self.torrents = [
            {
                "id": "Hello",
                "name": "hello text"
            }
        ]

    def data(self, index, role=None):
        row = index.row()
        if role == self.IdRole:
            return self.torrents[row]['id']
        if role == self.NameRole:
            return self.torrents[row]['name']

        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.torrents)

    def roleNames(self):
        return self.roles

    def addItem(self, torrent):
        row = 0
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.torrents.insert(0, torrent)
        self.endInsertRows()