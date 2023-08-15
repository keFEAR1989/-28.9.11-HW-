import requests
from pydantic import BaseModel

class WeatherRequest(BaseModel):
    # Имя города
    city: str
    # Ключ API OpenWeatherMap
    appid: str

class WeatherResponse(BaseModel):
    # Основная информация о погоде
    main: dict
    # Название города
    name: str

def test_request_with_all_required_fields(weather_request: WeatherRequest):
    # Отправить запрос к API OpenWeatherMap
    response = requests.get(
        url="https://api.openweathermap.org/data/2.5/weather",
        params=weather_request.dict(),
    )

    # Проверить, что запрос был успешным
    assert response.status_code == 200

    # Проверить, что тело ответа соответствует ожидаемой схеме
    response_body = response.json()
    assert isinstance(response_body, WeatherResponse)
    assert response_body.main is not None
    assert response_body.name is not None

def test_request_without_city_field(weather_request: WeatherRequest):
    # Удалить поле `city` из запроса
    weather_request.city = None

    # Отправить запрос к API OpenWeatherMap
    response = requests.get(
        url="https://api.openweathermap.org/data/2.5/weather",
        params=weather_request.dict(),
    )

    # Проверить, что запрос не был успешным
    assert response.status_code != 200

    # Проверить, что тело ответа содержит сообщение об ошибке
    error_message = response.json()["message"]
    assert error_message == "Необходимый параметр отсутствует: city"

def test_request_with_invalid_appid(weather_request: WeatherRequest):
    # Установить недействительное значение для `appid`
    weather_request.appid = "invalid"

    # Отправить запрос к API OpenWeatherMap
    response = requests.get(
        url="https://api.openweathermap.org/data/2.5/weather",
        params=weather_request.dict(),
    )

    # Проверить, что запрос не был успешным
    assert response.status_code != 200

    # Проверить, что тело ответа содержит сообщение об ошибке
    error_message = response.json()["message"]
    assert error_message == "Недействительный ключ API"


