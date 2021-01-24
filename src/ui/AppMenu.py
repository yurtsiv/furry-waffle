from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMessageBox, QDialog, QPushButton

class AppMenu(QObject):
    def __init__(self, on_file_selected):
        super().__init__()

        self.on_file_selected = on_file_selected

    @pyqtSlot(str)
    def on_file_open(self, file_url):
        self.on_file_selected(file_url)
