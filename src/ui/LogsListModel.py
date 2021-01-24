from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt, pyqtSlot


class LogsListModel(QAbstractListModel):
    TORRENT_NAME_ROLE = Qt.UserRole + 1
    TEXT_ROLE = Qt.UserRole + 2
    CREATED_AT = Qt.UserRole + 3

    ROLES = {
        TORRENT_NAME_ROLE: 'torrent_name'.encode('utf-8'),
        TEXT_ROLE: 'log_text'.encode('utf-8'),
        CREATED_AT: 'created_at'.encode('utf-8')
    }

    def __init__(self, logs):
        QAbstractListModel.__init__(self)

        self.__logs_obj = logs
        self.__logs = []

    def refresh(self):
        self.beginResetModel()
        self.__logs = self.__logs_obj.all_logs
        self.endResetModel()

    def data(self, index, role=None):
        row = index.row()
        log = self.__logs[row]

        if role == self.TORRENT_NAME_ROLE:
            return log.torrent_name

        if role == self.TEXT_ROLE:
            return log.text
 
        if role == self.CREATED_AT:
            return log.created_at.strftime('%d/%m/%Y %H:%M:%S')

        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.__logs)

    def roleNames(self):
        return self.ROLES
