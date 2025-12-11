# web_interface/NetworkHelper.py
import requests
from requests.auth import HTTPBasicAuth


class NetworkHelper:
    def __init__(self, base_url, username, password):
        # base_url очікується, наприклад: "http://127.0.0.1:8001/api"
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)

    def get_list(self, endpoint):
        """1. GET List: Отримати список всіх об'єктів"""
        try:
            url = f"{self.base_url}/{endpoint}/"
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"API Error (Get List): {e}")
            return []

    def get_item(self, endpoint, item_id):
        """2. GET Item: Отримати один об'єкт за ID"""
        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"API Error (Get Item): {e}")
            return None

    def create_item(self, endpoint, data):
        """3. POST: Створити новий об'єкт"""
        try:
            url = f"{self.base_url}/{endpoint}/"
            response = requests.post(url, json=data, auth=self.auth)
            return response.status_code == 201
        except Exception as e:
            print(f"API Error (Create): {e}")
            return False

    def update_item(self, endpoint, item_id, data):
        """4. PUT: Оновити об'єкт"""
        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.put(url, json=data, auth=self.auth)
            return response.status_code == 200
        except Exception as e:
            print(f"API Error (Update): {e}")
            return False

    def delete_item(self, endpoint, item_id):
        """5. DELETE: Видалити об'єкт"""
        try:
            url = f"{self.base_url}/{endpoint}/{item_id}/"
            response = requests.delete(url, auth=self.auth)
            # 204 No Content - стандарт успішного видалення
            return response.status_code == 204
        except Exception as e:
            print(f"API Error (Delete): {e}")
            return False
