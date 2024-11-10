from collections import UserDict
from .note import NoteRecord
from colorama import Fore, Style
from rapidfuzz import process
from tabulate import tabulate
from .search import SortOrder, SortBy


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

    def list_notes(self, query: str = None, by_tags: bool = False) -> str:
        def format_as_table(notes):
            colored_notes = []
            for note in notes:
                colored_note = [
                    Fore.YELLOW + cell + Style.RESET_ALL for cell in note.split("\n")
                ]
                colored_notes.append(colored_note)

            return tabulate(colored_notes, tablefmt="grid")

        if not query:
            notes = [str(record) for record in self.data.values()]
            return format_as_table(notes)

        if by_tags:
            matching_notes = [
                str(note) for note in self.data.values() if note.has_tag(query)
            ]

            if matching_notes:
                return (
                    Fore.CYAN
                    + "Found matches:\n"
                    + format_as_table(matching_notes)
                    + Style.RESET_ALL
                )
            else:
                return Fore.RED + "No matches found." + Style.RESET_ALL
        else:
            titles = list(self.data.keys())
            results = process.extract(query, titles, limit=5)

            threshold = 80
            matching_notes = [
                str(self.data[title])
                for title, score, _ in results
                if score >= threshold
            ]

            if matching_notes:
                return (
                    Fore.CYAN
                    + "We found some matching notes:\n"
                    + format_as_table(matching_notes)
                    + Style.RESET_ALL
                )
            else:
                return Fore.RED + "No matches found for that query." + Style.RESET_ALL

    def sort_notes(self, sort_by: str, sort_order: SortOrder = None):
        # Sort by creation date

        if sort_by == SortBy.CREATED_AT.value:
            sorted_records = sorted(
                self.data.values(),
                key=lambda x: x.created_at,
                reverse=sort_order == SortOrder.DESC.value,
            )
        # Sort by last modified date (or by creation date if the note was never modified)

        elif sort_by == SortBy.MODIFIED_AT.value:
            sorted_records = sorted(
                self.data.values(),
                key=lambda x: x.modified_at or x.created_at,
                reverse=sort_order == SortOrder.DESC.value,
            )
        # Sort by tags, grouping notes with similar tags together

        else:
            available_tags = set(
                tag
                for note in self.data.values()
                if bool(note.tags)
                for tag in note.tags
            )
            sorted_records = []

            # Group notes by each tag

            for tag in available_tags:
                matching_notes = [
                    str(note) for note in self.data.values() if note.has_tag(tag)
                ]
                if matching_notes:
                    sorted_records.append(f"Tag: {tag}")
                    sorted_records.extend(matching_notes)

            notes_without_tags = [
                str(note) for note in self.data.values() if not bool(note.tags)
            ]
            # List notes without tags at the end
            if notes_without_tags:
                sorted_records.append("Notes without tags:")
                sorted_records.extend(notes_without_tags)

        return (
            Fore.CYAN
            + f"Sorted notes by '{sort_by}'{" in '" + str(sort_order) + "' order" if sort_order else ""}:\n"
            + "\n\n".join([str(note) for note in sorted_records])
            + Style.RESET_ALL
        )
