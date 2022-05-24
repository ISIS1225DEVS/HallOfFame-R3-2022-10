"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from math import ceil
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mg
from datetime import datetime as dt
assert cf

# ___________________________________________________
# Construccion de modelos
# ___________________________________________________


def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {'players': None,
                'clubIndex': None
                }

    analyzer['players'] = lt.newList('ARRAY_LIST', compareIds)
    """
    players es una lista donde se almacenan todos los jugadores de todos
    los clubes.
    """

    analyzer["clubIndex"] = mp.newMap(500,
                                      maptype='PROBING',
                                      loadfactor=0.5,)
    """
    clubIndex es un map cuyas llaves son los nombres de los clubes y cada valor
    es un arbol con los jugadores del club organizado por sus fechas de ingreso
    y sus valores son listas donde se guardan los jugaodres.
    """

    analyzer['clubIndex_num'] = mp.newMap(500,
                                          maptype='PROBING',
                                          loadfactor=0.5)
    """
    clubIndex_num es un mapa que guarda como llave los nombres de los clubes
    y como valor un marcador que indica el total de jugadores en dicho club.
    """

    analyzer["posIndex"] = mp.newMap(43,
                                     maptype='PROBING',
                                     loadfactor=0.5,
                                     )
    """
    posIndex es un mapa que guarda como llave las posiciones de los jugadores
    y como valor una lista de jugadores que juegan en esa posicion.
    """

    analyzer["tagIndex"] = mp.newMap(21,
                                     maptype='PROBING',
                                     loadfactor=0.5)
    """
    tagIndex es un mapa cuyas llaves son tags y sus valores son arboles que
    guardan jugadores segun su 'wage_eur'.
    """

    analyzer["traitIndex"] = mp.newMap(2000,
                                       maptype='PROBING',
                                       loadfactor=0.5,
                                       )
    """
    traitIndex es un mapa cuyas llaves son traits y sus valores son arboles que
    guardan jugadores segun su 'dob'.
    """

    analyzer["propertyIndex"] = mp.newMap(17,
                                          maptype='PROBING',
                                          loadfactor=0.5,
                                          )
    """
    propertyIndex es un mapa cuyas llaves son diferentes propiedades de cada jugador:
    (overall, potential, value_eur, wage_eur, age, height_cm, weight_kg, release_clause_eur)
    y sus valores son arboles que guardan jugadores segun su la propiedad respectiva.
    """

    analyzer["nameIndex"] = mp.newMap(36157,
                                      maptype='PROBING',
                                      loadfactor=0.5,
                                      )
    """
    name index es un mapa cuyas llaves son los nombres "short_name" de cada jugador
    y sus valores son el jugador respectivo.
    """

    analyzer["min-max"] = {"potential": [1000000, 0], "age": [1000000, 0], "height_cm": [1000000, 0], "value_eur": [1000000, 0]}
    """
    name index es un mapa cuyas llaves son los nombres "short_name" de cada jugador
    y sus valores son el jugador respectivo.
    """
    return analyzer

# ___________________________________________________
# Funciones para agregar informacion al catalogo
# ___________________________________________________


