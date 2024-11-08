from prompt_toolkit.document import Document 
from questionary import Validator, ValidationError 
from users import Phone, Email

class PhoneValidator(Validator):
    def validate(self, document: Document):
        if document.text and not Phone.is_valid(document.text):
            raise ValidationError(
                message="Please enter a 10-digit phone number",
                cursor_position=len(document.text),
            )
        
class EmailValidator(Validator):
    def validate(self, document: Document):
        if document.text and not Email.is_valid(document.text):
            raise ValidationError(
                message="Please enter a valid email, e.g. example@example.com",
                cursor_position=len(document.text),
            )
