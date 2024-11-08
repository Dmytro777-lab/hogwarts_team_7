class NotValidPhoneNumberError(Exception):
    def __init__(self, message="Phone number must be 10 digits."):
        self.message = message
        super().__init__(self.message)


class NotValidEmailError(Exception):
    def __init__(self, message="Please enter a valid email, e.g. example@example.com"):
        self.message = message
        super().__init__(self.message)


class NotValidBirhdayError(Exception):
    def __init__(self, message="Please enter a valid date in DD.MM.YY format, and it cannot be in the future"):
        self.message = message
        super().__init__(self.message)


class ContactsError(Exception):
    def __init__(self, message="Contact doesn't exist"):
        self.message = message
        super().__init__(self.message)


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
