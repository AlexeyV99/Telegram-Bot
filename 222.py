import requests

url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

querystring = {"id":"1178275040"}

headers = {
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
	"X-RapidAPI-Key": "04fed69a5cmshaa8a1712aefedb3p16964fjsn6db9f26ecde6"
}

response = requests.request("GET", url, headers=headers, params=querystring)


with open('json.txt', 'w') as f:
	f.write(response.text)



#print(response.text)
