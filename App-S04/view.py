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
assert cf
import pandas as pd
import tabulate
import datetime

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def getFirtLastN(lista, N):
    FirstLast =  lt.newList(datastructure = "ARRAY_LIST")
    size = lt.size(lista)
    for i in range(1,N+1):
        lt.addLast(FirstLast, lt.getElement(lista, i))
    for i in range(size-(N-1),size+1):
        lt.addLast(FirstLast, lt.getElement(lista, i))
    return FirstLast

#Carga de datos
def printPlayers(catalog):
    print("\nLos primeros y últimos cinco jugadores son: ")

    lista = [["Info. general", "Info. dinero (EUR)", "Info. liga/club", "Info. reputación"]]
    sub_list = getFirtLastN(catalog["players"], 5)
    for i in range(1, lt.size(sub_list)+1):
        player = lt.getElement(sub_list, i)
        info_general = "Nombre: " + player["short_name"] + " - Edad: " + player["age"] +  " - Altura: " + player["height_cm"]+  " - Peso: " + player["weight_kg"] + " - Nacionalidad: " + player["nationality_name"]
        info_dinero = "Valor: " + player["value_eur"] + " - Salario: " + player["wage_eur"]+ " - Cláusula de liberación: " + player["release_clause_eur"]
        info_liga = "Liga: " + player["league_name"] + " - Club: " + player["club_name"] + " - Fecha de vinculación al club: " + player["club_joined"]
        info_reputacion = "Posiciones en que juega: " + player["player_positions"] + " - Overall: " + player["overall"] + " - Reputación internacional: " + player["international_reputation"] + " - Tags: " + player["player_tags"] + " - Comentarios: " + player["player_traits"]
        lista2 = [info_general, info_dinero, info_liga, info_reputacion]
        s = pd.Series(lista2).str.wrap(25)
        lista.append(s)
    print(tabulate.tabulate(lista,  tablefmt = "grid"))

# Requerimiento 1
def printPlayerByClub(sub_list):
    lista = [["Name", "Age", "dob", "Overall", "Nationality", "value_eur", "wage_eur", "release_clause_eur", "club_joined", "player_positions", "club_position", "player_traits", "player_tags"]]
    for player in lt.iterator(sub_list): 
        lista2 = [player["short_name"], player["age"], str(player["dob"].date()), player["overall"], player["nationality_name"], player["value_eur"], player["wage_eur"], player["release_clause_eur"], player["club_joined"], player["player_positions"], player["club_position"], player["player_traits"], player["player_tags"]]        
        s = pd.Series(lista2).str.wrap(20)
        lista.append(s)
        league_name = player["league_name"]
        league_level = player["league_level"]
    print("\n----- League Details -----")
    print("     * Name:", league_name)
    print("     * Category:", league_level)
    print("\nThe last 5 team adquisitions are:")
    print(tabulate.tabulate(lista,  tablefmt = "grid"))

#Requerimiento 2
def printPlayersByPositionInRange(lista):
    tabla = [["Overall", "potential", "short_name","dob", "Age", "player_positions", "Nationality", "value_eur", "wage_eur", "release_clause_eur","player_tags","player_traits"]]
    
    if lt.size(lista) > 6:
        lista = getFirtLastN(lista, 3)

    for player in lt.iterator(lista):    
        fila = [player["overall"], player["potential"], player["short_name"], str(player["dob"].date()), player["age"], player["player_positions"], player["nationality_name"],player["value_eur"], player["wage_eur"],player["release_clause_eur"], player["player_tags"],  player["player_traits"]]        
        s = pd.Series(fila).str.wrap(15)
        tabla.append(s)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))
    
# Requerimiento 3
def printPlayerBySalaryTag(lista):
    tabla = [["Name", "Age", "dob", "Nationality", "value_eur", "wage_eur", "club_name", "league_name","Potential", "Overall", "player_positions", "player_traits", "player_tags"]]
    if lt.size(lista) > 6:
        lista = getFirtLastN(lista, 3)
    
    for player in lt.iterator(lista):
        lista2 = [player["long_name"], player["age"], str(player["dob"].date()), player["nationality_name"], player["value_eur"], player["wage_eur"], player["club_name"], player["league_name"], player["potential"], player["overall"], player["player_positions"], player["player_traits"], player["player_tags"]]     
        s = pd.Series(lista2).str.wrap(20)
        tabla.append(s)
        
    print("\nThe players in range are:")
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

