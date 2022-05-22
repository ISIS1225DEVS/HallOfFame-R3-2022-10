"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from numpy import short
import config as cf
import sys
import controller
from tabulate import tabulate
from textwrap import wrap
from typing import Any
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

PRINT_SEPARATOR = "\n" + "="*38


def printMenu():
    print(PRINT_SEPARATOR)
    print("Bienvenido")
    print("0- Crear catálogo y cargar datos")
    print("1- Reportar adquisiciones recientes de un club")
    print("2- Reportar jugadores de posición P en rangos de desempeño, potencial y salario")
    print("3- Reportar jugadores con etiqueta E dentro de un rango salarial")
    print("4- Reportar jugadores con rasgo característico nacidos en un periodo de tiempo")
    print("5- Graficar histograma de propiedad P para los jugadores FIFA")
    print("6- Encontrar posibles sustitutos para los jugadores FIFA")
    print("S- Salir")


# Opción 0 - Carga de datos
def newController()->Any:
    return controller.newController()

control = None

def loadData(control: dict)->Any:
    """
    Carga los datos en el catalogo, dentro del modelo

    Args:
        control (dict): diccionario representativo de los datos

    Returns:
        Any: TAD lista de los jugadores
    """
    return controller.loadData(control)


def printPlayers(ps: Any, hds: list, num = 5):
    """
    Imprime los primeros num y últimos num jugadores cargados

    Args:
        ps (Any): TAD lista de jugadores
        hds (list): lista de str con las llaves a mirar
        num (int): número de jugadores a mirar
    """
    to_print = []
    sz = lt.size(ps)
    print("Jugadores encontrados:", sz)

    if (sz == 0 or ps == None):
        print("No players available")
        return
    # no hay suficientes
    elif (sz < num*2):
        first_ps = lt.subList(ps, 1, sz)
        last_ps = lt.newList("ARRAY_LIST")
    else:
        first_ps = lt.subList(ps, 1, num)
        last_ps = lt.subList(ps, sz-num+1, num)

    fl_ps = lt.newList("ARRAY_LIST")
    for p in lt.iterator(first_ps):
        lt.addLast(fl_ps, p)
    for p in lt.iterator(last_ps):
        lt.addLast(fl_ps, p)

    for p in lt.iterator(fl_ps):
        printable_p = []
        mesg = None

        for k in hds:
            # convertimos el tipo que nos dan
            if (type(p[k]) == set):
                mesg = ', '.join([x for x in p[k]])
            else:
                mesg = str(p[k])

            printable_p.append('\n'.join(wrap(mesg, 15)))

        to_print.append(printable_p)

    print("Los primeros", num, "y últimos", num, "jugadores son:")
    print(tabulate(to_print, headers=hds, tablefmt="grid"))

# Opción 1
def printRecentPlayers(recent_players: Any):
    """
    Imprime los 5 jugadores más recientes del club

    Args:
        recent players (Any): RBT de jugadores ordenados por fecha de entrada
    """
    hds = ["club_joined", "age", "dob", "short_name", 
    "overall", "nationality_name", "value_eur", "wage_eur", 
    "release_clause_eur", "club_contract_valid_until", "player_positions",
    "club_position", "player_tags", "player_traits"]

    to_print = []
    elementos = om.size(recent_players)
 
    players_list = om.keySet(recent_players)
    if lt.size(players_list) > 5:
        first_5 = lt.subList(players_list, 1, 5)
    else:
        first_5 = players_list


    liga = lt.getElement(first_5, 1)['league_name']
    nivel = lt.getElement(first_5, 1)['league_level']

    for p in lt.iterator(first_5):
        printable_p = []
        mesg = None

        for k in hds:
            # convertimos el tipo que nos dan
            if (type(p[k]) == set):
                mesg = ', '.join([x for x in p[k]])
            else:
                mesg = str(p[k])

            printable_p.append('\n'.join(wrap(mesg, 15)))

        to_print.append(printable_p)
    
    print(PRINT_SEPARATOR)
    print('El número de adquisiciones asociadas al club es: {}'.format(elementos))
    print('El club juega en la liga {}, la cual es de nivel: {}'.format(liga, nivel))
    print(PRINT_SEPARATOR)

    print("Los primeros 5 jugadores son:")
    print(tabulate(to_print, headers=hds, tablefmt="grid"))