def addPlayer(analyzer, player):
    neoPlayer = newPlayer(player)
    lt.addLast(analyzer['players'], neoPlayer)

    # ___________________________________________________
    # Indice por Culbs
    # ___________________________________________________
    if not mp.contains(analyzer['clubIndex'], neoPlayer['club_name'].lower()):
        # se crea arbol
        playerTree = om.newMap(omaptype='RBT', comparefunction=compareDates)
        updateDateIndex(playerTree, neoPlayer)
        mp.put(analyzer['clubIndex'], neoPlayer['club_name'].lower(),
               playerTree)
        mp.put(analyzer['clubIndex_num'], neoPlayer['club_name'].lower(), 1)

    elif mp.contains(analyzer['clubIndex'], neoPlayer['club_name'].lower()):
        key = mp.get(analyzer['clubIndex'], neoPlayer['club_name'].lower())
        value = me.getValue(key)
        # Value = Arbol
        key1 = mp.get(analyzer['clubIndex_num'],
                      neoPlayer['club_name'].lower())
        value1 = me.getValue(key1)
        value1 += 1
        mp.put(analyzer['clubIndex_num'], neoPlayer['club_name'].lower(),
               value1)
        updateDateIndex(value, neoPlayer)
    # ___________________________________________________
    # Indice por Posicion
    # ___________________________________________________
    for pos in neoPlayer['player_positions'].split(","):
        pos = pos.lower().strip()
        if not mp.contains(analyzer['posIndex'], pos):
            # se crean multiples arboles
            # arbol por "overall"
            playerOverall = om.newMap(omaptype='RBT', comparefunction=compareNumbers)
            updateNumericalIndex("overall", playerOverall, neoPlayer)
            # arbol por "potential"
            playerPotetial = om.newMap(omaptype='RBT', comparefunction=compareNumbers)
            updateNumericalIndex("potential", playerPotetial, neoPlayer)
            # arbol por "wage_eur"
            playerWage = om.newMap(omaptype='RBT', comparefunction=compareNumbers)
            updateNumericalIndex("wage_eur", playerWage, neoPlayer)
            # arbol por "Rep Number" BONO:
            playerRep = om.newMap(omaptype='RBT', comparefunction=compareNumbers)
            updateRepIndex(analyzer["min-max"], playerRep, neoPlayer)
            playerTuple = playerOverall, playerPotetial, playerWage, playerRep
            mp.put(analyzer['posIndex'], pos, playerTuple)

        elif mp.contains(analyzer['posIndex'], pos):
            key = mp.get(analyzer['posIndex'], pos)
            value = me.getValue(key)
            # Value -> Tupla
            updateNumericalIndex("overall", value[0], neoPlayer)
            updateNumericalIndex("potential", value[1], neoPlayer)
            updateNumericalIndex("wage_eur", value[2], neoPlayer)
            updateRepIndex(analyzer["min-max"], value[3], neoPlayer)
    # ___________________________________________________
    # Indice por Tags
    # ___________________________________________________
    for tag in neoPlayer['player_tags'].split(","):
        tag = tag.strip()
        if tag == "":
            tag = "unknown"
        if not mp.contains(analyzer['tagIndex'], tag):
            # se crea arbol
            playerTree = om.newMap(omaptype='RBT', comparefunction=compareIds)
            updateNumericalIndex("wage_eur", playerTree, neoPlayer)
            mp.put(analyzer['tagIndex'], tag, playerTree)

        elif mp.contains(analyzer['tagIndex'], tag):
            key = mp.get(analyzer['tagIndex'], tag)
            value = me.getValue(key)
            # Value -> Arbol
            updateNumericalIndex("wage_eur", value, neoPlayer)
    # ___________________________________________________
    # Indice por traits
    # ___________________________________________________
    for trait in neoPlayer['player_traits'].split(","):
        trait = trait.lower().strip()
        if not mp.contains(analyzer['traitIndex'], trait):
            # se crea arbol
            playerTree = om.newMap(omaptype='RBT', comparefunction=compareDobs)
            updateDobIndex(playerTree, neoPlayer)
            mp.put(analyzer['traitIndex'], trait, playerTree)

        elif mp.contains(analyzer['traitIndex'], trait):
            key = mp.get(analyzer['traitIndex'], trait)
            value = me.getValue(key)
            # Value -> Arbol
            updateDobIndex(value, neoPlayer)
    # ___________________________________________________
    # Indice por properties
    # ___________________________________________________
    properties = ["overall", "potential", "value_eur", "wage_eur",
                  "age", "height_cm", "weight_kg", "release_clause_eur"]
    if not mp.contains(analyzer['propertyIndex'], "overall"):
        # se crean arboles
        for property in properties:
            # Overall
            Tree = om.newMap(omaptype='RBT', comparefunction=compareNumbers)
            updateNumericalIndex(property, Tree, neoPlayer)
            mp.put(analyzer['propertyIndex'], property, Tree)
    else:
        for property in properties:
            key = mp.get(analyzer['propertyIndex'], property)
            value = me.getValue(key)
            # Value -> Arbol
            updateNumericalIndex(property, value, neoPlayer)

    # ___________________________________________________
    # Indice por short_names
    # ___________________________________________________
    name = neoPlayer['short_name'].lower().strip()
    if not mp.contains(analyzer['nameIndex'], name):
        # se crea nodo
        mp.put(analyzer['nameIndex'], name, neoPlayer)

    return analyzer

