from aiogram import Bot, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.order import generate_order_kb, add_checkmark_to_dish
from states.order import NewOrder
from database.post_order import send_order
from utils.validate_order import validate_order
from filters.name_filter import NameFilter
from filters.time_filter import TimeFilter

order_router = Router()

@order_router.message(Command("order"))
async def order_handler(msg: Message, state: FSMContext):
    await msg.reply("Выберите блюда для заказа:", reply_markup=generate_order_kb())
    await state.set_state(NewOrder.dishes)

@order_router.callback_query(NewOrder.dishes)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if callback_query.data.startswith("select_dish"):

        dish_name = callback_query.data.split(":")[2]

        # Обработка выбора блюда
        await bot.answer_callback_query(callback_query.id, f"Выбрано блюдо - {dish_name}")

        # Добавляем галочку к выбранному блюду
        inline_keyboard = callback_query.message.reply_markup
        await add_checkmark_to_dish(callback_query.data, inline_keyboard, state)
        
        # Обновляем сообщение с клавиатурой, чтобы показать галочку
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=inline_keyboard)
        
        
    elif callback_query.data == "make_order":

        # Удаление клавиатуры из сообщения
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=None)

        # Изменение текста сообщения
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Продолжите оформление заказа")

        # Считаем общую сумму всех выбранных блюд
        total_price = sum([dish['price'] for dish in data.get('dishes', [])])

        # Сохраняем общую сумму в состояние
        data['total_price'] = total_price
        await state.update_data(data)

        # Обработка кнопки "Сделать заказ"
        await bot.answer_callback_query(callback_query.id, f"Вы сделали заказ!\nОбщая сумма: {total_price}")

        # Запрос имени пользователя
        await callback_query.message.answer("Введите ваше имя и фамилию:")
        
        # Установка состояния name для запроса имени пользователя
        await state.set_state(NewOrder.name)
    else:
        await bot.answer_callback_query(callback_query.id, "Неизвестное действие")


@order_router.message(NewOrder.name, NameFilter())
async def process_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)

    # Запрос времени, к которому приготовить заказ
    await message.answer(text="Теперь укажите время, во сколько вы заберете заказ в формате hh:mm")

    # Установка состояния time_to для запроса времени, к которому приготовить заказ
    await state.set_state(NewOrder.time_to)

@order_router.message(NewOrder.name)
async def process_name(message: Message):
    await message.answer(text="Сообщение должно содержать имя и фамилию через пробел!. Только латиница и кириллица\n\nВведите имя и фамилию:")

@order_router.message(NewOrder.time_to, TimeFilter())
async def process_time(message: Message, state: FSMContext):

    # Сохранение имени пользователя в состоянии
    await state.update_data(time_to=message.text)

    # Извлечение данных из состояния
    data = await state.get_data()
    dishes_list = data.get('dishes', [])
    name = data.get('name')
    total_price = data.get('total_price')
    time_to = data.get('time_to')

    print(f"dishes_list - {dishes_list}")

    send_order(name, time_to, total_price, dishes_list)

    # запрос в меню - гет запрос для получения актуального меню
    # запрос в ордер - пост запрос для добавления в таблицу ордер заказа
    # валидация имени и времени

    # Обработка заказа
    await message.answer(f"Спасибо за заказ!\n\n👤 Имя: <b>{name}</b>\n🍲 Блюда:\n<b>{validate_order(dishes_list)}</b>\n💳 Сумма заказа: <b>{total_price} ₽</b>\n🕙 Время получения: <b>{time_to}</b>\n\nПри получении заказа назовите своё имя")
    # Сброс состояния
    await state.clear()

@order_router.message(NewOrder.time_to)
async def process_name(message: Message):
    await message.answer(text="Неверный формат времени!\n\nВведенное время должно соответствовать формату hh:mm")