#Requerimiento 4
def printPlayersByDobTraits(lista):
    tabla = [["dob", "Overall", "potential", "long_name", "Age", "league_name", "club_name", "player_positions", "Nationality", "value_eur", "wage_eur", "club_position", "player_tags","player_traits"]]
    
    if lt.size(lista) > 6:
        lista = getFirtLastN(lista, 3)

    for player in lt.iterator(lista):    
        fila = [str(player["dob"].date()), player["overall"], player["potential"], player["long_name"], player["age"], player["league_name"], player["club_name"], player["player_positions"], player["nationality_name"],player["value_eur"], player["wage_eur"], player["club_position"], player["player_tags"], player["player_traits"]]        
        s = pd.Series(fila).str.wrap(15)
        tabla.append(s)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

#Requerimiento 5
def printHistogramByProperty(dic):
    tabla = [["bin", "count", "lvl", "mark"]]
    llaves = list(dic.keys())
    for llave in llaves:
        fila = ["("+str(round(llave[0], 3))+", "+str(round(llave[1],3))+"]", str(dic[llave]["count"]), str(dic[llave]["lvl"]), dic[llave]["mark"]]
        s = pd.Series(fila).str.wrap(30)
        tabla.append(s)
    print(tabulate.tabulate(tabla, tablefmt = "grid"))
    
#Requerimiento 6 (BONO)
def printPlayersMoreSimilar(lista):
    print("\nLos primeros y últimos tres jugadores son: ")
    if lt.size(lista) > 6:
        lista = getFirtLastN(lista, 3)
   
    tabla = [["Valor Representativo", "Info. general", "Info. dinero (EUR)", "Info. liga/club", "Info. reputación"]]    
    for i in range(1, lt.size(lista)+1):
        player = lt.getElement(lista, i)
        info_general = "Nombre: " + player["short_name"] + " - Edad: " + player["age"] +  " - Altura: " + player["height_cm"]+  " - Fecha de nacimiento: " + str(player["dob"].date()) + " - Nacionalidad: " + player["nationality_name"]
        info_dinero = "Valor del contrato: " + player["value_eur"] + " - Salario: " + player["wage_eur"] #+ " - Cláusula de liberación: " + player["release_clause_eur"]
        info_liga = "Liga: " + player["league_name"] + " - Club: " + player["club_name"] #+ " - Fecha de vinculación al club: " + player["club_joined"]
        info_reputacion = " - Potencial: " + player["potential"] + " - Overall: " + player["overall"] + "- Posiciones en que juega: " + player["player_positions"] + " - Tags: " + player["player_tags"] + " - Comentarios: " + player["player_traits"]
        fila = [str(player["vr"]), info_general, info_dinero, info_liga, info_reputacion]
        s = pd.Series(fila).str.wrap(25)
        tabla.append(s)
    print(tabulate.tabulate(tabla,  tablefmt = "grid"))