def normalizer(analyzer, player):
    properties = ["potential", "age", "height_cm", "value_eur"]
    for prop in properties:
        if player[prop] != "":
            if int(float(player[prop])) < analyzer["min-max"][prop][0]:
                analyzer["min-max"][prop][0] = int(float(player[prop]))
            if int(float(player[prop])) > analyzer["min-max"][prop][1]:
                analyzer["min-max"][prop][1] = int(float(player[prop]))


# ___________________________________________________
# Funciones para creacion de datos
# ___________________________________________________


def newPlayer(player):
    """
    Esta función cambia las columnas de fecha a formato datetime
    """
    tags = player['player_tags']
    carac = "#"
    if tags == "":
        player['player_tags'] = 'unknown'
    else:
        for x in range(len(carac)):
            tags = tags.replace(carac[x], "")
        player['player_tags'] = tags.lower().strip()

    dob = player['dob']
    player['wage_eur'] = int(float(player['wage_eur']))
    player['overall'] = int(float(player['overall']))
    player['potential'] = int(float(player['potential']))
    player['age'] = int(float(player['age']))
    player['height_cm'] = int(float(player['height_cm']))
    player['weight_kg'] = int(float(player['weight_kg']))
    player['sofifa_id'] = int(player['sofifa_id'])

    if player['release_clause_eur'] == "":
        player['release_clause_eur'] = "unknown"
    else:
        player['release_clause_eur'] = int(float(player['release_clause_eur']))

    if player['value_eur'] == "":
        player['value_eur'] = "unknown"
    else:
        player['value_eur'] = int(float(player['value_eur']))

    try:
        dob_format = dt.strptime(dob, "%Y-%m-%d")
        dob = dob_format
    except ValueError:
        dob = str(int(float(dob)))
        dob_format = dt.strptime(dob, "%Y")
        dob = dob_format

    joined = player['club_joined']
    try:
        joined_format = dt.strptime(joined, "%Y-%m-%d")
        joined = joined_format
    except ValueError:
        joined = str(int(float(joined)))
        joined_format = dt.strptime(joined, "%Y")
        joined = joined_format

    contract = player["club_contract_valid_until"]
    try:
        contract_format = dt.strptime(contract, "%Y-%m-%d")
        contract = contract_format
    except ValueError:
        contract = str(int(float(contract)))
        contract_format = dt.strptime(contract, "%Y")
        contract = contract_format

    return player


