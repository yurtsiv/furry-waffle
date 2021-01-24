from PyQt5.QtCore import QObject, pyqtSlot

class AppMenu(QObject):
    def __init__(self, on_file_selected, on_logs_open):
        super().__init__()

        self.on_file_selected = on_file_selected
        self.on_logs_open = on_logs_open

    @pyqtSlot(str)
    def on_file_open(self, file_url):
        self.on_file_selected(file_url)
 
    @pyqtSlot()
    def on_logs_open(self):
        self.on_logs_open()
