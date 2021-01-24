from datetime import datetime

class Log:
    def __init__(self, torrent_name, text, created_at = None):
        self.__torrent_name = torrent_name
        self.__text = text
        self.__created_at = created_at or datetime.now()
 
    @classmethod
    def from_serializable(cls, dict):
        return cls(
            dict['torrent_name'],
            dict['text'],
            datetime.fromtimestamp(dict['created_at'])
        )
 
    @property
    def serializable(self):
        return {
            'torrent_name': self.torrent_name,
            'text': self.text,
            'created_at': datetime.timestamp(self.created_at)
        }

    @property
    def torrent_name(self):
        return self.__torrent_name

    @property
    def text(self):
        return self.__text

    @property
    def created_at(self):
        return self.__created_at
    
    def __eq__(self, other):
        return self.text == other.text and self.torrent_name == other.torrent_name
 
    def __hash__(self):
        return hash(self.text + self.torrent_name)