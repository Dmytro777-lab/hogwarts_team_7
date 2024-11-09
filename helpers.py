class NotValidPhoneNumberError(Exception):
    def __init__(self, message="Phone number must be 10 digits."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotValidPhoneNumberError: {self.message}"


class NotValidEmailError(Exception):
    def __init__(self, message="Please enter a valid email, e.g., example@example.com"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotValidEmailError: {self.message}"


class NotValidBirthdayError(Exception):
    def __init__(self, message="Please enter a valid date in DD.MM.YY format, and it cannot be in the future"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"NotValidBirthdayError: {self.message}"


class ContactsError(Exception):
    def __init__(self, message="Contact doesn't exist"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ContactsError: {self.message}"


class NotesError(Exception):
    def __init__(self, message="No notes found."):
        self.message = message
        super().__init__(self.message)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except IndexError as e:
            return e
        except KeyError as e:
            return e
        except NotValidPhoneNumberError as e:
            return e
        except NotValidEmailError as e:
            return e
        except NotValidBirhdayError as e:
            return e
        except ContactsError as e:
            return e
        except NotesError as e:
            return e

    return inner
