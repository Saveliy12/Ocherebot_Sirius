import sqlite3
import requests

def execute(sql):
    try:
        connection = sqlite3.connect("db.sqlite3")
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result
    except Exception as e:
        print(f'{e}')

def get_all_dishes() -> list:
    try:
        menu_url = "http://localhost:8001/api/menu/get"
        response = requests.get(menu_url)

        data = response.json()
        print(data)
        return data
    except Exception as e:
        print(f"Ошибка получения меню{e}")

def transform_data(input_data):
    transformed_data = []
    for item in input_data:
        transformed_item = {
            'id': item['id'],
            'name': item['name'],
            'type': item['type'],
            'price': str(int(item['price'])) if item['price'].is_integer() else str(item['price'])
        }
        transformed_data.append(transformed_item)
    return transformed_data
