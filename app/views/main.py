from typing import Union

from flask import render_template
from flask_login import current_user, login_required

from app.models.User import User
from app.server import web
from app.settings import URLS


@web.route(URLS.INDEX)
def index() -> Union[bytes, str]:
    return render_template('public/index.html')


@web.route(URLS.PROFILE)
@login_required
def profile() -> Union[bytes, str]:
    user: User = current_user
    return render_template('public/profile.html', username=user.username)
