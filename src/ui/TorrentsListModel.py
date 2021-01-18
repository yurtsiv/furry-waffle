from operator import index
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt, pyqtSlot
import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

class TorrentsListModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    ProgressPercentRole = Qt.UserRole + 3
    ProgressFormattedRole = Qt.UserRole + 4
    ControlBtnTextRole = Qt.UserRole + 5
    StatusRole = Qt.UserRole + 6

    roles = {
        IdRole: 'id'.encode('utf-8'),
        NameRole: 'name'.encode('utf-8'),
        ProgressPercentRole: 'progressPercent'.encode('utf-8'),
        ProgressFormattedRole: 'progressFormatted'.encode('utf-8'),
        ControlBtnTextRole: 'controlBtnText'.encode('utf-8'),
        StatusRole: 'status'.encode('utf-8')
    }

    def __init__(self, torrent_client):
        QAbstractListModel.__init__(self)

        self.torrent_client = torrent_client
        self.torrents = sorted(
            torrent_client.get_torrents(),
            key=lambda t: t.date_added,
            reverse=True
        )

        set_interval(self._fetch_torrents, 2)

    def _fetch_torrents(self):
        new_torrents = sorted(
            self.torrent_client.get_torrents(),
            key=lambda t: t.date_added,
            reverse=True
        )
        new_torrents_len = len(new_torrents)
        curr_torrents_len = len(self.torrents)

        if new_torrents_len == curr_torrents_len:
            self.torrents = new_torrents
            begin = self.createIndex(0, 0)
            end = self.createIndex(new_torrents_len, 0)
            self.dataChanged.emit(begin, end)

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
            try:
                return self.torrents[row].progress
            except:
                return 0
        if role == self.ProgressFormattedRole:
            try:
                torrent = self.torrents[row]
                fields = torrent._fields
                totalSize = fields['sizeWhenDone'].value
                totalSizeFmt = self._format_size(totalSize)
                downloadedSizeFmt = self._format_size(totalSize - fields['leftUntilDone'].value)
                return "%s / %s (%2.2f%%)" % (downloadedSizeFmt, totalSizeFmt, torrent.progress)
            except:
                return "0B / 0B (0%)"

        if role == self.StatusRole:
            return self.torrents[row].status
 
        if role == self.ControlBtnTextRole:
            torrent = self.torrents[row]

            if torrent.status == 'downloading':
                return "Pause"

            return "Resume"

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

    @pyqtSlot(str)
    def on_control_btn_click(self, torrent_id):
        try:
            torrent_idx = list(map(lambda t: str(t.id), self.torrents)).index(torrent_id)

            torrent = self.torrents[torrent_idx]
            idx = self.createIndex(torrent_idx, 0)

            if torrent.status == 'downloading':
                torrent.stop()
                self.dataChanged.emit(idx, idx)
            elif torrent.status == 'stopped':
                torrent.start()
                self.dataChanged.emit(idx, idx)
        except:
            pass