import random

def mostrar_menu():
    while True:
        print("\n---- MENÚ ----")
        print("1. Iniciar modo carrera")
        print("2. Salir")
        
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            iniciar_modo_carrera()
        elif opcion == "2":
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

def iniciar_modo_carrera():
    equipos = mostrar_equipos()
    posicion = seleccionar_posicion()
    liga_seleccionada, equipo_seleccionado = seleccionar_liga_y_equipo(equipos)

    print(f"\nHas seleccionado ser un {posicion} en el equipo {equipo_seleccionado} de la {liga_seleccionada}.")

    equipos_rivales = equipos[liga_seleccionada].copy()
    equipos_rivales.remove(equipo_seleccionado)
    random.shuffle(equipos_rivales)

    puntos_totales = 0
    for equipo_rival in equipos_rivales:
        puntos_totales += simular_partido(posicion, equipo_seleccionado, equipo_rival)
        input("\nPresiona Enter para continuar al siguiente partido...")  # Espera a que el usuario presione Enter

    print(f"\nAl final de la temporada, has obtenido {puntos_totales} puntos.")

def main():
    mostrar_menu()

if __name__ == "__main__":
    main()