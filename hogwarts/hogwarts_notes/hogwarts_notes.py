from collections import UserDict
from .note import NoteRecord


class Notes(UserDict):
    def add_record(self, record: NoteRecord):
        self.data[record.note.title] = record

    def find(self, title: str) -> NoteRecord:
        return self.data.get(title)

    def delete(self, title: str):
        if title in self.data:
            del self.data[title]

    def is_empty(self) -> bool:
        return not bool(self.data)
