from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from utils.threading import set_interval
from utils.formatters import format_file_size

"""
A controller for the application footer, which
is responsible for periodically updating
different kinds of stats shown.
"""
class Footer(QObject):
    REFETCH_SIGNAL = pyqtSignal()

    def __init__(self, torrent_client):
        super().__init__()

        # late init
        self.window = None

        self.__footer_text_view = None
        self.__torrent_client = torrent_client
        self.REFETCH_SIGNAL.connect(self.on_refetch)
        self.__stop_interval = set_interval(lambda: self.REFETCH_SIGNAL.emit(), 1)
    
    def clean_up(self):
        """
        Clear all resources/timers
        """
        self.__stop_interval.set()

    @pyqtSlot()
    def on_refetch(self):
        """
        QtSlot.
        Refresh the UI
        """
        if self.window is None:
            return
        
        if self.__footer_text_view is None:
            self.__footer_text_view = self.window.findChild(QObject, 'footerText')

        stats = self.__torrent_client.session_stats()._fields['cumulative_stats'].value

        downloaded = format_file_size(stats['downloadedBytes'])
        uploaded = format_file_size(stats['uploadedBytes'])

        self.__footer_text_view.setProperty(
            'text',
            'Downloaded: ' + downloaded + '          Uploaded: ' + uploaded 
        )
