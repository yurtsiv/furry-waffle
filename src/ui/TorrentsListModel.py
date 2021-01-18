from operator import index
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt, pyqtSlot
import threading

def set_interval(func, sec):
    stopped = threading.Event()

    def func_wrapper():
        while not stopped.wait(sec):
            func()

    t = threading.Thread(target=func_wrapper)
    t.daemon = True
    t.start()

    return stopped

class TorrentsListModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    ProgressPercentRole = Qt.UserRole + 3
    ProgressFormattedRole = Qt.UserRole + 4
    ControlBtnTextRole = Qt.UserRole + 5
    ControlBtnVisibleRole = Qt.UserRole + 6
    StatsFormattedRole = Qt.UserRole + 7

    roles = {
        IdRole: 'id'.encode('utf-8'),
        NameRole: 'name'.encode('utf-8'),
        ProgressPercentRole: 'progressPercent'.encode('utf-8'),
        ProgressFormattedRole: 'progressFormatted'.encode('utf-8'),
        ControlBtnTextRole: 'controlBtnText'.encode('utf-8'),
        ControlBtnVisibleRole: 'controlBtnVisible'.encode('utf-8'),
        StatsFormattedRole: 'statsFormatted'.encode('utf-8')
    }

    def __init__(self, torrent_client):
        QAbstractListModel.__init__(self)

        self.torrent_client = torrent_client
        self.torrents = sorted(
            torrent_client.get_torrents(),
            key=lambda t: t.date_added,
            reverse=True
        )

        self.stop_interval = set_interval(self._fetch_torrents, 1)

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

        if role == self.ControlBtnTextRole:
            torrent = self.torrents[row]
            
            status = None
            try:
                status = torrent.status
            except:
                return "Pause"

            if status == 'downloading':
                return "Pause"

            return "Resume"
        
        if role == self.ControlBtnVisibleRole:
            torrent = self.torrents[row]

            status = None
            try:
                status = torrent.status
            except:
                return False

            return status == 'downloading' or status == 'stopped'
        
        if role == self.StatsFormattedRole:
            torrent = self.torrents[row]
            
            try:
                if torrent.status == 'check pending' or torrent.status == 'checking':
                    return 'Checking...'
                
                if torrent.status == 'stopped':
                    return 'Paused'

                if torrent.status == 'downloading':
                    speed = self._format_size(torrent.rateDownload)
                    peers_connected = torrent._fields['peersConnected'].value or 0
                    peers_sending = torrent._fields['peersSendingToUs'].value or 0

                    return 'Downloading from %d of %d peers. Speed: %s/s' % (peers_sending, peers_connected, speed)

                return 'Seeding'
            except Exception as e:
                print(e)
                return ''

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
    
    def _remove_torrent(self, torrent_id, delete_data = False):
        try:
            torrent_idx = list(map(lambda t: str(t.id), self.torrents)).index(torrent_id)
            torrent = self.torrents[torrent_idx]

            self.torrent_client.remove_torrent(
                torrent.id,
                delete_data
            )

            idx = self.createIndex(torrent_idx, 0)
            self.beginRemoveRows(QModelIndex(), torrent_idx, torrent_idx)
            del self.torrents[torrent_idx]
            self.endRemoveRows()
        except Exception as e:
            pass
    
    def clean_up(self):
        self.stop_interval.set()

    @pyqtSlot(str)
    def on_remove(self, torrent_id):
        self._remove_torrent(torrent_id)

    @pyqtSlot(str)
    def on_remove_with_data(self, torrent_id):
        self._remove_torrent(torrent_id, True)
