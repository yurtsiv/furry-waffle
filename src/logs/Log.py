from datetime import datetime


"""
A single log representation
"""
class Log:
    def __init__(self, title, description, created_at=None):
        self.__description = description
        self.__title = title
        self.__created_at = created_at or datetime.now()

    def matches_search(self, search_text):
        """
        Check if the log is fulfilling search criteria
        """
        s = search_text.lower()
        return self.description.lower().find(s) != -1 or self.title.lower().find(s) != -1 or self.formatted_created_at.lower().find(s) != -1

    @classmethod
    def from_serializable(cls, dict):
        """
        Create a Log instance from serializable dictionary
        """
        return cls(
            dict['description'],
            dict['title'],
            datetime.fromtimestamp(dict['created_at'])
        )

    @property
    def formatted_created_at(self):
        return self.created_at.strftime('%d/%m/%Y %H:%M:%S')

    @property
    def serializable(self):
        """
        Get serializable represntation of the log
        """
        return {
            'description': self.description,
            'title': self.title,
            'created_at': datetime.timestamp(self.created_at)
        }

    @property
    def description(self):
        return self.__description

    @property
    def title(self):
        return self.__title

    @property
    def created_at(self):
        return self.__created_at

    def __eq__(self, other):
        return self.title == other.title and self.description == other.description and self.created_at == other.created_at

    def __hash__(self):
        return hash(self.title + self.description + str(self.created_at))
