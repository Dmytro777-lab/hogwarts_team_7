from enum import Enum
from colorama import Fore, Style
import questionary

from hogwarts_pupils import *
from hogwarts_notes import *


# Enum class to define all available commands
class Commands(Enum):
    EXIT = "exit"
    HELP = "help"
    CLOSE = "close"
    HELLO = "hello"

    # Pupils management commands
    ADD_PUPIL = "pupil:add"
    SHOW_PUPIL = "pupil:show"
    ALL_PUPILS = "pupil:all"
    BIRTHDAYS = "pupil:birthdays"
    UPDATE_PUPIL = "pupil:update"
    DELETE_PUPIL = "pupil:delete"
    SEARCH_PUPILS = "pupil:search"

    # Note management commands
    ADD_NOTE = "note:add"
    DELETE_NOTE = "note:delete"
    UPDATE_NOTE = "note:update"
    ALL_NOTES = "note:all"
    SEARCH_NOTES = "note:search"
    ADD_NOTE_TAG = "note:add:tag"
    SORT_NOTE = "note:sort"

    # Override equality operator to allow direct comparison with string command values
    def __eq__(self, value: object) -> bool:
        return self.value == value


# Function to handle user commands and continuously prompt for input
def listen_commands(book, notes, on_exit: callable):
    try:
        # Welcome message with color formatting
        print(Fore.CYAN + "Welcome to the Command Center!" + Style.RESET_ALL)

        # Retrieve a list of all command values for autocomplete
        commands = [e.value for e in Commands]

        # Main command input loop
        while True:
            # Prompt user for a command with autocomplete suggestions
            command = questionary.autocomplete(
                "Please enter a command:", choices=commands
            ).ask()

            # Using match-case to handle command execution
            match command:
                # Exit commands: call on_exit callback and end the loop
                case Commands.EXIT | Commands.CLOSE:
                    on_exit(book, notes)
                    print(Fore.CYAN + "Goodbye! See you next time!" + Style.RESET_ALL)
                    break

                # Hello command: provides a friendly greeting
                case Commands.HELLO:
                    print(Fore.CYAN + "How can I assist you?" + Style.RESET_ALL)

                # Help command: displays a list of all available commands
                case Commands.HELP:
                    print(
                        "\n- ".join(
                            [
                                Fore.CYAN
                                + "Here are the available commands:"
                                + Style.RESET_ALL,
                                *commands,
                            ]
                        )
                    )

                # Pupil management commands
                case Commands.ADD_PUPIL:
                    print(add_pupil(book))

                case Commands.SHOW_PUPIL:
                    print(show_pupil(book))

                case Commands.ALL_PUPILS:
                    print(all_pupils(book))

                case Commands.BIRTHDAYS:
                    print(pupils_birthdays(book))

                case Commands.UPDATE_PUPIL:
                    print(update_pupil(book))

                case Commands.DELETE_PUPIL:
                    print(delete_pupil(book))

                case Commands.SEARCH_PUPILS:
                    print(search_pupil(book))

                # Note management commands
                case Commands.ADD_NOTE:
                    print(add_note(notes))

                case Commands.UPDATE_NOTE:
                    print(update_note(notes))

                case Commands.DELETE_NOTE:
                    print(delete_note(notes))

                case Commands.ALL_NOTES:
                    print(show_notes(notes))

                case Commands.SEARCH_NOTES:
                    print(search_notes(notes))
                case Commands.SORT_NOTE:
                    print(sort_notes(notes))
                case Commands.ADD_NOTE_TAG:
                    print(add_tag(notes))

                # Invalid command: prompts the user to try again
                case _:
                    print(
                        Fore.RED
                        + "Invalid command. Please try again."
                        + Style.RESET_ALL
                    )
    # Handle keyboard interruption (Ctrl+C) for graceful program termination
    except KeyboardInterrupt:
        on_exit(book, notes)
