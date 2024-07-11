from aiogram import  Router
from aiogram.types import Message
from aiogram.filters import Command
start_router = Router()

@start_router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет!\n\nС помощью этого бота вы сможете сделать заказ в столовой НТУ Сириус «Вега»\n\nСделать заказ - /order")