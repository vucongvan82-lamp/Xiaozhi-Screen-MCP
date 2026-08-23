from services.weather_service import get_weather
from datetime import datetime


def idle_weather(
        address="",
        save_location=False,
        esp_id=""):
    
    data = get_weather(address)

    now = datetime.now()

    main = data.get("main", {})
    temp = main.get("temp")
    humidity = main.get("humidity")

    location = address if address else "Chưa cài đặt"

    return {
        "Trợ lý ảo": "Gia Vũ",
        "Ngày": f'{now.strftime("%d/%m/%Y")} - {now.strftime("%H:%M:%S")}',
        "Tỉnh": location,
        "ESP_MAC": esp_id,
        "Thời tiết": f'{round(temp)}°C ; {humidity}%'
    }
