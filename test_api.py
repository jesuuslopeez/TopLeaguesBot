import requests
from config import FDO_API_KEY

BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": FDO_API_KEY}

def test_goleadores():
    liga_codigo = "PL"  # Cambia a otra liga si es necesario
    url = f"{BASE_URL}/competitions/{liga_codigo}/scorers"
    response = requests.get(url, headers=HEADERS)

    print("Código de respuesta:", response.status_code)
    print("Respuesta JSON:")
    print(response.json())

test_goleadores()
