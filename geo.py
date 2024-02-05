import requests

API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def geocode(adress):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": adress,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponyms = json_response['response']['GeoObjectCollection']['featureMember']
    return toponyms[0]["GeoObject"] if toponyms else 0


def get_coordinates(address):
    toponym = geocode(address)
    toponym_coord = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coord.split()
    return float(toponym_long), float(toponym_lat)

def get_ll_span(adress):
    toponym = geocode(adress)
    if not toponym:
        return (None, None)
    toponym_coord = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coord.split()
    ll = ','.join([toponym_long, toponym_lat])
    env = toponym['boundedBy']['Envelope']
    l, b = env['lowerCorner'].split(" ")
    r, t = env['upperCorner'].split(" ")
    dx = abs(float(l) - float(r)) / 2
    dy = abs(float(t) - float(b)) / 2
    span = f'{dx},{dy}'
    return ll, span