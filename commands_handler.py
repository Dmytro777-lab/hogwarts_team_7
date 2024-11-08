from enum import Enum
from colorama import Fore, Style
import questionary


class Commands(Enum):
    EXIT = "exit"
    HELP = "help"
    CLOSE = "close"
    HELLO = "hello"

    ADD_MEMBER = "member:add"
    SHOW_MEMBER = "member:show"
    ALL_MEMBERS = "member:all"
    BIRTHDAYS = "member:birthdays"
    UPDATE_MEMBER = "member:update"
    DELETE_MEMBER = "member:delete"
    SEARCH_MEMBERS = "member:search"

    ADD_NOTE = "note:add"
    DELETE_NOTE = "note:delete"
    UPDATE_NOTE = "note:update"
    ALL_NOTES = "note:all"
    SEARCH_NOTES = "note:search"
    ADD_NOTE_TAG = "note:add:tag"
    SORT_NOTE = "note:sort"

    def __eq__(self, value: object) -> bool:
        return self.value == value


def listen_commands(book, notes, on_exit: callable):
    try:
        print(Fore.CYAN + "Welcome to the Command Center!" + Style.RESET_ALL)
        commands = [e.value for e in Commands]
        while True:
            command = questionary.autocomplete(
                "Please enter a command:", choices=commands
            ).ask()

            if command in (Commands.EXIT, Commands.CLOSE):
                on_exit(book, notes)
                print(Fore.CYAN + "Goodbye! See you next time!" + Style.RESET_ALL)
                break

            elif command == Commands.HELLO:
                print(Fore.CYAN + "How can I assist you?" + Style.RESET_ALL)

            elif command == Commands.HELP:
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

            else:
                print(Fore.RED + "Invalid command. Please try again." + Style.RESET_ALL)
    except KeyboardInterrupt:
        on_exit(book, notes)
