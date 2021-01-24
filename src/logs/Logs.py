import os
import json
from operator import attrgetter

from utils.lists import list_map
from logs.Log import Log

class Logs:
    FILE_PATH = '.logs.json'

    def __init__(self):
        try:
            self._ensure_file()
        except:
            pass

        self.__pending_logs = set()
        self.__existing_logs = None

    @property
    def all_logs(self):
        self._ensure_file()

        with open(self.FILE_PATH, 'r') as f:
            if self.__existing_logs is None:
                self.__existing_logs = set(map(
                    Log.from_serializable,
                    json.load(f)
                ))

            return list(
                sorted(
                    self.__pending_logs | self.__existing_logs,
                    key=attrgetter('created_at'),
                    reverse=True
                )
            )

    def get_by_search(self, search_text):
        return [l for l in self.all_logs if l.matches_search(search_text)]

    def add_log(self, torrent, text):
        self.__pending_logs.add(Log(torrent.name, text))
    
    def clear_all(self):
        self.__pending_logs = set()
        self.__existing_logs = set()

    def save_logs(self):
        self._ensure_file()

        all_logs = self.all_logs

        serializable_logs = list_map(
            lambda log: log.serializable,
            self.all_logs
        )

        with open(self.FILE_PATH, 'w') as f:
            json.dump(serializable_logs, f, indent=2)
            self.__pending_logs = set()
            self.__existing_logs = set(all_logs)

    def log_torrent_added(self, torrent):
        self.add_log(
            torrent,
            'Torrent added'
        )

    def _ensure_file(self):
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'w') as f:
                json.dump([], f)
