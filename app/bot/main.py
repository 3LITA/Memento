import telebot
from telebot import types

from app.locale import replies
from app.settings import dist
from app.settings.local import TOKEN

from . import markups, utils


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=dist.COMMANDS.get('start_commands'))
def start_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    keyboard = markups.create_menu_markup(user)
    if user.inline_keyboard_id:
        text = replies.START_AGAIN.format(message.from_user.first_name)
        bot.delete_message(user.chat_id, user.inline_keyboard_id)
    else:
        text = replies.START_REPLY.format(message.from_user.first_name)
    bot.send_message(
        chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode='Markdown'
    )


@bot.message_handler(commands=dist.COMMANDS.get('help_commands'))
def help_handler(message: types.Message) -> None:
    utils.get_user(message)
    text = replies.HELP_REPLY
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=dist.COMMANDS.get('menu_commands'))
def menu_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    if user.inline_keyboard_id:
        try:
            bot.delete_message(message.chat.id, user.inline_keyboard_id)
        except telebot.apihelper.ApiException:
            user.forget_keyboard()

    text = replies.MENU_REPLY
    keyboard = markups.create_menu_markup(user)

    message_id = bot.send_message(
        message.chat.id, text, reply_markup=keyboard
    ).message_id
    user.set_inline_keyboard(message_id)


@bot.message_handler(commands=dist.COMMANDS.get('expectations_commands'))
def expectations_handler(message: types.Message) -> None:
    print(utils.expectations)


@bot.message_handler(regexp=r'^/.*')
def unknown_handler(message: types.Message) -> None:
    text = replies.UNKNOWN_COMMAND_REPLY
    bot.send_message(message.chat.id, text)
