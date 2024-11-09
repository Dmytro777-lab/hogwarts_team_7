from enum import Enum
from colorama import Fore, Style
import questionary


# Enum class to define all available commands
class Commands(Enum):
    EXIT = "exit"
    HELP = "help"
    CLOSE = "close"
    HELLO = "hello"

    # Member management commands
    ADD_MEMBER = "member:add"
    SHOW_MEMBER = "member:show"
    ALL_MEMBERS = "member:all"
    BIRTHDAYS = "member:birthdays"
    UPDATE_MEMBER = "member:update"
    DELETE_MEMBER = "member:delete"
    SEARCH_MEMBERS = "member:search"

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

            # Exit commands: call on_exit callback and end the loop
            if command in (Commands.EXIT, Commands.CLOSE):
                on_exit(book, notes)
                print(Fore.CYAN + "Goodbye! See you next time!" + Style.RESET_ALL)
                break

            # Hello command: provides a friendly greeting
            elif command == Commands.HELLO:
                print(Fore.CYAN + "How can I assist you?" + Style.RESET_ALL)

            # Help command: displays a list of all available commands
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

            # Invalid command: prompts the user to try again
            else:
                print(Fore.RED + "Invalid command. Please try again." + Style.RESET_ALL)
                
    # Handle keyboard interruption (Ctrl+C) for graceful program termination
    except KeyboardInterrupt:
        on_exit(book, notes)