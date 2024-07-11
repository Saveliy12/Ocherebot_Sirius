from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.get_dishes import get_all_dishes

# Функция для создания inline-клавиатуры
def generate_order_kb() -> InlineKeyboardBuilder:
    
    buttons = []

    # Добавление кнопок для каждого блюда
    for dish in get_all_dishes():
        button_text = f"{dish['name'].title()} • {dish['price']}"
        callback_data = f"select_dish:{dish['id']}:{dish['name']}:{dish['price']}"
        buttons.append([types.InlineKeyboardButton(text=button_text, callback_data=callback_data)])
    buttons.append([types.InlineKeyboardButton(text="➡️ Сделать заказ", callback_data="make_order")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    return keyboard

async def add_checkmark_to_dish(callback_data: str, inline_keyboard: types.InlineKeyboardMarkup, state: FSMContext) -> types.InlineKeyboardMarkup:
    # Разбиваем callback_data, чтобы получить id блюда и его имя
    _, dish_id, dish_name, dish_price = callback_data.split(":")

    # Проходимся по кнопкам в клавиатуре
    for row in inline_keyboard.inline_keyboard:
        for button in row:
            # Находим кнопку с callback_data, соответствующим id блюда
            if button.callback_data == f"select_dish:{dish_id}:{dish_name}:{dish_price}":
                # Проверяем, было ли это блюдо уже выбрано
                data = await state.get_data()
                chosen_dishes = data.get('dishes', [])
                for chosen_dish in chosen_dishes:
                    if int(dish_id) in chosen_dish:
                        # Удаляем блюдо из состояния, если оно было выбрано повторно
                        chosen_dishes.remove(chosen_dish)
                        await state.update_data(dishes=chosen_dishes)
                        # Убираем галочку (✅) рядом с названием блюда
                        button.text = button.text.replace("✅ ", "")
                        return inline_keyboard

                # Если блюдо еще не выбрано, добавляем его в состояние
                chosen_dishes.append({int(dish_id): dish_name, 'price': float(dish_price)})
                await state.update_data(dishes=chosen_dishes)
                # Устанавливаем галочку (✅) рядом с названием блюда
                button.text = f"✅ {button.text}"
                return inline_keyboard
    
    return inline_keyboard

