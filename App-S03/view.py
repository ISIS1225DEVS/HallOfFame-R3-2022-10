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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from prettytable import PrettyTable
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

carga = "large"
playerfile = f'fifa-players-2022-utf8-{carga}.csv'
control = None
control = controller.init()


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Ultimas adquisiciones de un club")
    print("3- Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario.")
    print("4- Tags y salarios")
    print("5- Reportar los jugadores con cierto rasgo característico y nacidos en un periodo de tiempo.")
    print("6- Histograma de propiedad")
    print("7 BONO:- Encontrar posibles sustituciones para los jugadores FIFA.")

def printInicio(control):
    x = PrettyTable()
    x.field_names = ["sofifa_id", "long_name", "age", "height_cm", "weight_kg", "nationality_name",
                     "overall", "value_eur", "wage_eur", "release_clause_eur", "league_name",
                     "club_name", "club_joined", "player_positions", "player_tags",
                     "player_traits"]
    lista = control["players"]
    controller.sortplayers(lista)
    for i in range(1, 6):
        pl = lt.getElement(lista, i)
        x.add_row([pl["sofifa_id"], pl["long_name"], pl["age"], pl["height_cm"], pl["weight_kg"], pl["nationality_name"],
                   pl["overall"], pl["value_eur"], pl["wage_eur"], pl["release_clause_eur"], pl["league_name"],
                   pl["club_name"], pl["club_joined"], pl["player_positions"], pl["player_tags"],
                   pl["player_traits"]])

    for i in range(-5, 0):
        pl = lt.getElement(lista, i)
        x.add_row([pl["sofifa_id"], pl["long_name"], pl["age"], pl["height_cm"], pl["weight_kg"], pl["nationality_name"],
                   pl["overall"], pl["value_eur"], pl["wage_eur"], pl["release_clause_eur"], pl["league_name"],
                   pl["club_name"], pl["club_joined"], pl["player_positions"], pl["player_tags"],
                   pl["player_traits"]])
    print(x)

def printLastPlayers(club, jugadores, total):

    if jugadores is None:
        print("No existe ese club, o intente digitarlo de nuevo")

    else:
        ll = None
        ln = None
        x = PrettyTable()
        x.field_names = ['joined', 'age', 'dob', 'short_name', 'overall',
                         'nationality',
                         'value_eur', 'wage_eur', 'release_clause_eur',
                         'contract_valid', 'pos', 'club_pos', 'tags', 'traits']

        for pl in lt.iterator(jugadores):
            ll = pl['league_level']
            ln = pl['league_name']
            x.add_row([pl['club_joined'], pl['age'], pl['dob'],
                       pl['short_name'], pl['overall'],
                       pl['nationality_name'], pl['value_eur'],
                       pl['wage_eur'], pl['release_clause_eur'],
                       pl['club_contract_valid_until'], pl['player_positions'],
                       pl['club_position'], pl['player_tags'],
                       pl['player_traits']])

        print("====================REQ NO 1. INPUTS====================")
        print(f"ultimas adquisiciones para: {club}")
        print(f"Total adquisiciones: {total}")
        print("====================REQ NO 1 ANSWERS====================")
        print(f"nombre: {ln}")
        print(f"Categoria: {ll}")
        print(x)