# Opción 3
def printWagesTags(lista, num_players):
    hds = ["long_name", "age", "dob", "nationality_name", "value_eur", "wage_eur", "club_name",
     "league_name", "potential", "overall", "player_positions", "player_traits", "player_tags"]

    to_print = []

    # No hay jugadores con ese rango de salarios y ese tag
    if ((lista == None) or (lt.size(lista) == 0)):
        print("No hay jugadores con ese rango de salarios y ese tag")
        return

    # se sacan tamaños y subarreglos

    if (num_players < 6):
        primeros = lt.subList(lista, 1, min(3, num_players))
        ultimos = lt.subList(lista, 4, max(0, num_players-4))
    else:
        primeros = lt.subList(lista, 1, min(3, num_players))
        ultimos = lt.subList(lista, max(1, num_players-2), 3)

    total = lt.newList(datastructure='ARRAY_LIST')

    for j in lt.iterator(primeros): lt.addLast(total, j)
    for j in lt.iterator(ultimos): lt.addLast(total, j)


    for i in range(lt.size(total)):
        printable_p = []
        mesg = None

        for k in hds:
            # convertimos el tipo que nos dan
            if (type(lt.getElement(total, lt.size(total)-i)[k]) == set):
                mesg = ', '.join([x for x in lt.getElement(total, lt.size(total)-i)[k]])
            else:
                mesg = str(lt.getElement(total, lt.size(total)-i)[k])

            printable_p.append('\n'.join(wrap(mesg, 15)))

        to_print.append(printable_p)
    
    print(PRINT_SEPARATOR)
    print('El número de jugadores que cumplen con los criterios de búsqueda: {}'.format(num_jugadores))
    print(PRINT_SEPARATOR)

    print("Los primeros 3 y últimos 3 jugadores son:")
    print(tabulate(to_print, headers=hds, tablefmt="grid"))




# Opción 4
def printHistogram(ht: Any):
    """
    Imprime el histograma del requerimiento 4

    Args:
        ht (Any): TAD lista con valores ((a,b), x)
    """
    hds = ["bin", "count", "lvl", "mark"]
    to_print = []
    tot_players = 0

    for elem in lt.iterator(ht):
        printable_bucket = [
            str("(" + str(round(elem[0], 2)) + ", " + str(round(elem[1], 2)) + "]"),
            elem[2],
            elem[3],
            "*" * elem[3]
        ]

        tot_players += elem[2]

        to_print.append(printable_bucket)

    print("Se registraron", tot_players, "jugadores.")
    print(tabulate(to_print, headers=hds, tablefmt="grid"))

# Opción 6 

