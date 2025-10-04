import requests
import json

def weather_info(place):
    places = {
    "andijon": [40.8154, 72.2834],
    "buxoro": [39.7676, 64.4239],
    "fargona": [40.3864, 71.7864],
    "jizzax": [40.1158, 67.8422],
    "namangan": [41.0000, 71.6667],
    "navoiy": [40.0844, 65.3792],
    "qashqadaryo": [38.8667, 66.0411],   # Qarshi shahri markaz sifatida
    "qoraqalpogiston": [42.4667, 59.6000],  # Nukus shahri markaz sifatida
    "samarqand": [39.6542, 66.9597],
    "sirdaryo": [40.8333, 68.6667],   # Guliston shahri markaz sifatida
    "surxondaryo": [37.2242, 67.2783],  # Termiz shahri markaz sifatida
    "toshkent shahri": [41.2995, 69.2401],  # Toshkent shahri
    "toshkent": [41.2646, 69.2163],  # viloyat markazi – Nurafshon
    "xorazm": [41.55, 60.6333]  # Urganch shahri markaz sifatida
}   
    place = place.lower()
    infos = {}
   
    if place in places:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={places[place][0]}&longitude={places[place][1]}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,rain_sum,snowfall_sum&timezone=auto&forecast_days=5"
        response = requests.get(url, timeout=10)
        jresponse = response.json()
        code = response.status_code
        infos['code'] = code
        infos['informations'] = jresponse['daily']
    elif len(place)==16 and place[:10]+place[11:]=='qoraqalpogiston':
        place = 'qoraqalpogiston'
        url = f"https://api.open-meteo.com/v1/forecast?latitude={places[place][0]}&longitude={places[place][1]}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,rain_sum,snowfall_sum&timezone=auto&forecast_days=5"
        response = requests.get(url, timeout=10)
        jresponse = response.json()
        code = response.status_code
        infos['code'] = code
        infos['informations'] = jresponse['daily']
    elif len(place)==15 and place[:9]+place[10:]=='qoraqalpoiston':
        place = 'qoraqalpogiston'
        url = f"https://api.open-meteo.com/v1/forecast?latitude={places[place][0]}&longitude={places[place][1]}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,rain_sum,snowfall_sum&timezone=auto&forecast_days=5"
        response = requests.get(url, timeout=10)
        jresponse = response.json()
        code = response.status_code
        infos['code'] = code
        infos['informations'] = jresponse['daily']
    else:
        return False
    return infos

    
        