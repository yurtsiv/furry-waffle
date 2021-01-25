from PyQt5.QtCore import QObject, pyqtSlot

from ui.utils import show_error


"""
A controller for logs dialog, which
currently is only responsible for opening the dialog.
"""
class LogsDialog(QObject):
    def __init__(self):
        super().__init__()

        self.window = None

    def open(self):
        """
        Show logs dialog
        """
        if self.window is None:
            return

        dialog = self.window.findChild(QObject, "logsDialog")
        dialog.open()
