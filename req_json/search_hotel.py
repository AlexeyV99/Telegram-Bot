from req_json.search_hotel_detale import hotel_detale
from req_json.api_request import api_request
from loguru import logger


def s_hotel(city_id: str, hotel_num: int) -> dict or None:
    """
    Функция поиска отелей в выбранном городе
    :param city_id: str
    :return: dict or None
    """
    logger.info(f'Пользователь выполнил команду "s_hotel"')
    params = {
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

    data = api_request(method_endswith='properties/v2/list', params=params, method_type="POST")

    if data['data']:
        hotels_list = data["data"]["propertySearch"]['properties']
        result = {}
        for i_hotel in hotels_list:

            result[i_hotel["id"]] = {
                'name': i_hotel["name"],
                'price': i_hotel['price']['lead']['amount'],
                'f_price': i_hotel['price']['lead']['formatted'],

                'link': f"https://www.hotels.com/h{i_hotel['id']}.Hotel-Information"
            }

        # на тот случай, если отелей в городе меньше, чем было в запросе
        i_num_hotel = 1
        result_num = {}
        for i_code, i_hotel in result.items():
            if i_num_hotel > hotel_num:
                return result_num
            result_num[i_code] = i_hotel
            address, hotel_foto = hotel_detale(i_code)
            result_num[i_code]['address'] = address
            result_num[i_code]['hotel_foto'] = hotel_foto
            i_num_hotel += 1
        return result_num
    else:
        return None

