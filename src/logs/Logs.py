import os
import json
from operator import attrgetter

from utils.lists import list_map, find_by
from logs.Log import Log


class Logs:
    FILE_PATH = '.logs.json'

    def __init__(self):
        self.__working = True
        try:
            self._ensure_file()
        except:
            self.__working = False

        self.__pending_logs = set()
        self.__existing_logs = None

    @property
    def working(self):
        return self.__working

    @property
    def all_logs(self):
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

    def add_log(self, torrent, text):
        self.__pending_logs.add(Log(torrent.name, text))

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
