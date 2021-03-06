from PyQt5.QtCore import QObject, pyqtSlot

from ui.utils import show_error

class LogsDialog(QObject):
    """
    A controller for logs dialog, which
    currently is only responsible for opening the dialog.
    """

    def __init__(self):
        super().__init__()

        # late init
        self.window = None

    def open(self):
        """
        Show logs dialog
        """
        if self.window is None:
            return

        dialog = self.window.findChild(QObject, "logsDialog")
        dialog.open()
