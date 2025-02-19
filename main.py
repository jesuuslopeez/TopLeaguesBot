import telebot
import requests
import pytz
import time
import threading
from datetime import datetime

# Conexión con el bot
TOKEN = '8115206546:AAEoT-OTtoYm1ixXKb7vRbDFv1VFucBIoSM'
FDO_API_KEY = 'bf887f129b1f42e79e8da3ec889b12b9'
bot = telebot.TeleBot(TOKEN)

# Formato hora España/Madrid
spain_tz = pytz.timezone('Europe/Madrid')

def obtener_partidos_hoy():
    hoy = datetime.now().strftime('%Y-%m-%d')
    url = "https://api.football-data.org/v4/matches"
    headers = {"X-Auth-Token": FDO_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "⚠️ No se pudo obtener información sobre los partidos de hoy."

    data = response.json()
    partidos = data.get("matches", [])

    partidos_hoy = [partido for partido in partidos if partido['utcDate'][:10] == hoy]

    if not partidos_hoy:
        return "📭 No hay partidos programados para hoy."

    mensaje = "📅 *Partidos de hoy:*\n"
    for partido in partidos_hoy:
        home = partido["homeTeam"]["name"]
        away = partido["awayTeam"]["name"]
        utc_time = partido["utcDate"]

        utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = pytz.utc.localize(utc_time)
        local_time = utc_time.astimezone(spain_tz)
        hora_local = local_time.strftime('%H:%M')

        mensaje += f"⚽ {home} vs {away} 🕒 {hora_local}\n"

    return mensaje

def obtener_competiciones():
    url = "https://api.football-data.org/v4/competitions"
    headers = {"X-Auth-Token": FDO_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "⚠️ No se pudo obtener la lista de competiciones."

    data = response.json()

    # Imprimimos el JSON completo para ver qué estamos recibiendo
    print("JSON recibido:", data)

    competiciones = data.get("competitions", [])

    # Lista de competiciones con las nuevas IDs
    competiciones_permitidas = {
        "PL",  # Premier League
        "SA",  # Serie A
        "BL1",  # Bundesliga
        "FL1",  # Ligue 1
        "PD",  # La Liga
        "DED",  # Eredivisie
        "ELC"  # Championship
    }

    mensaje = "🏆 Competiciones disponibles:\n"
    for competicion in competiciones:
        codigo = competicion["code"]

        # Comprobar si el código de la competencia está en la lista de permitidas
        if codigo in competiciones_permitidas:
            nombre = competicion["name"]
            mensaje += f"- {nombre} (Código: {codigo})\n"

    if mensaje == "🏆 Competiciones disponibles:\n":
        return "⚠️ No se encontraron competiciones disponibles."

    return mensaje

def obtener_partidos_jornada(liga):
    url = f"https://api.football-data.org/v4/competitions/{liga}/matches"
    headers = {"X-Auth-Token": FDO_API_KEY}

    response = requests.get(url, headers=headers)

    print(f"URL solicitada: {url}")
    print(f"Respuesta status code: {response.status_code}")

    try:
        data = response.json()
        print(f"JSON recibido: {data}")
    except Exception as e:
        print(f"Error al procesar el JSON: {e}")
        return "⚠️ Error al procesar los datos."

    if response.status_code != 200 or "matches" not in data:
        return "⚠️ No se pudo obtener información sobre los partidos de la jornada."

    partidos = data["matches"]

    if not partidos:
        return "📭 No hay partidos programados."

    # Obtener la fecha actual en formato UTC
    ahora = datetime.utcnow().strftime('%Y-%m-%d')

    # Encontrar la jornada más reciente basada en la fecha actual
    jornadas = {}
    for partido in partidos:
        matchday = partido.get("matchday")
        fecha_partido = partido["utcDate"][:10]  # Solo la fecha sin hora
        if matchday not in jornadas:
            jornadas[matchday] = fecha_partido

    # Buscar la jornada más reciente a la fecha actual
    jornada_actual = None
    for j, fecha in sorted(jornadas.items()):
        if fecha >= ahora:
            jornada_actual = j
            break

    if jornada_actual is None:
        return "⚠️ No se pudo determinar la jornada actual."

    # Filtrar solo los partidos de esa jornada
    partidos_jornada = [p for p in partidos if p.get("matchday") == jornada_actual]

    # Limitar a máximo 10 partidos
    partidos_jornada = partidos_jornada[:10]

    mensaje = f"📅 *Partidos de la jornada {jornada_actual} ({liga})* 📅\n\n"
    for partido in partidos_jornada:
        home = partido["homeTeam"].get("name", "Desconocido")
        away = partido["awayTeam"].get("name", "Desconocido")
        utc_time = partido.get("utcDate")

        if not home or not away or not utc_time:
            continue  # Evita partidos con datos incompletos

        # ⚠️ Conversión de Hora UTC a España 📌
        try:
            utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")  # Parseamos la fecha
            utc_time = pytz.utc.localize(utc_time)  # Aseguramos que es UTC
            local_time = utc_time.astimezone(spain_tz)  # Convertimos a España
            hora_local = local_time.strftime('%H:%M')
        except Exception as e:
            print(f"Error al convertir la hora: {e}")
            hora_local = "Hora desconocida"

        mensaje += f"⚽ {home} vs {away} 🕒 {hora_local}\n"

    return mensaje

# Comando de inicio (/start)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bienvenido a @TopLeaguesBot!\nEscribe /help para descubrir que puedes hacer.\n⚽🏆")

# Comando de ayuda (/help)
@bot.message_handler(commands=['help'])
def send_help(message):
    ayuda = """
    Comandos disponibles:
    /start - Inicia la interacción con @TopLeaguesBot
    /help - Muestra el listados de comandos
    /hoy - Muestra los partidos de hoy
    /competiciones - Muestra los códigos de las competiciones
    /jornada <codigo> - Muestra los partidos de la próxima jornada
    """
    bot.reply_to(message, ayuda)

# Comando de partidos del día (/hoy)
@bot.message_handler(commands=['hoy'])
def partidos_hoy(message):
    mensaje = obtener_partidos_hoy()
    bot.reply_to(message, mensaje)

# Comando de competiciones (/competiciones)
@bot.message_handler(commands=['competiciones'])
def mostrar_competiciones(message):
    mensaje = obtener_competiciones()
    bot.reply_to(message, mensaje)


# Comando de partidos de la jornada (/jornada <codigo>)
@bot.message_handler(commands=['jornada'])
def partidos_jornada(message):
    command = message.text.split(maxsplit=1)

    if len(command) < 2:
        bot.reply_to(message, "⚠️ Debes especificar el ID de la liga. Ejemplo: /jornada PD")
        return

    liga_codigo = command[1].upper()

    mensaje = obtener_partidos_jornada(liga_codigo)

    bot.reply_to(message, mensaje)


def keep_alive():
    while True:
        try:
            requests.get("https://topleaguesbot.onrender.com")
            print("Keep-Alive enviado.")
        except Exception as e:
            print(f"Error en Keep-Alive: {e}")
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == '__main__':
    bot.polling(none_stop=True)