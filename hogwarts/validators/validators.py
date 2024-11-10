from prompt_toolkit.document import Document
from questionary import Validator, ValidationError
from hogwarts_pupils import Phone, Email, Birthday
import re


class RequiredValidator(Validator):
    def validate(self, document: Document):
        if not document.text.strip():
            raise ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )


class NumberValidation(Validator):
    def validate(self, document: Document):
        if not document.text.isnumeric():
            raise ValidationError(
                message="Invalid input. Please enter a valid integer.",
                cursor_position=len(document.text),
            )


class PhoneValidator(Validator):
    def validate(self, document: Document):
        phone_number = document.text.strip()

        # Checking for empty string
        if not phone_number:
            raise ValidationError(
                message="Phone number cannot be empty",
                cursor_position=0,
            )

        # Length and format check supporting international formats
        if not re.fullmatch(r"\+?\d{10,15}", phone_number):
            raise ValidationError(
                message="Please enter a valid phone number (10-15 digits, optional '+' prefix)",
                cursor_position=len(phone_number),
            )

        # Additional check with the Phone class (if it contains specific logic)
        if not Phone.is_valid(phone_number):
            raise ValidationError(
                message="Phone number format is invalid",
                cursor_position=len(phone_number),
            )


class EmailValidator(Validator):
    def validate(self, document: Document):
        email = document.text.strip()

        # Checking for empty string
        if not email:
            raise ValidationError(
                message="Email cannot be empty",
                cursor_position=0,
            )

        # Checking email format using Email.is_valid
        if not Email.is_valid(email):
            raise ValidationError(
                message="Please enter a valid email, e.g., example@example.com",
                cursor_position=len(email),
            )


class DateValidator(Validator):
    def validate(self, document: Document):
        if document.text and not Birthday.is_valid(document.text):
            raise ValidationError(
                message="Please enter a valid date in DD.MM.YY format, and it cannot be in the future",
                cursor_position=len(document.text),
            )
