# Created by https://t.me/vlasovdev message file | Создано https://t.me/vlasovdev message file


import json

from aiogram.types import Message


class MessageUtils:
    @staticmethod
    def dump(message: Message) -> str:
        return message.json()

    @staticmethod
    def load(message: str) -> Message:
        return Message(**json.loads(message))
