import json
import requests

# {'name': 'asd ', 'time': '12:12', 'price': '150р.', 'ids': ['1']}
def send_order(name, time, price, ids):
    # Собираем id названий блюд
    dishes_str = extract_dish_ids(ids)

    # Формируем JSON
    order_data = {
        "name": name,
        "time": time,
        "price": price,
        "ids": dishes_str
    }

    res = json.dumps(order_data)
    print(res)

    # Отправляем POST-запрос
    url = "http://localhost:8001/api/order/post"
    try:
        response = requests.post(url, json=order_data)
        response.raise_for_status()  # Проверяем статус ответа
        print("Заказ успешно отправлен!")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке заказа: {e}")


def extract_dish_ids(data: list) -> list:
    dish_ids = set()
    for sublist in data:
        for item in sublist:
            if isinstance(item, int):
                dish_ids.add(str(item))
    return sorted(list(dish_ids))