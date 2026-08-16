import requests

def get_weather(address="Thanh Hoa"):
   import requests
from urllib.parse import quote

API_KEY = "25f070cf4a2f5ba0b92a64352809bacf"


def get_weather(address="Thanh Hoa"):

    city = quote(address)

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},VN"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    print("URL =", url)

    response = requests.get(url)

    print("STATUS =", response.status_code)

    data = response.json()

    print("DATA =", data)

    return data