class IncorrectCharacters(Exception):
    pass


class TooLongError(Exception):
    pass


class NotUnique(Exception):
    pass


class EmptyDeck(Exception):
    pass


class PasswordError(Exception):
    pass


class TooShortPassword(PasswordError):
    pass


class NoNumber(PasswordError):
    pass


class NoCapitalLetter(PasswordError):
    pass


class NoLowercaseLetter(PasswordError):
    pass


class EmailAlreadyUsed(NotUnique):
    pass


class UsernameAlreadyUsed(NotUnique):
    pass


class NotFound(Exception):
    pass
