import re
from datetime import datetime, timedelta, date
from dataclasses import dataclass
from collections import UserDict
from helpers import (
    NotValidEmailError,
    NotValidPhoneNumberError,
    NotValidBirthdayError,
)
from typing import Optional
from colorama import Fore, Style


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Address(Field):
    pass


class Phone(Field):
    # Using a compiled regular expression to improve performance
    PHONE_NUMBER_REGEX = re.compile(r"\d{10}")

    def __init__(self, value: str):
        if not Phone.is_valid(value):
            raise NotValidPhoneNumberError(f"Invalid phone number: {value}")
        super().__init__(value)

    @staticmethod
    def is_valid(value):
        # Using a compiled regular expression
        return Phone.PHONE_NUMBER_REGEX.fullmatch(value) is not None


class Email(Field):
    # Using a compiled regular expression for email
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def __init__(self, value):
        if not Email.is_valid(value):
            raise NotValidEmailError(f"Invalid email address: {value}")
        super().__init__(value)

    @staticmethod
    def is_valid(value):
        # Using a compiled regular expression
        return Email.EMAIL_REGEX.fullmatch(value) is not None


class Birthday(Field):
    format = "%d.%m.%Y"

    def __init__(self, value):
        if not Birthday.is_valid(value):
            raise NotValidBirthdayError()

        date_object = datetime.strptime(value, Birthday.format).date()
        super().__init__(date_object)

    @staticmethod
    def is_valid(value):
        try:
            # Datetime handles leap years and dates out of month's range
            input_date = datetime.strptime(value, Birthday.format).date()
            current_date = datetime.now().date()
            # Birthday can't be in the future
            return input_date <= current_date
        except ValueError:
            # If the date is invalid, strptime will raise a ValueError
            return False


@dataclass
class Pupil:
    __address: Address = None
    __email: Email = None
    __birthday: Birthday = None
    __phone: Phone = None

    def __init__(self, name: str):
        self.name = Name(name)

    @property
    def phone(self) -> Optional[str]:
        return (
            self.__phone.value
            if self.__phone and hasattr(self.__phone, "value")
            else None
        )

    @phone.setter
    def phone(self, value: Optional[str]):
        self.__phone = Phone(value)

    @property
    def email(self) -> Optional[str]:
        return (
            self.__email.value
            if self.__email and hasattr(self.__email, "value")
            else None
        )

    @email.setter
    def email(self, value: Optional[str]):
        self.__email = Email(value)

    @property
    def birthday(self) -> Optional[date]:
        return (
            self.__birthday.value
            if self.__birthday and hasattr(self.__birthday, "value")
            else None
        )

    @birthday.setter
    def birthday(self, value: Optional[str]):
        self.__birthday = Birthday(value)

    @property
    def address(self) -> Optional[str]:
        return (
            self.__address.value
            if self.__address and hasattr(self.__address, "value")
            else None
        )

    @address.setter
    def address(self, value: Optional[str]):
        self.__address = Address(value)

    @staticmethod
    def get_fields() -> list[str]:
        return ["name", "phone", "email", "birthday", "address"]

    def __str__(self):
        return f"""\n{self.name}:
            Phone: {self.phone}
            Address: {self.address}
            Email: {self.email}
            Birthday: {self.birthday}"""


class Pupils(UserDict[str, Pupil]):

    def add_record(self, record: Pupil):
        self.data[record.name.value] = record

    def find(self, name: str) -> Pupil:
        return self.data.get(name)

    def search_pupils(self, term: str):
        term_lower = term.lower()
        results = []

        # Iterate over all records in the address book
        for record in self.data.values():
            highlighted_record = ""
            match_found = False

            for field in Pupil.get_fields():
                value = getattr(record, field, None)
                if value is not None:
                    field_value_str = str(value)
                    if isinstance(value, date):
                        field_value_str = value.strftime("%d.%m.%Y")

                    if term_lower in field_value_str.lower():
                        match_found = True
                        highlighted_value = re.sub(
                            term,
                            f"{Fore.BLUE}\\g<0>{Style.RESET_ALL}",
                            field_value_str,
                            flags=re.IGNORECASE,
                        )
                        highlighted_record += f"{highlighted_value} "
                    else:
                        highlighted_record += f"{field_value_str} "

            if match_found:
                results.append(highlighted_record.strip())

        prefix = f"Found {Fore.GREEN}{len(results)}{Style.RESET_ALL} pupil{'s' if len(results) > 1 else ''} that match your search:\n"
        return (
            prefix + "\n".join(results)
            if results
            else Fore.RED + "No match found." + Style.RESET_ALL
        )

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, delta_days: int):
        today = datetime.now().date()
        congratulations_list = []

        for name, record in self.data.items():
            if not record.birthday:
                continue

            user_birth_date_formatted = record.birthday
            user_congratulation_date = user_birth_date_formatted.replace(
                year=today.year
            )

            # if the birthday has already passed this year, check the next year's date
            # to support large delta_days
            if user_congratulation_date < today:
                user_congratulation_date = user_birth_date_formatted.replace(
                    year=today.year + 1
                )

            if 0 <= (user_congratulation_date - today).days <= delta_days:
                # adjust the date if it's on weekends
                if user_congratulation_date.weekday() in [5, 6]:
                    user_congratulation_date = (
                        user_congratulation_date + timedelta(days=2)
                        if user_congratulation_date.weekday() == 5
                        else user_congratulation_date + timedelta(days=1)
                    )
                congratulations_list.append(
                    {
                        "name": name,
                        "congratulation_date": user_congratulation_date.strftime(
                            Birthday.format
                        ),
                    }
                )

        return congratulations_list
