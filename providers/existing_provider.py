# existing provider
import requests


def get_data():
    response = requests.get("https://api.provider1.com/data")
    return response.json()
