def validate_order(data: list) -> str:
    result = ''

    if not isinstance(data, list):
        print("Ошибка: Неверный формат данных. Ожидался список.")
        return result

    for item in data:
        if not isinstance(item, dict):
            print("Ошибка: Неверный формат элемента списка. Ожидался словарь.")
            continue

        dish_name = next((value for key, value in item.items() if isinstance(value, str)), None)
        if not dish_name:
            print("Ошибка: Не удалось найти название блюда в элементе списка.")
            continue

        result += f"- {dish_name.title()}\n"

    return result
