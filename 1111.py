import requests
from pprint import pprint




url = "https://hotels4.p.rapidapi.com/properties/list"

querystring = {"destinationId": "1506246",
               "pageNumber": "1",
               "pageSize": "3",
               "checkIn": "2020-01-08",
               "checkOut": "2020-01-15",
               "adults1": "1",
               "sortOrder": "PRICE",
               "locale": "us_US",
               "currency": "USD"}

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "04fed69a5cmshaa8a1712aefedb3p16964fjsn6db9f26ecde6"
}

try:
    r = requests.request("GET", url, headers=headers, params=querystring)
    data = r.json()
    print(data)
    # if data['moresuggestions'] == 0:
    #     print('Такого города не существует')
    # else:
    #     for i_data in data['suggestions']:
    #         if i_data['group'] == 'CITY_GROUP':
    #             for i_city in i_data['entities']:
    #                 print(i_city['caption'], i_city['destinationId'])
except Exception as e:
    print(e)
