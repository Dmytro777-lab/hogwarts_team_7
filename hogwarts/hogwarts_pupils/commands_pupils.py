import questionary
from tabulate import tabulate
from colorama import Fore, Style, init

import validators
from .hogwarts_pupils import Pupils, Pupil
from helpers import ContactsError, input_error
import validators.ask_name

init()


@input_error
def add_pupil(list: Pupils):
    name = questionary.text(
        "Enter the name of the pupil:",
        validate=validators.validators.RequiredValidator,
    ).ask()
    message = Fore.LIGHTGREEN_EX + "New pupil added." + Style.RESET_ALL
    contact = list.find(name)
    if contact:
        if questionary.confirm(
            "This pupil already exists. Do you want to update their details?"
        ).ask():
            message = (
                Fore.LIGHTGREEN_EX
                + "Pupil details have been updated."
                + Style.RESET_ALL
            )
        else:
            return (
                Fore.LIGHTRED_EX + "The addition of the pupil failed." + Style.RESET_ALL
            )

    contact = contact or Pupil(name)
    list.add_record(contact)
    form = questionary.form(
        address=questionary.text("[Optional] Enter address:"),
        phone=questionary.text(
            "[Optional] Enter phone number:",
            validate=validators.validators.PhoneValidator,
        ),
        email=questionary.text(
            "[Optional] Enter email address:",
            validate=validators.validators.EmailValidator,
        ),
        birthday=questionary.text(
            "[Optional] Enter birthday (DD.MM.YYYY):",
            validate=validators.validators.DateValidator,
        ),
    )
    fields = form.ask()

    for field, value in fields.items():
        if value:
            setattr(contact, field, value)

    return message


@input_error
def update_pupil(list: Pupils) -> str:
    name = validators.ask_name.ask_contact_name(list)
    record = list.find(name)
    if record is None:
        raise ContactsError(Fore.RED + "This pupil does not exist." + Style.RESET_ALL)

    field = questionary.autocomplete(
        "Which detail would you like to update?", choices=Pupil.get_fields()
    ).ask()
    if hasattr(record, field):
        new_value = questionary.text(
            f"Enter the new value for {field}:",
            validate=validators.validators.RequiredValidator,
        ).ask()
        setattr(record, field, new_value)

        return (
            Fore.GREEN
            + f"{field.capitalize()} has been updated for this pupil."
            + Style.RESET_ALL
        )
    else:
        raise ContactsError(
            Fore.RED
            + f"Field '{field}' does not exist for this pupil."
            + Style.RESET_ALL
        )


@input_error
def delete_pupil(list: Pupils) -> str:
    name = validators.ask_name.ask_contact_name(list)
    record = list.find(name)

    if record is None:
        raise ContactsError(Fore.RED + "This pupil does not exist." + Style.RESET_ALL)

    list.delete(name)

    return Fore.GREEN + f"{name} has been removed from the list." + Style.RESET_ALL


@input_error
def show_pupil(pupils_list: Pupils) -> str:
    name = questionary.autocomplete(
        "Enter the name of the pupil to view:", choices=[*pupils_list.keys()]
    ).ask()
    contact = pupils_list.find(name)

    if contact is None:
        raise ContactsError(
            Fore.RED + f"{name} is not found in the list." + Style.RESET_ALL
        )

    return str(contact)


@input_error
def all_pupils(pupils_list: Pupils) -> str:
    if not pupils_list:
        raise ContactsError(
            Fore.RED + "The list is empty! No pupils found." + Style.RESET_ALL
        )

    table_data = []
    command_output = Fore.CYAN + "Here is the list of all pupils:\n" + Style.RESET_ALL

    for name, contact in pupils_list.items():
        name = Fore.LIGHTBLUE_EX + name + Style.RESET_ALL
        address = contact.address
        if address is None:
            address = Fore.RED + "Homeless" + Style.RESET_ALL
        else:
            address = Fore.GREEN + address + Style.RESET_ALL
        email = contact.email
        if email is None:
            email = Fore.RED + "No email" + Style.RESET_ALL
        else:
            email = Fore.GREEN + email + Style.RESET_ALL
        phone = contact.phone
        if phone is None:
            phone = Fore.RED + "No phone" + Style.RESET_ALL
        else:
            phone = Fore.GREEN + phone + Style.RESET_ALL
        birthday = contact.birthday
        if birthday is None:
            birthday = Fore.RED + "Unborn" + Style.RESET_ALL
        else:
            birthday = Fore.GREEN + birthday.strftime("%d/%m/%Y") + Style.RESET_ALL
        table_data.append([name, phone, email, address, birthday])
        headers = [
            Fore.LIGHTYELLOW_EX + "Pupil" + Style.RESET_ALL,
            Fore.LIGHTYELLOW_EX + "Phone" + Style.RESET_ALL,
            Fore.LIGHTYELLOW_EX + "Email" + Style.RESET_ALL,
            Fore.LIGHTYELLOW_EX + "Address" + Style.RESET_ALL,
            Fore.LIGHTYELLOW_EX + "Birthday" + Style.RESET_ALL,
        ]
        command_output = tabulate(table_data, headers=headers, tablefmt="grid")

    return command_output


@input_error
def pupils_birthdays(list: Pupils) -> str:
    if not list:
        raise ContactsError(
            Fore.RED + "The list is empty! No pupils found." + Style.RESET_ALL
        )

    try:
        delta_days = int(
            questionary.text(
                "How many days ahead would you like to check for upcoming birthdays?",
                validate=validators.validators.NumberValidation,
            ).ask()
        )
        birthdays_list = list.get_upcoming_birthdays(delta_days)

        if not birthdays_list:
            return (
                Fore.RED
                + f"No birthdays in the next {delta_days} days."
                + Style.RESET_ALL
            )

        table_data = []
        for contact in birthdays_list:
            name = Fore.LIGHTBLUE_EX + contact["name"] + Style.RESET_ALL
            congrats_date = (
                Fore.GREEN + contact["congratulation_date"] + Style.RESET_ALL
            )
            table_data.append([name, congrats_date])

        headers = [
            Fore.LIGHTYELLOW_EX + "Pupil Name" + Style.RESET_ALL,
            Fore.LIGHTYELLOW_EX + "Birthday" + Style.RESET_ALL,
        ]

        output = tabulate(table_data, headers=headers, tablefmt="grid")
        return output

    except ValueError:
        return (
            Fore.RED + "Invalid number! Please enter a valid integer." + Style.RESET_ALL
        )


@input_error
def search_pupil(list: Pupils) -> str:
    if not list:
        raise ContactsError(
            Fore.RED + "The list is empty! No pupils found." + Style.RESET_ALL
        )

    search_input = questionary.text(
        "Enter the search term:",
        validate=validators.validators.RequiredValidator,
    ).ask()

    return list.search_pupils(search_input)
