import requests
from io import BytesIO
import requests
from PIL import Image


API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"

def get_response(toponym_to_find):


    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": API_KEY,
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        raise RuntimeError(f"Ошибка запроса: {response.url}\n"
                           f"HTTP статус: {response.status_code}({response.reason})")

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    return toponym


def get_ll(toponym):
    if not toponym:
        return None
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    return ll


def get_spn(toponym):
    if not toponym:
        return None
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx, dy = abs(float(l) - float(r)), abs(float(b) - float(t))
    spn = ",".join([str(dx), str(dy)])
    return spn


def get_object(ll, spn, map_type='map', add_params=None):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": map_type,
        "pt": f"{ll},pm2rdm"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    return response


def show_map(response):
    Image.open(BytesIO(
        response.content)).show()