def printPlayersbyPos(info, jugadores):

    x = PrettyTable()
    x.field_names = ['Nombre', 'Edad', 'Fecha',
                     'Nacionalidad', 'Valor Contrato', 'Valor Salario',
                     'Valor Cláusula', 'Potencial', 'Overall',
                     'Posiciones', 'Comentarios', 'Etiquetas']

    if lt.size(jugadores) == 0:
        print("No existen valores con estos parametros, intente digitarlos de nuevo")

    elif lt.size(jugadores) <= 6:
        for j in lt.iterator(jugadores):
            x.add_row([j['short_name'], j['age '], j['dob'],
                       j['nationality_name'], j['value_eur'], j['wage_eur'], j['release_clause_eur'],
                       j['potential'], j['overall'],
                       j['player_positions'], j['player_traits'],
                       j['player_tags']])
    else:
        for i in range(1, 4):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['short_name'], ji['age'], ji['dob'],
                       ji['nationality_name'], ji['value_eur'], ji['wage_eur'], ji['release_clause_eur'],
                       ji['potential'], ji['overall'],
                       ji['player_positions'], ji['player_traits'],
                       ji['player_tags']])

        for i in range(-2, 1):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['short_name'], ji['age'], ji['dob'],
                       ji['nationality_name'], ji['value_eur'], ji['wage_eur'], ji['release_clause_eur'],
                       ji['potential'], ji['overall'],
                       ji['player_positions'], ji['player_traits'],
                       ji['player_tags']])
    print("====================REQ NO 2. INPUTS====================")
    print(f"Para el limite inferior para de desempeño: #{info[1]}")
    print(f"Para el limite superior para de desempeño: #{info[2]}")
    print(f"Para el limite inferior para de potencial: #{info[3]}")
    print(f"Para el limite superior para de potencial: #{info[4]}")
    print(f"Para el limite inferior para de salario: #{info[5]}")
    print(f"Para el limite superior para de salario: #{info[6]}")
    print(f"Para posición: {info[0]}")
    print("====================REQ NO 2. ANSWERS====================")
    print(f"Jugadores validos: {lt.size(jugadores)}")
    print(x)


def printTagsAndWage(inferior, superior, tag, jugadores, disponibles):

    x = PrettyTable()
    x.field_names = ['wage_eur', 'overall', 'potential',
                     'long_name', 'dob', 'age', 'league_name',
                     'club_name', 'player_positions', 'nationality_name',
                     'value_eur', 'reselase_clause_eur', 'club_position',
                     'player_tags', 'player_traits']

    if lt.size(jugadores) == 0:
        print("No se econtraron valores")

    elif lt.size(jugadores) <= 6:
        for j in lt.iterator(jugadores):
            x.add_row([j['wage_eur'], j['overall'], j['potential'],
                       j['long_name'], j['dob'], j['age'], j['league_name'],
                       j['club_name'], j['player_positions'],
                       j['nationality_name'], j['value_eur'],
                       j['release_clause_eur'], j['club_position'],
                       j['player_tags'], j['player_traits']])
    else:
        for i in range(1, 4):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['wage_eur'], ji['overall'], ji['potential'],
                       ji['long_name'], ji['dob'], ji['age'], ji['league_name'],
                       ji['club_name'], ji['player_positions'],
                       ji['nationality_name'], ji['value_eur'],
                       ji['release_clause_eur'], ji['club_position'],
                       ji['player_tags'], ji['player_traits']])

        for i in range(-2, 1):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['wage_eur'], ji['overall'], ji['potential'],
                       ji['long_name'], ji['dob'], ji['age'], ji['league_name'],
                       ji['club_name'], ji['player_positions'],
                       ji['nationality_name'], ji['value_eur'],
                       ji['release_clause_eur'], ji['club_position'],
                       ji['player_tags'], ji['player_traits']])
    print("====================REQ NO 3. INPUTS====================")
    print(f"Para el tag: #{tag}")
    print(f"Limite superior: {superior}")
    print(f"Limite inferior: {inferior}")
    print("====================REQ NO 3 ANSWERS====================")
    print(f"Jugadores FIFA disponibles: {disponibles}")
    print(f"Jugadores en el rango: {lt.size(jugadores)}")
    print(x)


