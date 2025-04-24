import random
import discord
from discord.ext import commands
import dotenv

# Configura el bot para que comience con !
bot = commands.Bot(command_prefix="!")

# Necesario para que el bot funcione
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

# Listado de equipos.
def mostrar_equipos():
    equipos = {
        "Premier League": ["Manchester United", "Manchester City", "Arsenal", "Chelsea", "Tottenham", "Leicester City", "Brentford", "Nottingham Forest", "Newcastle",
         "Bournemouth", "Aston Villa", "Fulham", "Brighton", "Crystal Palace", "West Ham", "Wolves", "Ipswich Town", "Southampton"],

        "La Liga": ["Real Madrid", "Barcelona", "Atletico de Madrid", "Athletic Club", "Real Sociedad", "Betis", "Sevilla", "Villarreal", "Espanyol", "Rayo Vallecano", "Girona", "Osasuna", "Mallorca",
        "Las Palmas", "Getafe", "Celta", "Leganés", "Valencia", "Valladolid", "Alavés"],

        "Liga Hypermotion": ["Cádiz", "Cartagena", "Granada", "Almeria", "Burgos", "Racing de Santander", "Huesca", "Elche", "Mirandés", "Real Oviedo", "Real Sporting", "Levante", "Real Zaragoza", "RC Deportivo",
         "Albacete", "Eibar", "Cordoba", "Malaga", "Castellon", "Eldense", "Racing Ferrol", "Tenerife"],

        "Bundesliga": ["RB Leipzig", "Bayer Leverkusen", "FC Bayern Munchen", "Eintracht Frankfurt", "SC Freiburg", "Mainz 05", "Stuttgart", "Wolfsburg", "Borussia Monchegladbach",
          "Borussia Dortmund", "FC Augsburg", "Werder Bremen", "Union Berlin", "Hoffenheim", "FC ST Pauli", "Heidenheim", "VfL Bochum", "Holstein Kiel"],

        "Ligue One": ["Paris Saint Germain", "Olympique Marseille", "Nice", "Lille", "Monaco", "Olympique Lyon", "Strasbourg", "Lens", "Stade Brestois", "Toulouse", "Auxerre", "Angers SCO", "Stade Rennais", "Nantes", "Stade de Reims",
         "Saint-Étienne", "Montpellier", "Le Havre"],
         
        "Serie A": ["Inter Milan", "AC Milan", "Napoli", "Atalanta", "Juventus", "Lazio", "Fiorentina", "Bologna", "Roma", "Udinese", "Torino", "Genoa", "Como", "Hellas Verona", "Cagliari", "Lecce", "Parma",
         "Empoli", "Venezia", "AC Monza"]
    }
    return equipos

# Simulación del partido.
def simular_partido(posicion, equipo_seleccionado, equipo_rival):
    print(f"\n{equipo_seleccionado} vs {equipo_rival}")
    
    if posicion == "Delantero":
        probabilidad_gol = 0.5
        probabilidad_asistencia = 0.2
    elif posicion == "Mediocampista":
        probabilidad_gol = 0.3
        probabilidad_asistencia = 0.4
    elif posicion == "Defensa":
        probabilidad_gol = 0.2
        probabilidad_asistencia = 0.15
    else:  
        probabilidad_gol = 0.05
        probabilidad_asistencia = 0.1

    goles = 0
    asistencias = 0
    for _ in range(3):  # Simulamos 3 oportunidades de gol o asistencia.
        if random.random() < probabilidad_gol:
            goles += 1
        if random.random() < probabilidad_asistencia:
            asistencias += 1

    resultado = random.choice(["Ganar", "Empatar", "Perder"])
    if resultado == "Ganar":
        puntos = 3
    elif resultado == "Empatar":
        puntos = 1
    else:
        puntos = 0

    return puntos, goles, asistencias, resultado

# Comando para iniciar el modo carrera.
@bot.command(name="iniciar_carrera")
async def iniciar_carrera(ctx):
    equipos = mostrar_equipos()
    
    # Seleccionar posición
    posiciones = ["Portero", "Defensa", "Mediocampista", "Delantero"]
    posicion_msg = "Selecciona tu posición:\n"
    for i, posicion in enumerate(posiciones, 1):
        posicion_msg += f"{i}. {posicion}\n"
    await ctx.send(posicion_msg)

    def check(m):
        return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(posiciones)

    posicion_msg = await bot.wait_for("message", check=check)
    posicion = posiciones[int(posicion_msg.content) - 1]

    # Selecciona la liga de donde escogerás a tu equipo.
    ligas = list(equipos.keys())
    liga_msg = "Selecciona una liga:\n"
    for i, liga in enumerate(ligas, 1):
        liga_msg += f"{i}. {liga}\n"
    await ctx.send(liga_msg)

    liga_msg = await bot.wait_for("message", check=check)
    liga_seleccionada = ligas[int(liga_msg.content) - 1]

    # Selecciona tu equipo.
    equipos_liga = equipos[liga_seleccionada]
    equipo_msg = f"Selecciona un equipo de la {liga_seleccionada}:\n"
    for i, equipo in enumerate(equipos_liga, 1):
        equipo_msg += f"{i}. {equipo}\n"
    await ctx.send(equipo_msg)

    equipo_msg = await bot.wait_for("message", check=check)
    equipo_seleccionado = equipos_liga[int(equipo_msg.content) - 1]

    await ctx.send(f"Has seleccionado ser un {posicion} en el equipo {equipo_seleccionado} de la {liga_seleccionada}.")

    # Simula los partidos.
    equipos_rivales = equipos[liga_seleccionada].copy()
    equipos_rivales.remove(equipo_seleccionado)
    random.shuffle(equipos_rivales)

    puntos_totales = 0
    for equipo_rival in equipos_rivales:
        puntos, goles, asistencias, resultado = simular_partido(posicion, equipo_seleccionado, equipo_rival)
        puntos_totales += puntos
        await ctx.send(f"**{equipo_seleccionado} vs {equipo_rival}**\n"
                       f"Has marcado {goles} goles y hecho {asistencias} asistencias.\n"
                       f"Resultado: {resultado}\n"
                       f"Puntos obtenidos: {puntos}\n"
                       f"Puntos totales: {puntos_totales}\n"
                       f"Presiona Enter para continuar al siguiente partido...")

    await ctx.send(f"Al final de la temporada, has obtenido {puntos_totales} puntos.")

bot.run(dotenv.get_key("project.env", "BOTTOKEN"))