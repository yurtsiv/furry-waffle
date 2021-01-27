from PyQt5.QtCore import QModelIndex, QAbstractListModel, Qt, pyqtSlot, QObject
from ui.utils import confirm_action, show_info

"""
A controller for logs list, which is responsible for
providing the data for the view and handling user
interactions like searching or clearing logs.
"""
class LogsListModel(QAbstractListModel):
    DESCRIPTION_ROLE = Qt.UserRole + 1
    TITLE_ROLE = Qt.UserRole + 2
    CREATED_AT_ROLE = Qt.UserRole + 3

    ROLES = {
        TITLE_ROLE: 'title'.encode('utf-8'),
        DESCRIPTION_ROLE: 'description'.encode('utf-8'),
        CREATED_AT_ROLE: 'created_at'.encode('utf-8')
    }

    def __init__(self, logs):
        QAbstractListModel.__init__(self)

        # late init
        self.window = None

        self.__logs_obj = logs
        self.__logs = []

    def refresh(self):
        """
        Refresh the whole list of logs
        """
        self.beginResetModel()
        self.__logs = self.__logs_obj.all_logs
        self.endResetModel()

    def data(self, index, role=None):
        """
        Provide data for the UI
        """
        row = index.row()
        log = self.__logs[row]

        if role == self.TITLE_ROLE:
            return log.title

        if role == self.DESCRIPTION_ROLE:
            return log.description

 
        if role == self.CREATED_AT_ROLE:
            return log.formatted_created_at

        return None

    def rowCount(self, parent=QModelIndex()):
        """
        Override.
        Get number of logs in the list
        """
        return len(self.__logs)

    def roleNames(self):
        """
        Override.
        Get variables which can be used in QML
        """
        return self.ROLES
    
    @pyqtSlot(str)
    def on_search_change(self, search_text):
        """
        QtSlot.
        Apply search
        """
        self.beginResetModel()
        self.__logs = self.__logs_obj.get_by_search(search_text)
        self.endResetModel()

    @pyqtSlot()
    def on_clear_all(self):
        """
        QtSlot.
        Clear all logs
        """

        if self.__logs_obj.all_logs == []:
            return

        if confirm_action('Do you really want to delete all logs?', 'Clear logs'):
            self.__logs_obj.clear_all()
            self.refresh()

    @pyqtSlot(str)
    def on_clear_filtered(self, search_text):
        """
        QtSlot.
        Clear only those logs which are currently visible
        """
        if self.__logs == []:
            return

        if confirm_action('Do you really want to delete the logs you see in the list?', 'Clear logs'):
            self.__logs_obj.clear_by_search(search_text)
            self._clear_filter_field()
            self.__logs = self.__logs_obj.all_logs
            self.refresh()
 
    def _clear_filter_field(self):
        field = self.window.findChild(QObject, 'logSearchField')
        field.setProperty('text', '')