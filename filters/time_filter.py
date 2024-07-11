import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

class TimeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if validate_time_format(message.text):
            return True
        else:
            return False

import re

def validate_time_format(input_time):
    # Паттерн для проверки формата времени
    time_pattern = re.compile(r'^(\d{1,2})[:](\d{2})$')
    
    # Проверка соответствия формату
    match = time_pattern.match(input_time)
    if not match:
        return False
    
    # Извлечение часов и минут из введенного времени
    hour = int(match.group(1))
    minute = int(match.group(2))
    
    # Проверка корректности часов и минут
    if hour < 0 or hour > 23:
        return False
    if minute < 0 or minute > 59:
        return False
    
    return True