def printHistograma(bins, count, lvl, mark, mayor, menor, segmentos, niveles, propiedad):
    x = PrettyTable()
    x.field_names = ["Bin", "count", "lvl", "mark"]
    for i in range(1, lt.size(bins) + 1):
        bin = lt.getElement(bins, i)
        counts = lt.getElement(count, i)
        level = lt.getElement(lvl, i)
        marca = lt.getElement(mark, i)
        x.add_row([bin, counts, level, marca])
    contador = 0
    for i in lt.iterator(count):
        contador += i
    print("====================REQ NO 5. INPUTS====================")
    print(f"Para la propiedad: {propiedad}")
    print(f"con {segmentos} segmentos")
    print(f"Con escala de jugadores de {niveles}")
    print("====================REQ NO 5. ANSWERS====================")
    print(f"valores entre {menor} y {mayor}")
    print(f"Jugadores analizados: {contador}")
    print(f"Jugadores representados en el histograma: {contador}")
    print(x)


def printPlayersbyTrait(inferior, superior, trait, jugadores):

    x = PrettyTable()
    x.field_names = ['Nombre', 'Edad', 'Fefcha',
                     'Nationalidad', 'Valor contrato', 'Valor Salario', 'Club',
                     'Liga', 'Potencial', 'Overall',
                     'Posiciones', 'Comentarios', 'Tags']

    if lt.size(jugadores) == 0:
        print("No se econtraron valores")

    elif lt.size(jugadores) <= 6:
        for j in lt.iterator(jugadores):
            x.add_row([j['long_name'], j['age'], j['dob'],
                       j['nationality_name'], j['value_eur'], j['wage_eur'], j['club_name'],
                       j['league_name'], j['potential'],
                       j['overall'], j['player_positions'],
                       j['player_traits'], j['player_tags']])
    else:
        for i in range(1, 4):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['long_name'], ji['age'], ji['dob'],
                       ji['nationality_name'], ji['value_eur'], ji['wage_eur'], ji['club_name'],
                       ji['league_name'], ji['potential'],
                       ji['overall'], ji['player_positions'],
                       ji['player_traits'], ji['player_tags']])

        for i in range(-2, 1):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['long_name'], ji['age'], ji['dob'],
                       ji['nationality_name'], ji['value_eur'], ji['wage_eur'], ji['club_name'],
                       ji['league_name'], ji['potential'],
                       ji['overall'], ji['player_positions'],
                       ji['player_traits'], ji['player_tags']])
    print("====================REQ NO 4. INPUTS====================")
    print(f"Para el trait: #{trait}")
    print(f"Limite superior: {superior}")
    print(f"Limite inferior: {inferior}")
    print("====================REQ NO 4. ANSWERS====================")
    print(f"Jugadores en el rango: {lt.size(jugadores)}")
    print(x)


