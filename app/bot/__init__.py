from telebot import TeleBot

from app import settings


bot = TeleBot(settings.TOKEN)

__all__ = ['bot', 'contexts', 'main', 'replies', 'utils']
