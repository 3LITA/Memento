class NonUniqueTitleError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PasswordsNotMatchError(PermissionError):
    def __init__(self, message):
        super().__init__(message)


class NoPublicDeckError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RightsError(PermissionError):
    def __init__(self, message):
        super().__init__(message)


class CreatorError(RightsError):
    def __init__(self, message):
        super().__init__(message)


class AdminError(RightsError):
    def __init__(self, message):
        super().__init__(message)


class RangeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DoesNotExistError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NonUniqueSlugError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EmptyDeckError(Exception):
    def __init__(self, message):
        super().__init__(message)
