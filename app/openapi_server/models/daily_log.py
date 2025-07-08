from datetime import date


class DailyLog:
    """DailyLog model — manually cleaned from OpenAPI output"""

    def __init__(self, _date: date = None, entries: str = None):
        self.openapi_types = {
            '_date': date,
            'entries': str
        }

        self.attribute_map = {
            '_date': 'date',
            'entries': 'entries'
        }

        self.__date = _date
        self._entries = entries

    @classmethod
    def from_dict(cls, dikt) -> 'DailyLog':
        """Create DailyLog from dict"""
        _date = dikt.get("date")
        entries = dikt.get("entries")
        return cls(_date=_date, entries=entries)

    @property
    def _date(self) -> date:
        return self.__date

    @_date.setter
    def _date(self, _date: date):
        self.__date = _date

    @property
    def entries(self) -> str:
        return self._entries

    @entries.setter
    def entries(self, entries: str):
        self._entries = entries
