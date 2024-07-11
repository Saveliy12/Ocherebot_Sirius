import re
from aiogram.filters import BaseFilter
from aiogram.types import Message

class NameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if validate_username(message.text):
            return True
        else:
            return False

def validate_username(username: str) -> bool:
    # Проверка на количество слов
    if len(username.split()) < 2:
        return False

    # Проверка на минимальную длину каждого слова
    words = username.split()
    if len(words[0]) < 2 or len(words[1]) < 2:
        return False

    # Проверка, что строка состоит только из кириллицы или латиницы
    if not re.match(r'^[a-zA-Zа-яА-Я\s]+$', username):
        return False

    return True