def printPlayersReplace(name, pos, jugadores, rep):
    x = PrettyTable()
    x.field_names = ['Nombre', 'Valor Representativo', 'Age', 'Fecha',
                     'Nacionalidad', 'Valor Contrato', 'Valor Salario', 'Club',
                     'Liga', 'Potencial', 'Overall',
                     'Posiciones', 'Comentarios', 'Tags']

    if lt.size(jugadores) == 0:
        print("No se econtraron valores")

    elif lt.size(jugadores) <= 6:
        for j in lt.iterator(jugadores):
            x.add_row([j['long_name'], j['rep'], j['age'],
                       j['dob'], j['nationality_name'], j['value_eur'], j['wage_eur'],
                       j['club_name'], j['league_name'],
                       j['potential'], j['overall'],
                       j['player_positions'], j['player_traits'],
                       j['player_tags']])
    else:
        for i in range(1, 7):
            ji = lt.getElement(jugadores, i)
            x.add_row([ji['long_name'], ji['rep'], ji['age'],
                       ji['dob'], ji['nationality_name'], ji['value_eur'], ji['wage_eur'],
                       ji['club_name'], ji['league_name'],
                       ji['potential'], ji['overall'],
                       ji['player_positions'], ji['player_traits'],
                       ji['player_tags']])

    print("====================REQ NO 6. INPUTS====================")
    print(f"Para el jugador: #{name}")
    print(f"En la posición: {pos}")
    print("====================REQ NO 6 ANSWERS====================")
    print(f"Jugadores de remplazo posibles: {lt.size(jugadores)}")
    print(f"Valor representativo de {name}: {rep}")
    print(x)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        controller.loadData(control, playerfile)
        print('Jugadores cargados: ' + str(controller.playersSize(control)))
        print("------------------------")
        printInicio(control)

    elif int(inputs[0]) == 2:
        club = input("Ingrese nombre club a buscar: \n")
        jugadores = controller.lastPLayer(club, control)
        total = controller.totalClubPlayers(club, control)
        printLastPlayers(club, jugadores, total)

    elif int(inputs[0]) == 3:
        pos = input("Ingrese posicion a buscar: \n")
        infOv = int(float(input("Ingrese limite inferior para el desempeño a buscar: \n")))
        supOv = int(float(input("Ingrese limite superior para el desempeño a buscar: \n")))
        infPot = int(float(input("Ingrese limite inferior para el potencial a buscar: \n")))
        supPot = int(float(input("Ingrese limite superior para el potencial a buscar: \n")))
        infWage = int(float(input("Ingrese limite inferior para el salario a buscar: \n")))
        supWage = int(float(input("Ingrese limite superior para el salario a buscar: \n")))
        info = [pos, infOv, supOv, infPot, supPot, infWage, supWage]
        jugadores = controller.posPLayers(info, control)
        printPlayersbyPos(info, jugadores)

    elif int(inputs[0]) == 4:
        tag = input("Ingrese el tag a buscar:\n")
        superior = int(input("Ingrese el salario maximo:\n"))
        inferior = int(input("Ingrese el salario minimo:\n"))
        jugadores = controller.tagsAndWage(inferior, superior,
                                           tag, control)
        disponibles = controller.playersSize(control)
        printTagsAndWage(inferior, superior, tag, jugadores, disponibles)

    elif int(inputs[0]) == 5:
        inferior = input("Ingrese el limite inferior para la fecha de nacimiento:\n")
        superior = input("Ingrese el limite superior para la fecha de nacimiento:\n")
        trait = input("Ingrese la caracteristica a buscar:\n")
        jugadores = controller.playersbyTrait(trait, inferior, superior, control)
        printPlayersbyTrait(inferior, superior, trait, jugadores)

    elif int(inputs[0]) == 6:
        segmentos = int(input("Numero de segmentos:\n"))
        niveles = int(input("Ingrese niveles:\n"))
        propiedad = None
        print("""
        Propiedades:
        1. Overall.
        2. Potential.
        3. Value_eur.
        4. Wage_eur.
        5. Age.
        6. Height_cm
        7. Weigth_kg
        8. Release_clause_eur
              """)
        opcion = int(input("Ingrese propiedad a buscar:\n"))
        if opcion == 1:
            propiedad = "overall"
        elif opcion == 2:
            propiedad = "potential"
        elif opcion == 3:
            propiedad = "value_eur"
        elif opcion == 4:
            propiedad = "wage_eur"
        elif opcion == 5:
            propiedad = "age"
        elif opcion == 6:
            propiedad = "height_cm"
        elif opcion == 7:
            propiedad = "weight_kg"
        elif opcion == 8:
            propiedad = "release_clause_eur"
        else:
            print("propiedad no valida")

        bin, count, lvl, mark, mayor, menor = controller.histograma(segmentos, niveles, propiedad, control)
        printHistograma(bin, count, lvl, mark, mayor, menor, segmentos, niveles, propiedad)

    elif int(inputs[0]) == 7:
        name = input("Ingrese el nombre corto del jugador sustituido:\n")
        pos = input("Ingrese la posicion a buscar:\n")
        jugadores, rep = controller.playerReplace(name, pos, control)
        if jugadores == None:
            print("No se encontro al jugador")
        else:
            printPlayersReplace(name, pos, jugadores, rep)

    else:
        sys.exit(0)
sys.exit(0)
