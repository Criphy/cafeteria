import datetime
import json

from worker import Worker


class Cafe:
    title: str
    level: int = 1
    workers: list[Worker] = []

    def __init__(self):
        print(datetime.datetime.now())

    def __to_json__(self):
        _title, _level, _workers = self.__data__()
        return json.dumps({"title": _title, "level": _level, "workers": _workers})

    def __from_json__(self, _title, _level, _workers):
        self.title, self.level, self.workers = _title, _level, _workers

    def __data__(self):
        return self.title, self.level, [w.__data__() for w in self.workers]

    def setTitle(self, _title):
        self.title = _title

    def addWorker(self, _worker: Worker):
        self.workers.append(_worker)

    def save(self, cursor, pid):
        cursor.execute("""
        UPDATE players
        SET data = %s
        WHERE id = %s
        """, (self.__to_json__(), pid))
