
from aiogram.filters.state import StatesGroup, State
class NewOrder(StatesGroup):
    dishes = State()  # Состояние для хранения списка блюд
    name = State()   # Состояние для хранения имени пользователя
    time_to = State() # Время, к которому нужно приготовить заказ