import questionary


def ask_contact_name(book) -> str:
    return questionary.autocomplete(
        "Enter a contact name:", choices=[*book.keys()]
    ).ask()
