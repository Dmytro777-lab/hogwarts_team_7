# Custom exception for invalid phone numbers
class NotValidPhoneNumberError(Exception):
    def __init__(self, message="Phone number must be 10 digits."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotValidPhoneNumberError: {self.message}"


# Custom exception for invalid email addresses
class NotValidEmailError(Exception):
    def __init__(self, message="Please enter a valid email, e.g., example@example.com"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotValidEmailError: {self.message}"


# Custom exception for invalid birthday dates
class NotValidBirthdayError(Exception):
    def __init__(self, message="Please enter a valid date in DD.MM.YY format, and it cannot be in the future"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotValidBirthdayError: {self.message}"


# Custom exception for missing contacts
class ContactsError(Exception):
    def __init__(self, message="Contact doesn't exist"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ContactsError: {self.message}"


# Custom exception for missing notes
class NotesError(Exception):
    def __init__(self, message="No notes found."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotesError: {self.message}"


# Decorator to handle various exceptions and prevent code from breaking on errors
def input_error(func):
    def inner(*args, **kwargs):
        try:
            # Try to execute the function and return its result if no errors occur
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError,
                NotValidPhoneNumberError, NotValidEmailError,
                NotValidBirthdayError, ContactsError, NotesError) as e:
            # Return the exception object if an error occurs
            return e

    return inner