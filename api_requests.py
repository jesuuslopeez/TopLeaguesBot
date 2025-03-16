import requests
from config import FDO_API_KEY
from datetime import datetime
import pytz

BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": FDO_API_KEY}

# Mapeo de nombres de ligas a códigos de la API
LIGAS_MAP = {
    "premier league": "PL",
    "la liga": "PD",
    "bundesliga": "BL1",
    "ligue 1": "FL1",
    "serie a": "SA",
    "eredivisie": "DED",
    "primeira liga": "PPL",
    "championship": "ELC"
}

# Mapeo de nombres correctos para mostrar en los mensajes
NOMBRES_CORRECTOS = {
    "Primera Division": "La Liga"
}


def obtener_competiciones():
    """ Obtiene la lista de competiciones disponibles en la API y filtra solo las permitidas """
    url = f"{BASE_URL}/competitions"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None  # Error al obtener las competiciones

    competiciones = response.json().get("competitions", [])

    # Filtrar solo las competiciones que están en LIGAS_MAP
    competiciones_filtradas = [c for c in competiciones if c.get("code") in LIGAS_MAP.values()]

    # Reemplazar nombres si están en el mapeo
    for competicion in competiciones_filtradas:
        nombre = competicion.get("name", "")
        if nombre in NOMBRES_CORRECTOS:
            competicion["name"] = NOMBRES_CORRECTOS[nombre]

    return competiciones_filtradas


def obtener_partidos_hoy(liga=None):
    """ Obtiene los partidos programados para hoy, con opción de filtrar por liga """
    url = f"{BASE_URL}/matches"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None  # Error al obtener los partidos

    data = response.json()
    partidos = data.get("matches", [])

    hoy = datetime.utcnow().strftime('%Y-%m-%d')

    if liga:
        liga_codigo = LIGAS_MAP.get(liga.lower())
        if not liga_codigo:
            return []  # Liga no encontrada
        partidos_filtrados = [p for p in partidos if
                              p.get("utcDate", "").startswith(hoy) and p.get("competition", {}).get(
                                  "code") == liga_codigo]
    else:
        partidos_filtrados = [p for p in partidos if p.get("utcDate", "").startswith(hoy)]

    return partidos_filtrados

def obtener_partidos_jornada(liga):
    """ Obtiene los partidos de la jornada más próxima a la fecha actual en una liga específica """
    liga_codigo = LIGAS_MAP.get(liga.lower())

    if not liga_codigo:
        return None  # Liga no encontrada

    url = f"{BASE_URL}/competitions/{liga_codigo}/matches"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None  # Error al obtener los partidos de la jornada

    data = response.json()
    partidos = data.get("matches", [])

    # Si no hay partidos, retornamos vacío
    if not partidos:
        return []

    # Obtener la fecha actual en UTC
    ahora = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Encontrar la jornada más próxima a la fecha actual
    jornadas = {}
    for partido in partidos:
        matchday = partido.get("matchday")
        fecha_partido = partido.get("utcDate")

        if matchday and fecha_partido:
            fecha_partido_dt = datetime.strptime(fecha_partido, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
            if fecha_partido_dt >= ahora:
                if matchday not in jornadas or fecha_partido_dt < jornadas[matchday]:
                    jornadas[matchday] = fecha_partido_dt

    # Buscar la jornada más cercana
    jornada_actual = min(jornadas, key=jornadas.get, default=None)

    if jornada_actual is None:
        return []

    return [p for p in partidos if p.get("matchday") == jornada_actual]


def obtener_clasificacion(liga):
    """ Obtiene la clasificación de la liga especificada """
    liga_codigo = LIGAS_MAP.get(liga.lower())

    if not liga_codigo:
        return None  # Liga no encontrada

    url = f"{BASE_URL}/competitions/{liga_codigo}/standings"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None  # Error al obtener la clasificación

    data = response.json()
    standings = data.get("standings", [])

    if not standings:
        return []

    return standings[0].get("table", [])


def obtener_goleadores(liga):
    """ Obtiene la lista de máximos goleadores de la liga especificada """
    liga_codigo = LIGAS_MAP.get(liga.lower())

    if not liga_codigo:
        return None  # Liga no encontrada

    url = f"{BASE_URL}/competitions/{liga_codigo}/scorers"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print("Error al obtener los goleadores:", response.status_code, response.text)
        return None  # Error al obtener los goleadores

    data = response.json()
    goleadores = data.get("scorers", [])

    lista_goleadores = []
    emojis = ["🥇", "🥈", "🥉"] + [f"{i+1}️⃣" for i in range(3, 9)] + ["1️⃣0️⃣"]

    for idx, goleador in enumerate(goleadores[:10]):
        jugador = goleador.get("player", {}).get("name", "Desconocido")
        equipo = goleador.get("team", {}).get("name", "Desconocido")
        goles = goleador.get("goals") if goleador.get("goals") is not None else "?"

        lista_goleadores.append({
            "position": emojis[idx],
            "player": jugador,
            "team": equipo,
            "goals": goles
        })

    return lista_goleadores

