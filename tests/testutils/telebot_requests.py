from dataclasses import dataclass
from typing import Optional


MARKDOWN = 'Markdown'

SEND_MESSAGE = 'send_message'
EDIT_MESSAGE = 'edit_message'
DELETE_MESSAGE = 'delete_message'


@dataclass
class Request:
    action: str
    chat_id: int
    text: Optional[str] = None
    reply_markup: Optional[dict] = None
    parse_mode: Optional[str] = None
