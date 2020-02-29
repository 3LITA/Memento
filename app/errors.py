class NonUniqueTitleError(Exception):
    pass


class PasswordsNotMatchError(PermissionError):
    pass


class NoPublicDeckError(Exception):
    pass


class RightsError(PermissionError):
    pass


class CreatorError(RightsError):
    pass


class AdminError(RightsError):
    pass


class RangeError(Exception):
    pass


class DoesNotExistError(Exception):
    pass


class NonUniqueSlugError(Exception):
    pass


class EmptyDeckError(Exception):
    pass
