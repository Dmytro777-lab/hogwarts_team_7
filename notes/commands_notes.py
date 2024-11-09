import questionary
from colorama import Fore, Style

import validators
from helpers import input_error, NotesError 
from notes import Notes, NoteRecord, SearchBy

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
        "What is the content for your note?", validate=validators.validators.RequiredValidator
    ).ask()

    record = NoteRecord(title, content)
    notes_list.add_record(record)

    return (
        Fore.GREEN + f"Note titled '{title}' is added." + Style.RESET_ALL
    )


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
            Fore.RED
            + f"Note titled '{title}'is not found."
            + Style.RESET_ALL
        )

    notes_list.delete(title)
    return (
        Fore.RED
        + f"Note titled '{title}' has been deleted."
        + Style.RESET_ALL
    )


@input_error
def update_note(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(
            Fore.RED + "There are no notes." + Style.RESET_ALL
        )

    title = questionary.autocomplete(
        "What is the title of the note you wish to update?",
        choices=[*notes_list.keys()],
        validate=validators.validators.RequiredValidator,
    ).ask()
    record = notes_list.find(title)

    if not record:
        return NotesError(
            Fore.RED
            + f"Note titled '{title}' is not found."
            + Style.RESET_ALL
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

    return (
        Fore.GREEN
        + f"Note titled '{title}' has been updated."
        + Style.RESET_ALL
    )


@input_error
def search_notes(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(
            Fore.RED + "There are no notes." + Style.RESET_ALL
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



@input_error
def show_notes(notes_list: Notes):
    if notes_list.is_empty():
        raise NotesError(
            Fore.RED + "There are no notes." + Style.RESET_ALL
        )

    return notes_list.list_notes()