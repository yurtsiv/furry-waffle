from PyQt5.QtCore import QObject, pyqtSlot

from ui.utils import show_error


class LogsDialog(QObject):
    def __init__(self):
        super().__init__()

        self.window = None

    def open(self):
        if self.window is None:
            return

        dialog = self.window.findChild(QObject, "logsDialog")
        dialog.open()
