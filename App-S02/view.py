"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * along withthis program.If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from prettytable import PrettyTable, ALL
assert cf

default_limit = 10000
sys.setrecursionlimit(default_limit * 10000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

fifafile = 'FIFA/fifa-players-2022-utf8-large.csv'
cont = None

def printMenu():
    print("\nBienvenido querido usuario <3:")
    print("1- Cargar información en el catálogo")
    print("2- Reportar las cinco adquisiciones más recientes de un club")
    print("3- Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario")
    print("4- Reportar los jugadores dentro de un rango salarial y con cierta etiqueta")
    print("5- Reportar los jugadores con cierto rasgo característico y nacidos en un periodo de tiempo")
    print("6- Graficar el histograma de una propiedad para los jugadores FIFA")
    print("7- Encontrar posibles sustituciones para los jugadores FIFA")
    print("0- Salir")

def printSimplePrettyTable(fifaList, keys):
    table = PrettyTable()
    table.max_width = 20
    table.hrules = ALL
    table.field_names = keys
    rows = []
    for element in lt.iterator(fifaList):
        row = []
        for key in keys:
            if key == 'mark':
                table.align["mark"] = "l"
            strElement = str(element[key])
            if len(strElement) > 20:
                strElement = strElement[:20]
            row.append(strElement)
        rows.append(row)
    table.add_rows(rows)
    print(table)

def printHeaders(reqNum, firstMessage, secondMessage):
    print("\n============= Req No. " + str(reqNum) + " Inputs =============")
    print(firstMessage)
    print("\n============= Req No. " + str(reqNum) + " Answer =============" )
    print(secondMessage)

def printHeadersTop(reqNum, firstMessage):
    print("\n============= Req No. " + str(reqNum) + " Inputs =============")
    print(firstMessage)

def printHeadersBottom(reqNum, secondMessage):
    print("============= Req No. " + str(reqNum) + " Answer =============" )
    print(secondMessage)

def printSearchRange(*args):
    print("\n----- With Search Ranges of -----")

    for tag in args:
        tagsearch = tag[0]
        lower = tag[1]
        upper = tag[2]
        print("     * " + str(tagsearch) + " range between " + str(lower) + " and " + str(upper) + '\n')

def printLeagueDetails(fifaList):
    name = lt.getElement(fifaList,1)['league_name']
    category = int(float(lt.getElement(fifaList,1)['league_level']))
    print("\n----- League Details -----")
    print("     * Name: " + str(name))
    print("     * Category: "  + str(category))

def printPropertiesMenu():
    print("\n----- Properties -----")
    dictProperties = {1: 'Overall', 2: 'Potential', 3: 'Value_eur', 4: 'Wage_eur', 5: 'Age', 6: 'Height_cm', 7: 'Weight_kg', 8: 'Release_clause_eur'}
    for property in dictProperties:
        print(str(property) + ". " + str(dictProperties[property]))
    try:
        desiredProperty = int(input('Ingrese la propiedad de la cual desea hacer el histograma: ').strip())
        propertySelected = dictProperties.get(desiredProperty)
        if propertySelected:
            print('La propiedad seleccionada fue: ' + str(propertySelected) + '\n')
        else:
            print('Ingreso incorrecto, intente de nuevo. >:/' + '\n')
        return propertySelected
    except:
        print('Ingreso incorrecto, intente de nuevo. >:/' + '\n')
        return  None

"""
Menu principal
"""
while True:
    try:
        printMenu()
        inputs = input('Seleccione una opción para continuar: ')
        if int(inputs[0]) == 1:
            print("\nInicializando....")
            cont = controller.init()
            print("\nCargando la información de FIFA players ....")
            controller.loadData(cont, fifafile)
            print('Jugadores cargados: ' + str(controller.playersSize(cont)))
            loadedPlayers = controller.answerLst(cont['players'], 5)
            printSimplePrettyTable(loadedPlayers, ['short_name','age','height_cm','weight_kg','nationality_name'])

        elif int(inputs[0]) == 2:
            clubName = input('Ingrese el nombre del club que desea consultar: ').strip()
            playersByClubName, howMany, treeHeight, treeSize, totalAdquisitions = controller.playersByClubName(cont, clubName)
            if lt.size(playersByClubName) != 0:
                firstMessage = 'The TOP 5 most recent adquisition of the ' + str(clubName)
                secondMessage = 'There ' + str(clubName) + ' has ' + str(totalAdquisitions) + ' adquisitions.'
                printHeaders(1, firstMessage, secondMessage)
                printLeagueDetails(playersByClubName)
                print('\n The last ' + str(howMany) + ' team adquisitions are:')
                printSimplePrettyTable(playersByClubName, ['club_joined','age', 'dob', 'short_name', 'overall', 'nationality_name', 'value_eur', 'wage_eur', 'release_clause_eur', 'club_contract_valid_until', 'player_positions', 'club_position', 'player_tags', 'player_traits'])
                print('La altura del arbol del club ' + clubName + ' es: ' + str(treeHeight))
                print('La cantidad de elementos del arbol del club ' + clubName + ' es: ' + str(treeSize))
            else:
                input('No se encontraron jugadores. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 3:
            player_position = input('Ingrese la posicion del jugador que desea consultar: ').strip()
            player_position = player_position.upper()
            overallLower = int(input('Ingrese el limite inferior del overall de los jugadores: ').strip())
            overallUpper = int(input('Ingrese el limite superior del overall de los jugadores: ').strip())
            potentialLower = int(input('Ingrese el limite inferior del potencial de los jugadores: ').strip())
            potentialUpper = int(input('Ingrese el limite superior del potencial de los jugadores: ').strip())
            wageLower = int(input('Ingrese el limite inferior del salario recibido por los jugadores: ').strip())
            wageUpper = int(input('Ingrese el limite superior del salario recibido por los jugadores: ').strip())
            playersByPosition, howMany = controller.playersByPosition(cont, player_position, overallLower, overallUpper, potentialLower,potentialUpper, wageLower, wageUpper)
            if lt.size(playersByPosition) != 0:
                firstMessage = 'Search for players in position: ' + str(player_position)
                secondMessage = 'Available FIFA players: ' + str(controller.playersSize(cont)) + '\n' + 'Player found in range: ' + str(howMany) + ' and position: ' + player_position
                printHeadersTop(2, firstMessage)
                printSearchRange(('overall', overallLower, overallUpper), ('potential', potentialLower, potentialUpper), ('wage_eur', wageLower, wageUpper))
                printHeadersBottom(2, secondMessage)
                if howMany > 6:
                    print('The first 3 and last 3 players in range are: ')
                else:
                    print('The only ' + str(howMany) + ' players in range are: ')
                printSimplePrettyTable(playersByPosition, ['overall', 'potential', 'wage_eur', 'short_name', 'dob', 'age', 'player_positions', 'nationality_name', 'value_eur', 'release_clause_eur', 'club_position', 'player_tags', 'player_traits'])
            else:
                input('No se encontraron jugadores. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 4:
            player_tag = input('Ingrese el nombre de la caracteristica (tag) que desea consultar: ').strip()
            player_tag = '#' + player_tag
            lower = int(input('Ingrese el limite inferior del salario recibido por los jugadores: ').strip())
            upper = int(input('Ingrese el limite superior del salario recibido por los jugadores: ').strip())
            playersByTag, howMany = controller.playersByTag(cont, player_tag, lower, upper)
            if lt.size(playersByTag) != 0:
                firstMessage = 'Search for players with tag: ' + player_tag
                secondMessage = 'Available FIFA players: ' + str(controller.playersSize(cont)) + '\n' + 'Player found in range: ' + str(howMany) + ' and tag: ' + player_tag
                printHeadersTop(3, firstMessage)
                printSearchRange((player_tag, lower, upper))
                printHeadersBottom(3, secondMessage)
                if howMany > 6:
                    print('The first 3 and last 3 players in range are: ')
                else:
                    print('The only ' + str(howMany) + ' players in range are: ')
                printSimplePrettyTable(playersByTag, ['wage_eur', 'overall','potential', 'long_name', 'dob', 'age', 'league_name','club_name', 'player_positions', 'nationality_name', 'value_eur', 'release_clause_eur', 'club_position', 'player_tags', 'player_traits'])
            else:
                input('No se encontraron jugadores. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 5:
            trait = input('Ingrese el trait que desea consultar: ').strip()
            dobMin = input('Ingrese la fecha minima de nacimiento: ').strip()
            dobMax = input('Ingrese la fecha maxima de nacimiento: ').strip()
            playersByTraits, howMany = controller.playersByTraits(cont, trait, dobMin, dobMax)
            if lt.size(playersByTraits) != 0:
                firstMessage = 'Search for players with tag: ' + trait
                secondMessage = 'Available FIFA players: ' + str(controller.playersSize(cont)) + '\n' + 'Player found in range: ' + str(howMany) + ' and tag: ' + trait
                printHeadersTop(4, firstMessage)
                printSearchRange(('dob', dobMin, dobMax))
                printHeadersBottom(4, secondMessage)
                if howMany > 6:
                    print('The first 3 and last 3 players in range are: ')
                else:
                    print('The only ' + str(howMany) + ' players in range are: ')
                printSimplePrettyTable(playersByTraits, ['dob', 'overall', 'potential', 'long_name', 'age', 'league_name', 'club_name', 'player_positions', 'nationality_name', 'value_eur', 'wage_eur', 'release_clause_eur', 'club_position', 'player_tags', 'player_traits'])
            else:
                input('No se encontraron jugadores. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 6:
            selection = None
            while selection == None:
                selection = printPropertiesMenu()
            bins = int(input('Ingrese el numero de segmentos que desea visualizar: ').strip())
            mark = int(input('Ingrese el numero de niveles que desee visualizar: ').strip())
            playersByProperties, howMany = controller.playersByProperties(cont, bins, mark, selection)

            firstMessage = 'Count map (histogram) of: ' + str(selection) + '\nNumber of bins: ' + str(bins) + '\nNumber of levels: ' + str(mark)
            secondMessage = 'There are ' + str(controller.playersSize(cont)) + ' players on record.' + '\n' + 'The histogram counts ' + str(howMany)  + ' players.' + '\n' + str(selection) + 'Histogram with ' + str(bins) + ' bins and ' + str(mark) + ' per lvl mark.'
            printHeaders(5, firstMessage, secondMessage)
            printSimplePrettyTable(playersByProperties, ['bin', 'count', 'lvl', 'mark'])


        elif int(inputs[0]) == 7:
            playerSNameIN = input('Ingrese el nombre corto del jugador que necesita sustituir: ').strip()
            playersLt, namesakeCount = controller.UXSearch(cont,playerSNameIN)
            print('El jugador de FIFA ' + str(playerSNameIN) + ' tiene '+ str(namesakeCount - 1)+ ' homonimos.')
            playerSName = lt.getElement(playersLt, 1)
            if namesakeCount > 1:
                i = 0
                for player in lt.iterator(playersLt):
                    i = i + 1
                    print(str(i) + '. ' + str(player['short_name']) + ' Player Positions: ' + str(player['player_positions']) + ' Club: ' + str(player['club_name']) )
                namesake = int(input('Ingrese el homonimo que desea: ').strip())
                playerSName = lt.getElement(playersLt, namesake)
            playerPosition = input('Ingrese la posicion del jugador que desea consultar: ').strip().upper()
            playersBySustitution, howMany, totalPlayersPosition = controller.playerForSutitution(cont, playerSName, playerPosition)
            if lt.size(playersBySustitution) != 0:
                firstMessage = 'The possible sustitution for ' + str(playerSNameIN)
                secondMessage = 'Available FIFA players: ' + str(controller.playersSize(cont)) + '\n' + 'There are ' + str(totalPlayersPosition) + ' players with the position: ' + str(playerPosition) + '\nThere are ' + str(howMany) + ' possible sustitutions for ' + str(playerSNameIN)+ '.'
                printHeaders('6 (BONO)', firstMessage, secondMessage)
                specialkey = playerPosition + 'vr'
                printSimplePrettyTable(playersBySustitution, [specialkey, 'wage_eur', 'overall','potential', 'long_name', 'dob', 'age', 'league_name','club_name', 'player_positions', 'nationality_name', 'value_eur', 'release_clause_eur', 'club_position', 'player_tags', 'player_traits'])

            else:
                input('No se encontraron jugadores. Oprima ENTER para continuar...')

        elif int(inputs[0]) == 0:
            break
    except:
        input("Ingreso una opcion invalida, intentelo de nuevo. Oprima ENTER para continuar...")
        continue
sys.exit(0)
