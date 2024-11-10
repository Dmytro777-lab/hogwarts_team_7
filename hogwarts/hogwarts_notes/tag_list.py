from collections import UserList


class TagList(UserList):
    def add(self, tag: str):
        self.data.append(tag)

    def includes(self, tag: str) -> bool:
        return tag in self.data

    def __str__(self) -> str:
        return f"Tags: {", ".join(tag for tag in self.data) or "None"}"