def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información en el catálogo")
    print("3- Reportar las cinco adquisiciones más recientes de un club")
    print("4- Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario")
    print("5- Reportar los jugadores dentro de un rango salarial y con cierta etiqueta")
    print("6- Reportar los jugadores con cierto rasgo característico y nacidos en un periodo de tiempo")
    print("7- Graficar el histograma de una propiedad para los jugadores FIFA")
    print("8- Encontrar posibles sustituciones para los jugadores FIFA")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        print("\nInicializando....") 
        catalog = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(catalog)
        print('Jugadores cargados: ' + str(controller.playersSize(catalog)))
        printPlayers(catalog)

    #Requerimiento 1
    elif int(inputs[0]) == 3:
        club = input("Ingrese el nombre del club: ")
        answer = controller.getPlayersByClub(catalog, club)
        if answer != None:
            adquisiciones = answer[0]
            sub_list = answer[1]
            print("\n=============== Req No. 1 Inputs ===============")
            print("The TOP 5 most recent adquisitions of the", club)
            print("\n=============== Req No. 1 Answer ===============")
            print("The", club, "has", adquisiciones, "adquisitions.")
            printPlayerByClub(sub_list)
        else:
            print("el nombre del club no existe en el catalogo")
    
    #Requerimiento 2
    elif int(inputs[0]) == 4:
        overall_lo = int(float(input("Ingrese límite inferior para el desempeño global del jugador: ")))
        overall_hi = int(float(input("Ingrese límite superior para el desempeño global del jugador: ")))
        potential_lo = int(float(input("Ingrese límite inferior para el potencial del jugador: ")))
        potential_hi = int(float(input("Ingrese límite superior para el potencial del jugador: ")))
        wage_lo = int(float(input("Ingrese límite inferior del salario recibido por los jugadores: ")))
        wage_hi = int(float(input("Ingrese límite superior del salario recibido por los jugadores: ")))
        position = input("Ingrese la posición del jugador: ")
        lista = controller.getPlayersByPositionInRange(catalog, position, overall_lo, overall_hi, potential_lo, potential_hi, wage_lo, wage_hi)
        print("\n=============== Req. No. 2 Inputs ===============")
        print("Search for players in position:", position)
        print("----- With Search Ranges of -----")
        print("     * 'overall' range between", overall_lo, "and", overall_hi)
        print("     * 'potential' range between", potential_lo, "and", potential_hi)
        print("     * 'wage_eur' range between", wage_lo, "and", wage_hi)
        print("\n=============== Req No. 2 Answer ===============")
        print("Available FIFA players:", controller.playersSize(catalog))
        print("Players found in range: ", lt.size(lista), "and Position:", position)
        print("The first 3 and last 3 players in range are: ")
        printPlayersByPositionInRange(lista)

    #Requerimiento 3
    elif int(inputs[0]) == 5:
        salarylo = float(input("Ingrese límite inferior del salario recibido por los jugadores: "))
        salaryhi = float(input("Ingrese límite superior del salario recibido por los jugadores: "))
        tag = input("Ingrese el tag/caracteristica que identifica a los jugadores: ")
        lista = controller.getPlayersBySalaryTags(catalog, salarylo, salaryhi, tag)
        print("\n=============== Req. No. 3 Inputs ===============")
        print("Search for players with tag:", tag)
        print("----- With Search Ranges of -----")
        print("     * 'wage_eur' range between", salarylo, "and", salaryhi)
        print("\n=============== Req No. 3 Answer ===============")
        print("Available FIFA players:", controller.playersSize(catalog))
        print("Players found in range: ", lt.size(lista), "and Tag:", tag)
        printPlayerBySalaryTag(lista)

    #Requerimiento 4
    elif int(inputs[0]) == 6:
        dob_lo = input("Ingrese límite inferior de la fecha de nacimiento del jugador: ")
        dob_hi = input("Ingrese límite superior de la fecha de nacimiento del jugador: ")
        trait = input("Ingrese una de las características que identifican a los jugadores (player_traits): ")
        lista = controller.getPlayersByDobTraits(catalog, dob_lo, dob_hi, trait)
        print("\n=============== Req. No. 4 Inputs ===============")
        print("Search for players with tag:", trait)
        print("----- With Search Ranges of -----")
        print("     * 'dob' range between", dob_lo, "and", dob_hi)
        print("\n=============== Req No. 4 Answer ===============")
        print("Available FIFA players:", controller.playersSize(catalog))
        print("Players found in range: ", lt.size(lista), "and Tag:", trait)
        print("The first 3 and last 3 players in range are: ")
        printPlayersByDobTraits(lista)
    
    #Requerimiento 5
    elif int(inputs[0]) == 7:
        N = int(input("Ingrese número de segmentos en que se divide el rango de propiedad en el histograma (N): "))
        x = int(input("Ingrese número de niveles en que se dividen las marcas de jugadores en el histograma (x): "))
        propiedad = input("Ingrese propiedad de la cual se va a hacer el histograma: ")
        req5 = controller.getHistogramByProperty(catalog, N, x, propiedad)
        diccionario = req5[0]
        total = req5[1]
        llave_min, llave_max = req5[2], req5[3]
        print("\n=============== Req No. 5 Inputs ===============")
        print("Count map (histogram) of:", propiedad)
        print("Number of bins:", N)
        print("Players scale:", x)
        print("\n=============== Req No. 5 Answer ===============")
        print("There are", controller.playersSize(catalog), "players on record.")
        print("The histogram counts", total, "players.")
        print("The minimum and maximum value of property", propiedad, "is:", llave_min, "and", llave_max)
        print(propiedad, "Histogram with", N, "bins and", x, "players per lvl mark.")
        printHistogramByProperty(diccionario)
        print("NOTE: Each '*' represents", x, "players.")        

    #Requerimiento 6 (BONO)
    elif int(inputs[0]) == 8:
        short_name = input("Ingrese el nombre corto del jugador: ")
        position = input("Ingrese la posición del jugador: ")
        answer = controller.getPlayersMoreSimilar(catalog, short_name, position)
        if answer != None:
            player_goal, numberPlayersInPosition, playersMoreSimilar = answer
            print("\n=============== Req No. 6 Inputs ===============")
            print("Jugadores que puedan sustituir a", short_name, "(nombre largo:\"", player_goal["long_name"], "\") en su posición de", position)
            print("\n=============== Req No. 6 Answer ===============")
            print("Players found in position:", numberPlayersInPosition)
            print("Players with VR more similar to", player_goal["vr"], ":", lt.size(playersMoreSimilar))
            printPlayersMoreSimilar(playersMoreSimilar)
        else:
            print("Jugador no encontrado")
    else:
        sys.exit(0)

sys.exit(0)
