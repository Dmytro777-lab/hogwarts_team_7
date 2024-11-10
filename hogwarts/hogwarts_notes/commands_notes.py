import questionary
from colorama import Fore, Style

import validators
from helpers import input_error, NotesError
from hogwarts_notes import Notes, NoteRecord
from hogwarts_notes.search import SearchBy, SortBy, SortOrder


@input_error
def add_note(notes_list: Notes):
    while True:
        title = questionary.text(
            "What is the title for your note?",
            validate=validators.validators.RequiredValidator,
        ).ask()

        if notes_list.find(title):
            print(
                Fore.RED
                + f"A note with the title '{title}' already exists. Choose a different title."
                + Style.RESET_ALL
            )
        else:
            break

    content = questionary.text(
        "What is the content for your note?",
        validate=validators.validators.RequiredValidator,
    ).ask()

    record = NoteRecord(title, content)
    notes_list.add_record(record)

    return Fore.GREEN + f"Note titled '{title}' is added." + Style.RESET_ALL


@input_error
def delete_note(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "No notes found." + Style.RESET_ALL)

    title = questionary.autocomplete(
        "What is the title of the note you wish to delete?",
        choices=[*notes_list.keys()],
        validate=validators.validators.RequiredValidator,
    ).ask()

    record = notes_list.find(title)

    if not record:
        return NotesError(
            Fore.RED + f"Note titled '{title}'is not found." + Style.RESET_ALL
        )

    notes_list.delete(title)
    return Fore.RED + f"Note titled '{title}' has been deleted." + Style.RESET_ALL


@input_error
def update_note(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "There are no notes." + Style.RESET_ALL)

    title = questionary.autocomplete(
        "What is the title of the note you wish to update?",
        choices=[*notes_list.keys()],
        validate=validators.validators.RequiredValidator,
    ).ask()
    record = notes_list.find(title)

    if not record:
        return NotesError(
            Fore.RED + f"Note titled '{title}' is not found." + Style.RESET_ALL
        )

    new_title = questionary.text(
        f"Enter the new title (current: {record.note.title}):",
        default=record.note.title,
        validate=validators.validators.RequiredValidator,
    ).ask()

    new_content = questionary.text(
        f"Enter the new content (current: {record.note.content}):",
        default=record.note.content,
        validate=validators.validators.RequiredValidator,
    ).ask()

    record.note.edit(new_title, new_content)

    return Fore.GREEN + f"Note titled '{title}' has been updated." + Style.RESET_ALL


@input_error
def search_notes(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(
            Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL
        )

    search_by = questionary.select(
        "Please specify a search type:",
        choices=[search.value for search in SearchBy],
    ).ask()

    if search_by == SearchBy.TITLE.value:
        query = questionary.autocomplete(
            "Please enter the note title:",
            choices=[*notes_list.keys()],
            validate=validators.validators.RequiredValidator,
        ).ask()

        return notes_list.list_notes(query)
    else:
        query = questionary.text(
            "Please enter the tag name:",
            validate=validators.validators.RequiredValidator,
        ).ask()

        return notes_list.list_notes(query, by_tags=True)


@input_error
def show_notes(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "There are no notes." + Style.RESET_ALL)

    return notes_list.list_notes()


@input_error
def sort_notes(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(Fore.RED + "No notes be found" + Style.RESET_ALL)

    sort_by = questionary.select(
        "Please specify a sort type:",
        choices=[sort.value for sort in SortBy],
    ).ask()

    sort_order = None

    if sort_by is not SortBy.TAGS.value:
        sort_order = questionary.select(
            "Please specify a sort order:",
            choices=[sort.value for sort in SortOrder],
        ).ask()

    return notes_list.sort_notes(sort_by, sort_order)


@input_error
def add_tag(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(
            Fore.RED + "Arrr, no notes be found in the captain's log!" + Style.RESET_ALL
        )

    title = questionary.autocomplete(
        "Please enter the note title:",
        choices=[*notes_list.keys()],
        validate=validators.validators.RequiredValidator,
    ).ask()

    record = notes_list.find(title)

    if not record:
        raise NotesError(
            Fore.RED + f"Note titled '{title}' not found." + Style.RESET_ALL
        )

    while True:
        new_tag = questionary.text(
            f"Enter a new tag:", validate=validators.validators.RequiredValidator
        ).ask()

        if record.has_tag(new_tag):
            print(
                Fore.RED
                + f"A tag '{new_tag}' already exists. Please choose a different tag."
                + Style.RESET_ALL
            )
        else:
            break

    record.add_tag(new_tag)

    return (
        Fore.GREEN + f"Tag '{new_tag}' was added to '{title}' note." + Style.RESET_ALL
    )
