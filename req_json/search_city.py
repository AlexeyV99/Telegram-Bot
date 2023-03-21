import json
import requests
from config_data import config


def s_city(city: str):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {
        "q": city,
        "locale": "ru_RU",
        "langid": "1033",
        "siteid": "300000001"
    }

    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
    if response.status_code == 200:
        data = json.loads(response.text)
        if not data['sr']:
            print('Нет такого города!')
            return False

        result = {i_city["essId"]["sourceId"]: i_city["regionNames"]["displayName"] for i_city in data['sr']}
        return result
    else:
        print('Нет соединения!')
        return False
