from datetime import datetime
from .tag_list import TagList


class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def edit(self, new_title: str, new_content: str):
        if new_title:
            self.title = new_title
        if new_content:
            self.content = new_content

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}"


class NoteRecord:
    def __init__(self, title: str, content: str):
        self.note = Note(title, content)
        self.tags = TagList()
        self.created_at = datetime.now()
        self.modified_at = None

    def edit(self, new_title: str, new_content: str):
        self.note.edit(new_title, new_content)
        self.modified_at = datetime.now()

    def add_tag(self, tag: str):
        self.tags.add(tag)
        self.modified_at = datetime.now()

    def has_tag(self, name: str):
        return self.tags.includes(name)

    def show_note(self):
        return str(self.note)

    def show_tags(self):
        return str(self.tags)

    def __str__(self):
        return (
            f"{self.show_note()}\n"
            f"{self.show_tags()}\n"
            f"Created at: {self.created_at}\n"
            f"Modified at: {self.modified_at if self.modified_at else 'Never'}"
        )
