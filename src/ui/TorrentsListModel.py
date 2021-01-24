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
    ID_ROLE = Qt.UserRole + 1
    NAME_ROLE = Qt.UserRole + 2
    PROGRESS_PERCENT_ROLE = Qt.UserRole + 3
    PROGRESS_FORMATTED_ROLE = Qt.UserRole + 4
    CONTROL_BTN_TEXT_ROLE = Qt.UserRole + 5
    CONTROL_BTN_VISIBLE_ROLE = Qt.UserRole + 6
    STATS_FORMATTED_ROLE = Qt.UserRole + 7
    PROGRESS_BAR_COLOR_ROLE = Qt.UserRole + 8
    STATS_COLOR_ROLE = Qt.UserRole + 9

    roles = {
        ID_ROLE: 'id'.encode('utf-8'),
        NAME_ROLE: 'name'.encode('utf-8'),
        PROGRESS_PERCENT_ROLE: 'progress_percent'.encode('utf-8'),
        PROGRESS_FORMATTED_ROLE: 'progress_formatted'.encode('utf-8'),
        CONTROL_BTN_TEXT_ROLE: 'control_btn_text'.encode('utf-8'),
        CONTROL_BTN_VISIBLE_ROLE: 'control_btn_visible'.encode('utf-8'),
        STATS_FORMATTED_ROLE: 'stats_formatted'.encode('utf-8'),
        PROGRESS_BAR_COLOR_ROLE: 'progress_bar_color'.encode('utf-8'),
        STATS_COLOR_ROLE: 'stats_color'.encode('utf-8')
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
        torrent = self.torrents[row]

        if role == self.ID_ROLE:
            return torrent.id
        if role == self.NAME_ROLE:
            return torrent.name
        if role == self.PROGRESS_PERCENT_ROLE:
            try:
                return torrent.progress
            except:
                return 0
        if role == self.PROGRESS_FORMATTED_ROLE:
            try:
                fields = torrent._fields
                totalSize = fields['sizeWhenDone'].value
                totalSizeFmt = self._format_size(totalSize)
                downloadedSizeFmt = self._format_size(totalSize - fields['leftUntilDone'].value)
                return "%s / %s (%2.2f%%)" % (downloadedSizeFmt, totalSizeFmt, torrent.progress)
            except:
                return "0B / 0B (0%)"

        if role == self.CONTROL_BTN_TEXT_ROLE:
            status = None
            try:
                status = torrent.status
            except:
                return "Pause"

            if status == 'downloading':
                return "Pause"

            return "Resume"

        if role == self.CONTROL_BTN_VISIBLE_ROLE:
            status = None
            try:
                status = torrent.status
            except:
                return False
            
            error_string = torrent._fields['errorString'].value
            if error_string:
                return False

            return status == 'downloading' or status == 'stopped'

        if role == self.STATS_FORMATTED_ROLE:
            status = None
            try:
                status = torrent.status
            except:
                return 'Preparing...'

            error_string = torrent._fields['errorString'].value

            try:
                if error_string:
                    return 'Error: ' + error_string

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

        if role == self.PROGRESS_BAR_COLOR_ROLE:
            status = None
            try:
                status = torrent.status
            except:
                return '#4caf50'

            if status == 'downloading' or status == 'seeding':
                return '#4caf50'

            return '#bfbfbf'

        if role == self.STATS_COLOR_ROLE:
            status = None
            try:
                status = torrent.status
            except:
                return 'black'

            error_string = torrent._fields['errorString'].value

            if error_string:
                return '#bd0000'

            return 'black'

        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.torrents)

    def roleNames(self):
        return self.roles

    def add_item(self, torrent):
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
