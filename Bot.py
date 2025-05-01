import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configura el bot
intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer mensajes
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# Listado de equipos (igual que antes)
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

# Simulación del partido (igual que antes)
def simular_partido(posicion, equipo_seleccionado, equipo_rival):
    if posicion == "Delantero":
        probabilidad_gol = 0.5
        probabilidad_asistencia = 0.2
    elif posicion == "Mediocampista":
        probabilidad_gol = 0.3
        probabilidad_asistencia = 0.4
    elif posicion == "Defensa":
        probabilidad_gol = 0.2
        probabilidad_asistencia = 0.15
    else:  # Portero
        probabilidad_gol = 0.05
        probabilidad_asistencia = 0.1

    goles = 0
    asistencias = 0
    for _ in range(3):
        if random.random() < probabilidad_gol:
            goles += 1
        if random.random() < probabilidad_asistencia:
            asistencias += 1

    resultado = random.choice(["Ganar", "Empatar", "Perder"])
    puntos = 3 if resultado == "Ganar" else 1 if resultado == "Empatar" else 0

    return puntos, goles, asistencias, resultado

@bot.command(name="iniciar_carrera")
async def iniciar_carrera(ctx):
    try:
        equipos = mostrar_equipos()
        
        # Seleccionar posición
        posiciones = ["Portero", "Defensa", "Mediocampista", "Delantero"]
        posicion_msg = await ctx.send("Selecciona tu posición:\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(posiciones, 1)))

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and 1 <= int(m.content) <= len(posiciones)

        posicion_msg = await bot.wait_for("message", check=check)
        posicion = posiciones[int(posicion_msg.content) - 1]

        # Seleccionar liga
        ligas = list(equipos.keys())
        await ctx.send("Selecciona una liga:\n" + "\n".join(f"{i}. {l}" for i, l in enumerate(ligas, 1)))

        liga_msg = await bot.wait_for("message", check=check)
        liga_seleccionada = ligas[int(liga_msg.content) - 1]

        # Seleccionar equipo
        equipos_liga = equipos[liga_seleccionada]
        await ctx.send(f"Selecciona un equipo de la {liga_seleccionada}:\n" + "\n".join(f"{i}. {e}" for i, e in enumerate(equipos_liga, 1)))

        equipo_msg = await bot.wait_for("message", check=check)
        equipo_seleccionado = equipos_liga[int(equipo_msg.content) - 1]

        await ctx.send(f"Has seleccionado ser un {posicion} en el equipo {equipo_seleccionado} de la {liga_seleccionada}.")

        # Simular partidos
        equipos_rivales = equipos[liga_seleccionada].copy()
        equipos_rivales.remove(equipo_seleccionado)
        random.shuffle(equipos_rivales)

        puntos_totales = 0
        for equipo_rival in equipos_rivales:
            puntos, goles, asistencias, resultado = simular_partido(posicion, equipo_seleccionado, equipo_rival)
            puntos_totales += puntos
            
            msg = await ctx.send(
                f"**{equipo_seleccionado} vs {equipo_rival}**\n"
                f"Has marcado {goles} goles y hecho {asistencias} asistencias.\n"
                f"Resultado: {resultado}\n"
                f"Puntos obtenidos: {puntos}\n"
                f"Puntos totales: {puntos_totales}\n"
                "Presiona Enter para continuar..."
            )
            
            # Esperar a que el usuario presione Enter
            def enter_check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content == ""
            
            await bot.wait_for("message", check=enter_check)

        await ctx.send(f"¡Temporada terminada! Puntos totales: {puntos_totales}")

    except Exception as e:
        await ctx.send(f"Ocurrió un error: {e}")
        print(f"Error: {e}")

# Ejecutar el bot
bot.run(os.getenv("BOTTOKEN"))