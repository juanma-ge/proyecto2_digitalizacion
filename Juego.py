import random
import json
import os

ARCHIVO_PARTIDA = "partida_guardada.json"

def guardar_partida(datos):
    with open(ARCHIVO_PARTIDA, 'w') as archivo:
        json.dump(datos, archivo)

def cargar_partida():
    try:
        with open(ARCHIVO_PARTIDA, 'r') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def mostrar_menu():
    partida_guardada = cargar_partida()
    
    while True:
        print("\n---- MENÚ ----")
        print("1. Iniciar modo carrera")
        if partida_guardada:
            print("2. Continuar partida guardada")
            print("3. Salir")
            opciones_validas = ['1', '2', '3']
        else:
            print("2. Salir")
            opciones_validas = ['1', '2']
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            iniciar_modo_carrera()
            partida_guardada = cargar_partida()
        elif opcion == "2" and partida_guardada:
            continuar_partida(partida_guardada)
            partida_guardada = cargar_partida()
        elif opcion in opciones_validas[-1]:  # Última opción válida (Salir)
            print("Saliendo del juego...")
            break
        else:
            print("Opción no válida, por favor elige una de las opciones.")

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

def seleccionar_posicion():
    posiciones = ["Portero", "Defensa", "Mediocampista", "Delantero"]
    while True:
        print("\nSelecciona tu posición:")
        for i, posicion in enumerate(posiciones, 1):
            print(f"{i}. {posicion}")
        try:
            opcion = int(input("Elige una posición: ")) - 1
            if 0 <= opcion < len(posiciones):
                return posiciones[opcion]
            else:
                print("Opción no válida, por favor elige una posición válida.")
        except ValueError:
            print("Entrada no válida, por favor ingresa un número.")

def seleccionar_liga_y_equipo(equipos):
    while True:
        print("\nSelecciona una liga:")
        ligas = list(equipos.keys())
        for i, liga in enumerate(ligas, 1):
            print(f"{i}. {liga}")
        try:
            opcion_liga = int(input("Elige una liga: ")) - 1
            if 0 <= opcion_liga < len(ligas):
                liga_seleccionada = ligas[opcion_liga]
                break
            else:
                print("Opción no válida, por favor elige una liga válida.")
        except ValueError:
            print("Entrada no válida, por favor ingresa un número.")

    while True:
        print(f"\nSelecciona un equipo de la {liga_seleccionada}:")
        equipos_liga = equipos[liga_seleccionada]
        for i, equipo in enumerate(equipos_liga, 1):
            print(f"{i}. {equipo}")
        try:
            opcion_equipo = int(input("Elige un equipo: ")) - 1
            if 0 <= opcion_equipo < len(equipos_liga):
                equipo_seleccionado = equipos_liga[opcion_equipo]
                return liga_seleccionada, equipo_seleccionado
            else:
                print("Opción no válida, por favor elige un equipo válido.")
        except ValueError:
            print("Entrada no válida, por favor ingresa un número.")

def simular_partido(posicion, equipo_seleccionado, equipo_rival):
    print(f"\n{equipo_seleccionado} vs {equipo_rival}")
    
    if posicion == "Delantero":
        probabilidad_gol = 0.7
        probabilidad_asistencia = 0.3
    elif posicion == "Mediocampista":
        probabilidad_gol = 0.5
        probabilidad_asistencia = 0.5
    elif posicion == "Defensa":
        probabilidad_gol = 0.3
        probabilidad_asistencia = 0.7
    else:  # Esta posición es la de portero
        probabilidad_gol = 0.1
        probabilidad_asistencia = 0.1

    goles = 0
    asistencias = 0
    for _ in range(3):  # Simulamos 3 oportunidades de gol o asistencia
        if random.random() < probabilidad_gol:
            goles += 1
        if random.random() < probabilidad_asistencia:
            asistencias += 1

    print(f"Has marcado {goles} goles y hecho {asistencias} asistencias.")

    resultado = random.choice(["Ganar", "Empatar", "Perder"])
    if resultado == "Ganar":
        puntos = 3
        print(f"¡Has ganado el partido! Obtienes {puntos} puntos.")
    elif resultado == "Empatar":
        puntos = 1
        print(f"Has empatado el partido. Obtienes {puntos} punto.")
    else:
        puntos = 0
        print(f"Has perdido el partido. No obtienes puntos.")

    return puntos

