from flask import flash
from flask_babel import gettext as _


MESSAGE = 'message'
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'


def email_already_in_use(email: str) -> None:
    flash(_("The email {email} is already in use").format(email=email), category=ERROR)


def email_not_found(email: str) -> None:
    flash(
        _("No account was found with the email address {email}").format(email=email),
        category=ERROR,
    )


def wrong_password() -> None:
    flash(_("The password is incorrect"), category=ERROR)


def incorrect_characters_in_username(username: str) -> None:
    flash(
        _(
            "The username {username} contains incorrect characters, "
            "only latin letters and numbers are allowed"
        ).format(username=username),
        category=ERROR,
    )


def username_already_in_use(username: str) -> None:
    flash(
        _("The username {username} is already in use").format(username=username),
        category=ERROR,
    )


def insecure_password() -> None:
    flash(
        _(
            "Password must be at least 8 characters long, "
            "contain at least one digit, "
            "one uppercase and one lowercase latin letter"
        ),
        category=ERROR,
    )


def successful_sign_up() -> None:
    flash(_("Well done! Now you can sign in using your credentials"), category=INFO)


def unexpected_error() -> None:
    flash(_("An unexpected error happened. Please, try again later."), category=ERROR)