def printReq6(lista, num):
    hds = ["long_name", "age", "dob", "nationality_name", "value_eur", "wage_eur", "club_name",
     "league_name", "potential", "overall", "player_positions", "VR", "player_traits", "player_tags"]
    num_players = lt.size(lista)
    to_print = []

    #

    # se sacan tamaños y subarreglos

    if (num_players < 6):
        primeros = lt.subList(lista, 1, min(3, num_players))
        ultimos = lt.subList(lista, 4, max(0, num_players-4))
    else:
        primeros = lt.subList(lista, 1, min(3, num_players))
        ultimos = lt.subList(lista, max(1, num_players-2), 3)

    total = lt.newList(datastructure='ARRAY_LIST')

    for j in lt.iterator(primeros): lt.addLast(total, j)
    for j in lt.iterator(ultimos): lt.addLast(total, j)

    for i in range(lt.size(total)):
        printable_p = []
        mesg = None

        for k in hds:
            # convertimos el tipo que nos dan
            if (type(lt.getElement(total, lt.size(total)-i)[k]) == set):
                mesg = ', '.join([x for x in lt.getElement(total, lt.size(total)-i)[k]])
            else:
                mesg = str(lt.getElement(total, lt.size(total)-i)[k])

            printable_p.append('\n'.join(wrap(mesg, 15)))

        to_print.append(printable_p)
    
    print(PRINT_SEPARATOR)
    print('El número total de jugadores que pertenecen a esa posición es: {}'.format(num))
    print('El número total de jugadores que cumplen con el criterio de búsqueda: {}'.format(num_players))
    print(PRINT_SEPARATOR)

    print("El (los) jugador(es) más similar(es) es(son):")
    print(tabulate(to_print, headers=hds, tablefmt="grid"))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar:\n')
    if inputs == "0":
        print(PRINT_SEPARATOR)
        # Nuevo controlador
        print("Creando nuevo controlador...")
        control = newController()
        
        # Carga de jugadores
        print("Cargando información de los archivos ....")
        players = loadData(control)

        print(PRINT_SEPARATOR)
        print("Jugadores cargados:", lt.size(players))
        print(PRINT_SEPARATOR)

        hds = ["sofifa_id", "long_name", "age", 
        "height_cm", "weight_kg", "nationality_name", 
        "overall", "value_eur", "wage_eur", 
        "release_clause_eur", "league_name", "club_name",
        "club_joined", "player_positions", "player_tags", 
        "player_traits", "player_url"]
        printPlayers(players, hds, num=5)

    elif inputs == "1":
        print(PRINT_SEPARATOR)
        
        club = input('Ingrese el nombre del club de fútbol: ')
        recent_players = controller.getRecentAdquisitions(control, club)
        printRecentPlayers(recent_players)

    elif inputs == "2":
        print(PRINT_SEPARATOR)

        pos = input("Ingrese la posición del jugador: ")
        low_ov = int(input("Ingrese el mínimo de desempeño (overall): "))
        up_ov = int(input("Ingrese el máximo de desempeño (overall): "))
        low_pot = int(input("Ingrese el mínimo de potencial (potential): "))
        up_pot = int(input("Ingrese el máximo de potencial (potential): "))
        low_sal = int(input("Ingrese el mínimo de salario (euros): "))
        up_sal = int(input("Ingrese el máximo de salario (euros): "))

        # se hace la query
        players = controller.getPlayersPos(control, pos, low_ov, up_ov, low_pot, up_pot, low_sal, up_sal)


        hds = ["short_name", "age", "dob", "nationality_name", "value_eur", "wage_eur", "release_clause_eur", "potential", "overall", "player_positions", "player_traits", "player_tags"]

        printPlayers(players, hds, num=3)

    elif inputs == "3":
        print(PRINT_SEPARATOR)
        tag = input('Ingrese la característica que debe identificar a los jugadores (tag): ')
        lim_inf = float(input('Ingrese el límite inferior del salario recibido por los jugadores: '))
        lim_sup = float(input('Ingrese el límite superior del salario recibido por los jugadores: '))
        print(PRINT_SEPARATOR)

        lista, num_jugadores = controller.getWages(control, lim_inf, lim_sup, tag)
        printWagesTags(lista, num_jugadores)
        
    elif inputs == "4":
        print(PRINT_SEPARATOR)

        tra = input('Ingrese el rasgo (player_traits): ')
        low_dob = input('Ingrese la fecha inicial (YY-MM-DD): ')
        up_dob = input('Ingrese la fecha final (YY-MM-DD): ')

        players = controller.getPTraitsRangeDates(control, low_dob, up_dob, tra)

        hds = ["long_name", "age", "dob", "nationality_name", "value_eur", "wage_eur", "club_name", "league_name", "potential", "overall", "player_positions", "player_traits", "player_tags"]
        printPlayers(players, hds, num=3)

    elif inputs == "5":
        print(PRINT_SEPARATOR)

        prop = input('Ingrese la propiedad: ')
        bins = int(input('Ingrese el número de bins (N): '))
        scale = int(input('Ingrese la escala (x): '))

        histogram_table = controller.getHistogram(control, prop, bins, scale)

        print(PRINT_SEPARATOR)
        printHistogram(histogram_table)

    elif inputs == "6":
        print(PRINT_SEPARATOR)
        short_name = input('Ingrese el nombre corto del jugador: ')
        position = input('Ingrese el código de la posición del jugador: ')
        print(PRINT_SEPARATOR)
        lista_sustitutos, num = controller.getSustitutions(control, short_name, position)

        printReq6(lista_sustitutos, num)
        

    elif inputs == "S":
        sys.exit(0)
    else:
        continue