def continuar_partida(partida_guardada):
    print("\n--- CONTINUANDO PARTIDA GUARDADA ---")
    print(f"Posición: {partida_guardada['posicion']}")
    print(f"Liga: {partida_guardada['liga']}")
    print(f"Equipo: {partida_guardada['equipo']}")
    print(f"Puntos acumulados: {partida_guardada['puntos_totales']}")
    print(f"Partidos jugados: {len(partida_guardada['partidos_jugados'])}/{partida_guardada['total_partidos']}")
    
    confirmacion = input("\n¿Deseas continuar esta partida? (s/n): ").lower()
    if confirmacion == 's':
        equipos = mostrar_equipos()
        equipos_rivales = equipos[partida_guardada['liga']].copy()
        equipos_rivales.remove(partida_guardada['equipo'])
        
        # Filtrar equipos contra los que ya se jugó
        equipos_restantes = [eq for eq in equipos_rivales if eq not in partida_guardada['partidos_jugados']]
        
        puntos_totales = partida_guardada['puntos_totales']
        
        for equipo_rival in equipos_restantes:
            puntos = simular_partido(partida_guardada['posicion'], 
                                   partida_guardada['equipo'], 
                                   equipo_rival)
            puntos_totales += puntos
            
            # Actualiza los partidos jugados
            partida_guardada['partidos_jugados'].append(equipo_rival)
            
            # Guarda el progreso después de cada partido
            datos_guardar = {
                'posicion': partida_guardada['posicion'],
                'liga': partida_guardada['liga'],
                'equipo': partida_guardada['equipo'],
                'puntos_totales': puntos_totales,
                'partidos_jugados': partida_guardada['partidos_jugados'],
                'total_partidos': partida_guardada['total_partidos']
            }
            guardar_partida(datos_guardar)
            
            # Verificar si se completó la temporada
            if len(partida_guardada['partidos_jugados']) >= partida_guardada['total_partidos']:
                print(f"\n¡Temporada completada! Puntos totales: {puntos_totales}")
                if os.path.exists(ARCHIVO_PARTIDA):
                    os.remove(ARCHIVO_PARTIDA)
                break
                
            input("\nPresiona Enter para continuar al siguiente partido...")
    else:
        print("Volviendo al menú principal...")

def iniciar_modo_carrera():
    # Verificar si hay partida guardada
    partida_guardada = cargar_partida()
    if partida_guardada:
        confirmacion = input("Ya tienes una partida guardada. ¿Deseas empezar una nueva? (s/n): ").lower()
        if confirmacion != 's':
            return
    
    equipos = mostrar_equipos()
    posicion = seleccionar_posicion()
    liga_seleccionada, equipo_seleccionado = seleccionar_liga_y_equipo(equipos)

    print(f"\nHas seleccionado ser un {posicion} en el equipo {equipo_seleccionado} de la {liga_seleccionada}.")

    equipos_rivales = equipos[liga_seleccionada].copy()
    equipos_rivales.remove(equipo_seleccionado)
    random.shuffle(equipos_rivales)
    
    total_partidos = len(equipos_rivales)
    puntos_totales = 0
    partidos_jugados = []
    
    # Guardar estado inicial
    datos_guardar = {
        'posicion': posicion,
        'liga': liga_seleccionada,
        'equipo': equipo_seleccionado,
        'puntos_totales': puntos_totales,
        'partidos_jugados': partidos_jugados,
        'total_partidos': total_partidos
    }
    guardar_partida(datos_guardar)
    
    for equipo_rival in equipos_rivales:
        puntos = simular_partido(posicion, equipo_seleccionado, equipo_rival)
        puntos_totales += puntos
        partidos_jugados.append(equipo_rival)
        
        # Actualiza la partida guardada
        datos_guardar['puntos_totales'] = puntos_totales
        datos_guardar['partidos_jugados'] = partidos_jugados
        guardar_partida(datos_guardar)
        
        # Verifica si se completó la temporada
        if len(partidos_jugados) >= total_partidos:
            print(f"\n¡Temporada completada! Puntos totales: {puntos_totales}")
            if os.path.exists(ARCHIVO_PARTIDA):
                os.remove(ARCHIVO_PARTIDA)
            break
            
        input("\nPresiona Enter para continuar al siguiente partido...")

def main():
    mostrar_menu()

if __name__ == "__main__":
    main()