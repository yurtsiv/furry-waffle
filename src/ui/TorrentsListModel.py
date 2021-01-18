from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt

class TorrentsListModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    ProgressPercentRole = Qt.UserRole + 3
    ProgressFormattedRole = Qt.UserRole + 4

    roles = {
        IdRole: 'id'.encode('utf-8'),
        NameRole: 'name'.encode('utf-8'),
        ProgressPercentRole: 'progressPercent'.encode('utf-8'),
        ProgressFormattedRole: 'progressFormatted'.encode('utf-8')
    }

    def __init__(self, torrent_client):
        QAbstractListModel.__init__(self)

        self.torrents = torrent_client.get_torrents()

    def _format_size(self, bytes, suffix='B'):
        for unit in ['','k','M','G','T','P','E','Z']:
            if abs(bytes) < 1000.0:
                return "%3.2f%s%s" % (bytes, unit, suffix)
            bytes /= 1000.0

        return "%.1f%s%s" % (bytes, 'Y', suffix)

    def data(self, index, role=None):
        row = index.row()
        if role == self.IdRole:
            return self.torrents[row].id
        if role == self.NameRole:
            return self.torrents[row].name
        if role == self.ProgressPercentRole:
            return self.torrents[row].progress
        if role == self.ProgressFormattedRole:
            torrent = self.torrents[row]
            fields = torrent._fields
            totalSize = fields['sizeWhenDone'].value
            totalSizeFmt = self._format_size(totalSize)
            downloadedSizeFmt = self._format_size(totalSize - fields['leftUntilDone'].value)
            return "%s / %s (%2.2f%%)" % (totalSizeFmt, downloadedSizeFmt, torrent.progress)

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