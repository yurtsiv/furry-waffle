import sys

from PyQt5.QtCore import QObject, pyqtSlot

class AppMenu(QObject):
    def __init__(self, torrents_list_model):
        super().__init__()

        self.torrents_list_model = torrents_list_model

    @pyqtSlot(list)
    def onFilesOpen(self, a):
        self.torrents_list_model.addItem({
            'id': 'hello',
            'name': 'new_item' 
        })
