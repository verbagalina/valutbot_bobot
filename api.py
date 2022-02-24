import json
import requests
from config import money

class APIexception(Exception):
    pass

class Convert:
    @staticmethod #преобразуем значения
    def get_price(base, quote, amount):
        b = money[base]
        q = money[quote]
        a = float(amount)
        result = requests.get(f"https://free.currconv.com/api/v7/convert?q={b}_{q},{q}_{b}&compact=ultra&apiKey=c7cb4db2343e21cb892a")
        result = json.loads(result.content)
        return round(a * result[f"{b}_{q}"], 2)

