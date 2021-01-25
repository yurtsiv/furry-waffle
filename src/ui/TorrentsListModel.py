from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt, pyqtSlot
from ui.utils import confirm_action, show_error
from utils.lists import find_by

from utils.threading import set_interval
from utils.formatters import format_file_size

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

    ROLES = {
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

    REFETCH_SIGNAL = QtCore.pyqtSignal()

    FILTER_STATUSES = [None, 'downloading', 'seeding', 'stopped']

    def __init__(self, torrent_client, logs, on_peer_limit):
        QAbstractListModel.__init__(self)

        self.__logs = logs
        self.__torrent_client = torrent_client
        self.__filter_status = None
        self.__on_peer_limit = on_peer_limit

        self.__torrents = self._fetch_torrents()

        self.REFETCH_SIGNAL.connect(self.on_refetch)
        self.__stop_interval = set_interval(lambda: self.REFETCH_SIGNAL.emit(), 1)

    def data(self, index, role=None):
        row = index.row()
        torrent = self.__torrents[row]

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
                totalSizeFmt = format_file_size(totalSize)
                downloadedSizeFmt = format_file_size(totalSize - fields['leftUntilDone'].value)
                return "%s / %s (%2.2f%%)" % (downloadedSizeFmt, totalSizeFmt, torrent.progress)
            except:
                return "0B / 0B (0%)"

        if role == self.CONTROL_BTN_TEXT_ROLE:
            status = None
            try:
                status = torrent.status
            except:
                return "Pause"

            if status == 'downloading' or status == 'seeding':
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

            return status == 'downloading' or status == 'stopped' or status == 'seeding'

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
                    speed = format_file_size(torrent.rateDownload)
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
        return len(self.__torrents)

    def roleNames(self):
        return self.ROLES

    def add_item(self, torrent):
        if next((t for t in self.__torrents if t.id == torrent.id), None):
            return

        row = 0
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.__torrents.insert(0, torrent)
        self.endInsertRows()

    def clean_up(self):
        self.__stop_interval.set()

    @pyqtSlot()
    def on_refetch(self):
        new_torrents = self._fetch_torrents()
        new_torrents_len = len(new_torrents)
        curr_torrents_len = len(self.__torrents)

        if new_torrents_len == curr_torrents_len:
            self._log_done_torrents(self.__torrents, new_torrents)
            self.__torrents = new_torrents

            begin = self.createIndex(0, 0)
            end = self.createIndex(new_torrents_len, 0)
            self.dataChanged.emit(begin, end)

    @pyqtSlot(int)
    def on_filter(self, filter_idx):
        self.__filter_status = self.FILTER_STATUSES[filter_idx]
        self.beginResetModel()
        self.__torrents = self._fetch_torrents()
        self.endResetModel()

    @pyqtSlot(str)
    def on_control_btn_click(self, torrent_id):
        try:
            torrent_idx = list(map(lambda t: str(t.id), self.__torrents)).index(torrent_id)

            torrent = self.__torrents[torrent_idx]
            idx = self.createIndex(torrent_idx, 0)
            status = torrent.status

            if status == 'downloading' or status == 'seeding':
                torrent.stop()
                self.dataChanged.emit(idx, idx)
            elif status == 'stopped':
                torrent.start()
                self.dataChanged.emit(idx, idx)
        except:
            pass

    @pyqtSlot(str)
    def on_remove(self, torrent_id):
        self._remove_torrent(torrent_id)

    @pyqtSlot(str)
    def on_remove_with_data(self, torrent_id):
        self._remove_torrent(torrent_id, True)

    @pyqtSlot(str)
    def on_peer_limit(self, torrent_id):
        self.__on_peer_limit(int(torrent_id))

    def _remove_torrent(self, torrent_id, delete_data = False):
        try:
            torrent_idx = list(map(lambda t: str(t.id), self.__torrents)).index(torrent_id)
            torrent = self.__torrents[torrent_idx]

            confirm_msg = 'Do you really want to remove "' + torrent.name + '"'
            if delete_data:
                confirm_msg += ' and all the data?'
            else:
                confirm_msg += ' from the list?'

            if not confirm_action(confirm_msg, 'Remove torrent'):
                return

            self.__logs.add_log(
                torrent,
                'Torrent removed'
            )

            self.__torrent_client.remove_torrent(
                torrent.id,
                delete_data
            )

            self.beginRemoveRows(QModelIndex(), torrent_idx, torrent_idx)
            del self.__torrents[torrent_idx]
            self.endRemoveRows()
        except Exception as e:
            show_error(str(e))

    def _fetch_torrents(self):
        all_sorted = sorted(
            self.__torrent_client.get_torrents(),
            key=lambda t: t.date_added,
            reverse=True
        )

        if self.__filter_status is None:
            return all_sorted

        return [t for t in all_sorted if t.status == self.__filter_status]

    def _log_done_torrents(self, prev_torrents, new_torrents):
        try:
            for torrent in new_torrents:
                if torrent.progress == 100 and find_by(lambda t: t.name == torrent.name, prev_torrents).progress != 100:
                    self.__logs.add_log(torrent, 'Download finished')
        except:
            pass
