import json
import requests
from config_data import config


def hotel_detale(hotel_id: str, foto_num: int):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id		# сюда пишем id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.text)
    address = data["data"]["propertyInfo"]['summary']['location']['address']['addressLine']
    hotel_foto = [data["data"]["propertyInfo"]['propertyGallery']['images'][i]['image']['url'] for i in range(foto_num)]
    return [address, hotel_foto]


def s_hotel(city_id: str, hotel_num: int = 1, foto_num: int = 1):
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
                "max": 150,
                "min": 100
            }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        hotels_list = data["data"]["propertySearch"]['properties']
        result = {}
        for i in range(hotel_num):
            i_hotel = hotels_list[i]
            address, hotel_foto = hotel_detale(i_hotel["id"], foto_num)
            result[i_hotel["name"]] = {
                'id': i_hotel["id"],
                'price': i_hotel['price']['lead']['amount'],
                'address': address,
                'hotel_foto': hotel_foto,
                'link': f"https://www.hotels.com/ho{i_hotel['id']}"
            }
        return result
    else:
        print('Нет соединения!')
        return False
