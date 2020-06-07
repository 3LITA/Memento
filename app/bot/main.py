import telebot
from telebot import types

from app.bot.keyboard import markups
from app.settings import dist
from app.settings.local import TOKEN

from . import utils, replies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=dist.BOT_COMMANDS['start_commands'])
def start_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    if user.inline_keyboard_id:
        try:
            bot.delete_message(user.chat_id, user.inline_keyboard_id)
        except telebot.apihelper.ApiException:
            print(
                "Not found message %s for user %s" % (user.inline_keyboard_id, user.id)
            )  # logging
        user.forget_keyboard()
        text = replies.START_AGAIN.format(message.from_user.first_name)
    else:
        text = replies.START_REPLY.format(message.from_user.first_name)

    keyboard = markups.main_menu_markup(user.has_decks())
    message_id = bot.send_message(
        chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode='Markdown'
    ).message_id
    user.set_inline_keyboard(message_id)


@bot.message_handler(commands=dist.BOT_COMMANDS['help_commands'])
def help_handler(message: types.Message) -> None:
    utils.get_user(message)
    text = replies.HELP_REPLY
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=dist.BOT_COMMANDS['menu_commands'])
def menu_handler(message: types.Message) -> None:
    user = utils.get_user(message)
    if user.inline_keyboard_id:
        try:
            bot.delete_message(message.chat.id, user.inline_keyboard_id)
        except telebot.apihelper.ApiException:
            print(
                "Not found message %s for user %s" % (user.inline_keyboard_id, user.id)
            )  # logging
            user.forget_keyboard()

    text = replies.MENU_REPLY
    keyboard = markups.main_menu_markup(user.has_decks())

    message_id = bot.send_message(
        message.chat.id, text, reply_markup=keyboard
    ).message_id
    user.set_inline_keyboard(message_id)


@bot.message_handler(commands=dist.BOT_COMMANDS['expectations_commands'])
def expectations_handler(message: types.Message) -> None:
    print(utils.expectations)


@bot.message_handler(regexp=r'^/.*')
def unknown_command_handler(message: types.Message) -> None:
    text = replies.UNKNOWN_COMMAND_REPLY
    print(
        "%s tried to send a non-existing command %s" % (message.chat.id, message.text)
    )
    bot.send_message(message.chat.id, text)
