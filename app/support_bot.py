from typing import Any

from telebot import TeleBot

from app import settings


bot = TeleBot(settings.SUPPORT_BOT_TOKEN)


def report(message: str, customer: Any) -> None:
    bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID,
        text=f"Customer {customer.id} reports:\n\n{message}",
    )


def notify_critical_error(error_message: Exception) -> None:
    bot.send_message(
        chat_id=settings.ADMIN_CHAT_ID,
        text=f"Critical error occurred:\n\n{error_message}",
    )