def updateDateIndex(map, player):
    """
    CHECKEA que la fecha de cada jugador no se repita por club
    y añade cada fecha/jugador al arbol
    """
    occurreddate = player['club_joined']
    entry = om.get(map, occurreddate)

    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        lt.addLast(listPlayers, player)
        om.put(map, occurreddate, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map


def updateWageIndex(map, player):
    """
    CHECKEA que la fecha de cada jugador no se repita por club
    y añade cada fecha/jugador al arbol
    """
    wage = int(float(player['wage_eur']))
    entry = om.get(map, wage)

    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        lt.addLast(listPlayers, player)
        om.put(map, wage, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map


def updateDobIndex(map, player):
    """
    CHECKEA que la fecha de cada jugador no se repita por club
    y añade cada fecha/jugador al arbol
    """
    dob = player['dob']
    entry = om.get(map, dob)

    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        lt.addLast(listPlayers, player)
        om.put(map, dob, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map


def updateOverallIndex(map, player):
    """
    CHECKEA que el overall de cada jugador no se repita por club
    y añade cada overall/jugador al arbol
    """
    overall = int(float(player['overall']))
    entry = om.get(map, overall)

    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        lt.addLast(listPlayers, player)
        om.put(map, overall, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map


def updatePotentialIndex(map, player):
    """
    CHECKEA que el potential de cada jugador no se repita por posicion
    y añade cada potential/jugador al arbol
    """
    potential = int(float(player['potential']))
    entry = om.get(map, potential)

    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        lt.addLast(listPlayers, player)
        om.put(map, potential, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map


def updateNumericalIndex(property, map, player):
    """
    CHECKEA que el potential de cada jugador no se repita por posicion
    y añade cada potential/jugador al arbol
    """
    if player[property] == "unknown":
        number = -1
    else:
        number = int(float(player[property]))
    entry = om.get(map, number)

    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareNumbers)
        lt.addLast(listPlayers, player)
        om.put(map, number, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map


def updateRepIndex(analizer, map, player):
    """
    CALCULA, el numero representativo de cada jugador y lo guadra en el arbol
    de la forma numero/jugador
    """
    properties = ["potential", "age", "height_cm", "value_eur"]
    representative = 0
    for prop in properties:
        normal = 0
        if player[prop] != "unknown":
            normal = (int(float(player[prop])) - analizer[prop][0]) / (analizer[prop][1] - analizer[prop][0])
        representative += normal
    entry = om.get(map, representative)
    if entry is None:
        listPlayers = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        lt.addLast(listPlayers, player)
        om.put(map, representative, listPlayers)
    else:
        valor = me.getValue(entry)
        lt.addLast(valor, player)

    return map

# ___________________________________________________
# Funciones de consulta
# ___________________________________________________


def playerSize(analyzer):
    """
    Número de jugadores totales
    """
    return lt.size(analyzer['players'])


def indexHeight(tree):
    """
    Altura del arbol
    """
    return om.height(tree)


def indexSize(tree):
    """
    Numero de elementos en el indice
    """
    return om.size(tree)


def minKey(tree):
    """
    Llave mas pequena
    """
    return om.minKey(tree)


def maxKey(tree):
    """
    Llave mas grande
    """
    return om.maxKey(tree)


def LastPlayers(club, analyzer):
    """
    Devuelve las ultimas 5 adquisiciones mas recientes del club
    """
    if mp.contains(analyzer['clubIndex'], club.lower()):
        playerList = lt.newList('ARRAY_LIST')
        key = mp.get(analyzer['clubIndex'], club.lower())
        tree = me.getValue(key)
        nodos = lt.size(om.keySet(tree))
        pos = 1

        while pos != nodos + 1:

            fecha = om.select(tree, nodos-pos)
            value = om.get(tree, fecha)
            players = me.getValue(value)

            for player in lt.iterator(players):
                if lt.size(playerList) < 5:
                    lt.addLast(playerList, player)

                else:
                    break
            pos += 1

        return playerList

    else:
        return None


def totalPlayers(club, analyzer):
    """
    Retorna la cantidad de jugadores en un club
    """
    if mp.contains(analyzer['clubIndex_num'], club.lower()):
        key = mp.get(analyzer['clubIndex_num'], club.lower())
        value = me.getValue(key)
        return value
    else:
        return None


def posPlayers(info, analyzer):
    """
    Retorna la cantidad de jugadores en una posicion, filtrados
    por "overall", "potential" y "wage_eur"
    """
    if mp.contains(analyzer['posIndex'], info[0].lower()):
        key = mp.get(analyzer['posIndex'], info[0].lower())
        # Value -> Tupla con tres arboles
        value = me.getValue(key)
        overallTree = value[0]
        potentialTree = value[1]
        wageTree = value[2]
        overallList = om.values(overallTree, info[1], info[2])
        potentiaList = om.values(potentialTree, info[3], info[4])
        wageList = om.values(wageTree, info[5], info[6])
        minPlayers = overallList
        sortList = lt.newList("ARRAY_LIST")
        minN = 0
        if lt.size(potentiaList) <= lt.size(minPlayers):
            minPlayers = potentiaList
            minN = 1
        if lt.size(wageList) <= lt.size(minPlayers):
            minPlayers = wageList
            minN = 2
        for playerList in lt.iterator(minPlayers):
            for player in lt.iterator(playerList):
                if minN == 0:
                    if int(player["potential"]) >= info[3] and int(player["potential"]) <= info[4]:
                        if int(player["wage_eur"]) >= info[5] and int(player["wage_eur"]) <= info[6]:
                            lt.addLast(sortList, player)
                elif minN == 1:
                    if int(player["overall"]) >= info[1] and int(player["overall"]) <= info[2]:
                        if int(player["wage_eur"]) >= info[5] and int(player["wage_eur"]) <= info[6]:
                            lt.addLast(sortList, player)
                elif minN == 2:
                    if int(player["potential"]) >= info[3] and int(player["potential"]) <= info[4]:
                        if int(player["overall"]) >= info[1] and int(player["overall"]) <= info[2]:
                            lt.addLast(sortList, player)
        sortByPos(sortList)
        return sortList

    else:
        return None


def tagsAndWage(inferior, superior, tag, analyzer):
    tagsmp = analyzer['tagIndex']
    if mp.contains(tagsmp, tag.lower()):
        playerlist = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        key = mp.get(tagsmp, tag.lower())
        tree = me.getValue(key)
        lista = om.values(tree, inferior, superior)
        for nodo in lt.iterator(lista):
            for player in lt.iterator(nodo):
                lt.addLast(playerlist, player)
        sortByWage(playerlist)
        return playerlist


def Histograma(N, X, property, analyzer):
    tabla = analyzer['propertyIndex']
    treekey = mp.get(tabla, property.lower())
    tree = me.getValue(treekey)

    mayor = om.maxKey(tree)
    menor = om.minKey(tree)
    rango = mayor - menor
    amplitud = round((rango/N), 3)

    indices = lt.newList("ARRAY_LIST")
    indicesbin = lt.newList("ARRAY_LIST")
    indicescount = lt.newList("ARRAY_LIST")
    indiceslvl = lt.newList("ARRAY_LIST")
    indicesmark = lt.newList("ARRAY_LIST")

    suma = menor
    while lt.size(indices) < N-1:
        intervalo = round(suma + amplitud, 3)
        lt.addLast(indices, intervalo)
        suma = intervalo

    lt.addLast(indices, mayor)
    lt.addFirst(indices, menor)

    for i in range(2, lt.size(indices)+1):

        primer = lt.getElement(indices, i-1)
        segundo = lt.getElement(indices, i)
        contador = 0
        if i > 2:
            valores = om.values(tree, (primer+1), segundo)
        else:
            valores = om.values(tree, ceil(primer), segundo)

        for valor in lt.iterator(valores):
            contador += lt.size(valor)

        lt.addLast(indicesbin, f"({primer}-{segundo}]")
        lt.addLast(indicescount, contador)

    for valor in lt.iterator(indicescount):
        lvl = valor//X
        mark = "*"*lvl
        lt.addLast(indiceslvl, lvl)
        lt.addLast(indicesmark, mark)

    return indicesbin, indicescount, indiceslvl, indicesmark, mayor, menor


def playersbyTrait(trait, inferior, superior, analyzer):
    traitsmp = analyzer['traitIndex']
    if mp.contains(traitsmp, trait.lower()):
        playerlist = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
        key = mp.get(traitsmp, trait.lower())
        tree = me.getValue(key)
        lista = om.values(tree, inferior, superior)
        for nodo in lt.iterator(lista):
            sortForDob(nodo)
            for player in lt.iterator(nodo):
                lt.addLast(playerlist, player)
        return playerlist


def playerReplace(name, pos, analyzer):
    namemp = analyzer['nameIndex']
    posmp = analyzer['posIndex']
    if not mp.contains(namemp, name.lower()):
        return None
    key = mp.get(namemp, name.lower())
    player = me.getValue(key)
    key2 = mp.get(posmp, pos.lower())
    repTree = me.getValue(key2)[3]
    # Se normaliza cada propiedad
    properties = ["potential", "age", "height_cm", "value_eur"]
    representative = 0
    for prop in properties:
        minV = analyzer["min-max"][prop][0]
        maxV = analyzer["min-max"][prop][1]
        normal = (int(float(player[prop])) - minV) / (maxV - minV)
        representative += normal
    replaceList = lt.newList("ARRAY_LIST", cmpfunction=compareIds)
    take = om.get(repTree, representative)
    playerList = me.getValue(take)
    for player in lt.iterator(playerList):
        player["repDif"] = 0
        player["rep"] = representative
        lt.addLast(replaceList, player)
    minKey = om.floor(repTree, representative)
    maxKey = om.ceiling(repTree, representative)
    getLimits(repTree, minKey, maxKey, replaceList, representative)

    sortByRep(replaceList)

    return replaceList, representative


def getLimits(tree, minKey, maxKey, list, representative):
    mintake = om.get(tree, minKey)
    minplayerList = me.getValue(mintake)
    maxtake = om.get(tree, maxKey)
    maxlayerList = me.getValue(maxtake)

    for player in lt.iterator(minplayerList):
        repDif = representative - minKey
        if repDif < 0:
            repDif= repDif*-1
        player["repDif"] = repDif
        player["rep"] = minKey
        lt.addLast(list, player)
    for player in lt.iterator(maxlayerList):
        repDif = representative - maxKey
        if repDif < 0:
            repDif= repDif*-1
        player["repDif"] = repDif
        player["rep"] = maxKey
        lt.addLast(list, player)

    if lt.size(list) > 6:
        return
    else:
        minKey = om.floor(tree, minKey)
        maxKey = om.ceiling(tree, maxKey)
        return getLimits(tree, minKey, maxKey, list, representative)

# ___________________________________________________
# Funciones utilizadas para comparar elementos dentro de una lista
# ___________________________________________________


def compareIds(id1, id2):
    """
    Compara dos ids
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareDobs(date1, date2):
    """
    Compara dos dobs
    """
    date1 = dt.strptime(date1, "%Y-%m-%d")
    date2 = dt.strptime(date2, "%Y-%m-%d")
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareNumbers(num1, num2):
    """
    Compara dos fechas
    """
    num1 = int(float(num1))
    num2 = int(float(num2))
    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return 1
    else:
        return -1


def compareByWage(player1, player2):
    p1 = player1
    p2 = player2

    if p1['wage_eur'] > p2['wage_eur']:
        return p1['wage_eur'] > p2['wage_eur']
    elif p1['wage_eur'] == p2['wage_eur']:
        if p1['overall'] > p2['overall']:
            return p1['overall'] > p2['overall']
        elif p1['overall'] == p2['overall']:
            if p1['potential'] > p2['potential']:
                return p1['potential'] > p2['potential']
            elif p1['potential'] == p2['potential']:
                if p1['long_name'] > p2['long_name']:
                    return p1['long_name'] > p2['long_name']


def compareByPos(player1, player2):
    p1 = player1
    p2 = player2

    if p1['overall'] > p2['overall']:
        return p1['overall'] > p2['overall']
    elif p1['overall'] == p2['overall']:
        if p1['potential'] > p2['potential']:
            return p1['potential'] > p2['potential']
        elif p1['potential'] == p2['potential']:
            if p1['wage_eur'] > p2['wage_eur']:
                return p1['wage_eur'] > p2['wage_eur']
            elif p1['wage_eur'] == p2['wage_eur']:
                if p1['age'] > p2['age']:
                    return p1['age'] > p2['age']
                elif p1['age'] == p2['age']:
                    if p1['short_name'] > p2['short_name']:
                        return p1['short_name'] > p2['short_name']


def compareForDob(player1, player2):
    p1 = player1
    p2 = player2

    if p1['overall'] > p2['overall']:
        return p1['overall'] > p2['overall']
    elif p1['overall'] == p2['overall']:
        if p1['potential'] > p2['potential']:
            return p1['potential'] > p2['potential']
        elif p1['potential'] == p2['potential']:
            if p1['long_name'] > p2['long_name']:
                return p1['long_name'] > p2['long_name']


def compareByRep(player1, player2):
    p1 = player1["repDif"]
    p2 = player2["repDif"]

    return p1 > p2


def comparefifaid(player1, player2):
    if player1['sofifa_id'] < player2['sofifa_id']:
        return player1['sofifa_id'] < player2['sofifa_id']
    
# Funciones de ordenamiento


def sortByWage(lista):
    mg.sort(lista, cmpfunction=compareByWage)


def sortByPos(lista):
    mg.sort(lista, cmpfunction=compareByPos)


def sortForDob(lista):
    mg.sort(lista, cmpfunction=compareForDob)


def sortByRep(lista):
    mg.sort(lista, cmpfunction=compareByRep)


def sortById(lista):
    mg.sort(lista, cmpfunction=comparefifaid)
