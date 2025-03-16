import telebot
import pytz
import locale
from config import TOKEN
from api_requests import obtener_competiciones, obtener_partidos_hoy, obtener_partidos_jornada, obtener_clasificacion, obtener_goleadores
from datetime import datetime

# Configurar el locale para que los días se muestren en español
locale.setlocale(locale.LC_TIME, "es_ES.utf8")

# Inicializar el bot con el token
bot = telebot.TeleBot(TOKEN)

COMMANDS = [
    ("start", "Iniciar bot"),
    ("help", "Ver comandos"),
    ("competiciones", "Ver competiciones"),
    ("hoy", "Partidos de hoy"),
    ("jornada", "Jornada de una liga"),
    ("clasificacion", "Tabla de una liga"),
    ("goleadores", "Máximos goleadores")
]

def registrar_comandos():
    """ Registra los comandos en Telegram con un pequeño retardo para asegurar su procesamiento """
    comandos = [telebot.types.BotCommand(cmd, desc) for cmd, desc in COMMANDS]
    bot.set_my_commands(comandos)

# Comando de inicio (/start)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bienvenida = """
    👋 *¡Bienvenido a @TopLeaguesBot!* ⚽🏆  

    📢 *Tu bot de fútbol en Telegram está listo para la acción!*  
    Aquí podrás ver resultados, clasificaciones y estar al día con los partidos de tus ligas favoritas.  

    🏆 *¿Qué puedes hacer?*  
    📅 Ver los partidos de hoy ➜ /hoy  
    ⚽ Ver los partidos de la jornada ➜ /jornada <liga>  
    📊 Ver la clasificación ➜ /clasificacion <liga>
    🎯 Máximos goleadores ➜ /goleadores <liga>  
    
    📌 *Para más información usa* /help  
    ¡Disfruta del fútbol con @TopLeaguesBot! ⚡🔥
    """
    bot.reply_to(message, bienvenida, parse_mode="Markdown")


# Comando de ayuda (/help)
@bot.message_handler(commands=['help'])
def send_help(message):
    ayuda = """
    🤖 *Bienvenido a @TopLeaguesBot* ⚽🏆

    📌 *Lista de comandos disponibles:* 

    🔹 /start - Inicia la interacción con el bot y muestra un mensaje de bienvenida.
    🔹 /help - Muestra este listado de comandos con sus descripciones.

    📅 *Información de Partidos:*  
    ⚽  /hoy - Muestra los partidos del día con sus horarios y resultados.  
    🏆  /jornada <liga> - Muestra los partidos de la próxima jornada de la liga indicada.  

    📊 *Estadísticas:*  
    📌  /clasificacion <liga> - Muestra la tabla de posiciones de la liga indicada.  
    🎯  /goleadores <liga>  - Muestra los máximos goleadores de la liga indicada.  

    🏆 *Competiciones:*  
    🔍  /competiciones - Muestra las competiciones disponibles.  

    📢 *¡Disfruta del fútbol con @TopLeaguesBot!* ⚽🔥
    """
    bot.reply_to(message, ayuda, parse_mode="Markdown")


# Comando de competiciones (/competiciones)
@bot.message_handler(commands=['competiciones'])
def mostrar_competiciones(message):
    competiciones = obtener_competiciones()

    if not competiciones:
        bot.reply_to(message, "⚠️ No se pudo obtener la lista de competiciones.", parse_mode="Markdown")
        return

    mensaje = "🏆 *Competiciones disponibles:*\n"
    for competicion in competiciones:
        nombre = competicion.get("name", "Desconocido")
        mensaje += f"- *{nombre}*\n"

    bot.reply_to(message, mensaje, parse_mode="Markdown")


# Comando de partidos del día (/hoy y /hoy <competición>)
@bot.message_handler(commands=['hoy'])
def partidos_hoy(message):
    command = message.text.split(maxsplit=1)

    if len(command) == 1:
        liga_nombre = None  # Sin filtro, mostrar todos los partidos
    else:
        liga_nombre = command[1].strip().lower()

    partidos = obtener_partidos_hoy(liga_nombre)

    if not partidos:
        bot.reply_to(message, "❔ Parece que hoy no hay partidos de esta competición...", parse_mode="Markdown")
        return

    mensaje = "📅 *Partidos de hoy:*\n"
    spain_tz = pytz.timezone("Europe/Madrid")

    for partido in partidos:
        fecha_utc = partido.get("utcDate", "")
        fecha_dt = datetime.strptime(fecha_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc).astimezone(spain_tz)
        hora = fecha_dt.strftime("%H:%M")

        home = partido["homeTeam"].get("name", "Desconocido")
        away = partido["awayTeam"].get("name", "Desconocido")
        status = partido.get("status", "")

        if status == "IN_PLAY":
            marcador = "🔴 EN JUEGO"
        elif status == "FINISHED":
            goles_home = partido["score"]["fullTime"].get("home", "?")
            goles_away = partido["score"]["fullTime"].get("away", "?")
            marcador = f"🏆 {goles_home} - {goles_away}"
        else:
            marcador = f"🕒 {hora}"

        mensaje += f"⚽ *{home}* vs *{away}* {marcador}\n"

    bot.reply_to(message, mensaje, parse_mode="Markdown")


# Comando de partidos de la jornada (/jornada <liga>)
@bot.message_handler(commands=['jornada'])
def partidos_jornada(message):
    command = message.text.split(maxsplit=1)

    if len(command) < 2:
        bot.reply_to(message, "⚠️ Debes especificar el nombre de la competición. Ejemplo: `/jornada Premier League`",
                     parse_mode="Markdown")
        return

    liga_nombre = command[1].strip().lower()
    partidos = obtener_partidos_jornada(liga_nombre)

    if not partidos:
        bot.reply_to(message, f"⚠️ No se encontraron partidos para *{liga_nombre}*.", parse_mode="Markdown")
        return

    jornada = partidos[0].get("matchday", "Desconocida")
    mensaje = f"📅 *Jornada {jornada} en {liga_nombre.capitalize()}:*\n\n"

    partidos_por_dia = {}
    spain_tz = pytz.timezone("Europe/Madrid")

    for partido in partidos:
        fecha_utc = partido.get("utcDate", "")
        fecha_dt = datetime.strptime(fecha_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc).astimezone(spain_tz)
        dia = fecha_dt.strftime("%A %d/%m").capitalize()
        hora = fecha_dt.strftime("%H:%M")

        home = partido["homeTeam"].get("name", "Desconocido")
        away = partido["awayTeam"].get("name", "Desconocido")
        status = partido.get("status", "")

        if status == "IN_PLAY":
            marcador = "🔴 EN JUEGO"
        elif status == "FINISHED":
            goles_home = partido["score"]["fullTime"].get("home", "?")
            goles_away = partido["score"]["fullTime"].get("away", "?")
            marcador = f"🏆 {goles_home} - {goles_away}"
        else:
            marcador = f"🕒 {hora}"

        partido_info = f"⚽ *{home}* vs *{away}* {marcador}"

        if dia not in partidos_por_dia:
            partidos_por_dia[dia] = []
        partidos_por_dia[dia].append(partido_info)

    for dia, lista_partidos in partidos_por_dia.items():
        mensaje += f"📅 *{dia}:*\n"
        mensaje += "\n".join(lista_partidos) + "\n\n"

    bot.reply_to(message, mensaje, parse_mode="Markdown")


# Comando de clasificación de la liga (/clasificacion <liga>)
@bot.message_handler(commands=['clasificacion'])
def clasificacion_liga(message):
    command = message.text.split(maxsplit=1)

    if len(command) < 2:
        bot.reply_to(message,
                     "⚠️ Debes especificar el nombre de la competición. Ejemplo: `/clasificacion Premier League`",
                     parse_mode="Markdown")
        return

    liga_nombre = command[1].strip().lower()
    clasificacion = obtener_clasificacion(liga_nombre)

    if not clasificacion:
        bot.reply_to(message, f"⚠️ No se pudo obtener la clasificación para *{liga_nombre}*.", parse_mode="Markdown")
        return

    mensaje = f"📊 *Clasificación de {liga_nombre.capitalize()}:*\n\n"
    for equipo in clasificacion:
        posicion = equipo.get("position", "?")
        nombre = equipo.get("team", {}).get("name", "Desconocido")
        puntos = equipo.get("points", "?")

        mensaje += f"{posicion}. *{nombre}* - {puntos} pts\n"

    bot.reply_to(message, mensaje, parse_mode="Markdown")


# Comando de goleadores de la liga (/goleadores <liga>)
@bot.message_handler(commands=['goleadores'])
def goleadores_liga(message):
    command = message.text.split(maxsplit=1)

    if len(command) < 2:
        bot.reply_to(message, "⚠️ Debes especificar el nombre de la competición. Ejemplo: `/goleadores Premier League`",
                     parse_mode="Markdown")
        return

    liga_nombre = command[1].strip().lower()
    goleadores = obtener_goleadores(liga_nombre)

    if not goleadores:
        bot.reply_to(message, f"⚠️ No se pudo obtener la lista de goleadores para *{liga_nombre}*.",
                     parse_mode="Markdown")
        return

    emojis = ["🥇", "🥈", "🥉"] + [f"{i + 1}️⃣" for i in range(3, 9)] + ["1️⃣0️⃣"]

    mensaje = f"⚽ *Máximos goleadores de {liga_nombre.capitalize()}:*\n\n"
    for idx, goleador in enumerate(goleadores[:10]):  # Limitar a los 10 primeros
        posicion = emojis[idx]  # Medallas para los 3 primeros, números para el resto
        nombre = goleador["player"]
        equipo = goleador["team"]
        goles = goleador["goals"]

        mensaje += f"{posicion} *{nombre}* ({equipo}) - {goles} goles\n"

    bot.reply_to(message, mensaje, parse_mode="Markdown")

# Manejar comandos inexistentes
@bot.message_handler(func=lambda message: message.text.startswith("/"))
def comando_no_encontrado(message):
    bot.reply_to(message, "❌ Comando no reconocido. Escribe /help para ver la lista de comandos disponibles.", parse_mode="Markdown")


if __name__ == '__main__':
    print("Bot iniciado...")
    bot.polling(none_stop=True)
