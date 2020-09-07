import logging

from flask import Response, make_response, redirect, render_template, request
from flask_login import login_required, login_user, logout_user
from werkzeug import wrappers

from app import exceptions, support_bot
from app.models.User import User
from app.server import login_manager, web
from app.settings import URLS

from . import flashes


login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.get(user_id)


@web.route(URLS.LOGOUT, methods=["GET"])
@login_required
def logout() -> wrappers.Response:
    logout_user()
    return redirect(URLS.INDEX)


@web.route(URLS.LOGIN, methods=["GET"])
def login() -> wrappers.Response:
    response: Response = make_response(render_template("public/login.html"))
    chat_id = request.args.get('chat_id')
    if chat_id:
        response.set_cookie('chat_id', str(chat_id))
        logging.info("Setting cookie for chat_id=%s", chat_id)
    return response


@web.route(URLS.SIGN_IN, methods=["POST"])
def sign_in() -> wrappers.Response:
    email = request.form['email']
    password = request.form['password']
    remember = True if request.form.get('remember') else False
    try:
        user = User.login(email, password)
    except exceptions.NotFound:
        flashes.email_not_found(email)
    except exceptions.PasswordError:
        flashes.wrong_password()
    else:
        login_user(user, remember=remember)
        return redirect(URLS.PROFILE)
    return redirect(URLS.LOGIN)


@web.route(URLS.SIGN_UP, methods=["POST"])
def sign_up() -> wrappers.Response:
    username = request.form['username']
    email = request.form['email']
    password = request.form['password1']

    chat_id = None
    try:
        chat_id = int(request.cookies['chat_id'])
    except KeyError:
        pass
    except ValueError:
        pass

    logging.info("Got chat_id=%s from cookie", chat_id)

    try:
        user = User(email, password, username, chat_id)
    except exceptions.EmailAlreadyUsed:
        flashes.email_already_in_use(email)
    except exceptions.IncorrectCharacters:
        flashes.incorrect_characters_in_username(username)
    except exceptions.UsernameAlreadyUsed:
        flashes.username_already_in_use(username)
    except exceptions.PasswordError:
        flashes.insecure_password()
    except Exception as e:
        support_bot.notify_critical_error(e)
        logging.critical(e)
        flashes.unexpected_error()
    else:
        if chat_id:
            from app.bot import send_greetings

            send_greetings(user=user)
        flashes.successful_sign_up()
    return redirect(URLS.LOGIN)
