from prompt_toolkit.document import Document
from questionary import Validator, ValidationError
from users import Phone, Email
import re

class PhoneValidator(Validator):
    def validate(self, document: Document):
        phone_number = document.text.strip()
        
        # Checking for empty strin
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