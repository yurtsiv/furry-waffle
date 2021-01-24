from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt, pyqtSlot
from ui.utils import confirm_action

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
            return log.formatted_created_at

        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.__logs)

    def roleNames(self):
        return self.ROLES
    
    @pyqtSlot(str)
    def on_search_change(self, search_text):
        self.beginResetModel()
        self.__logs = self.__logs_obj.get_by_search(search_text)
        self.endResetModel()

    @pyqtSlot()
    def on_clear_all(self):
        if confirm_action('Do you really want to delete all logs?', 'Clear logs'):
            self.__logs_obj.clear_all()
            self.refresh()
