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
    pass