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


from numpy import short
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.ADT import orderedmap as om
assert cf
import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los jugadores
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'players': None,
                'clubName': None,
                'player_positions': None,
                'wage_eur': None,
                'dob': None,
                "stats": None, 
                "overall": None,
                "potential":None,
                "value_eur":None,
                "age": None,
                "height_cm":None,
                "weight_kg":None,
                "release_clause_eur":None}

    analyzer['players'] = lt.newList('SINGLE_LINKED')
    analyzer['clubName'] = om.newMap(omaptype='RBT')
    analyzer['player_positions'] = om.newMap(omaptype='RBT')
    analyzer['wage_eur'] = om.newMap(omaptype='RBT')
    analyzer['dob'] = om.newMap(omaptype='RBT')
    analyzer["overall"] = om.newMap(omaptype='RBT')
    analyzer["potential"] = om.newMap(omaptype='RBT')
    analyzer["value_eur"] = om.newMap(omaptype='RBT')
    analyzer["age"] = om.newMap(omaptype='RBT')
    analyzer["height_cm"] = om.newMap(omaptype='RBT')
    analyzer["weight_kg"] = om.newMap(omaptype='RBT')
    analyzer["release_clause_eur"] = om.newMap(omaptype='RBT')
    analyzer["players_name"] = mp.newMap(18077,maptype='PROBING',loadfactor=0.5)

    analyzer['stats']  = mp.newMap(8,maptype='PROBING',loadfactor=0.5)
    mp.put(analyzer['stats'], "min_potential", 101)
    mp.put(analyzer['stats'], "max_potential", -1)
    mp.put(analyzer['stats'], "min_age", 101)
    mp.put(analyzer['stats'], "max_age", -1)
    mp.put(analyzer['stats'], "min_height", 300)
    mp.put(analyzer['stats'], "max_height", -1)
    mp.put(analyzer['stats'], "min_cost", 1e30)
    mp.put(analyzer['stats'], "max_cost", -1)
    return analyzer

# Funciones para agregar informacion al catalogo
def addPlayer(analyzer, player):
    if player["value_eur"]=="":
        player["value_eur"] = 0
    
    if player["player_tags"] == "":
        player["player_tags"]= "Unknown"
     
    if player["player_traits"] == "":
        player["player_traits"] = "Unknown"
       
    lt.addLast(analyzer['players'], player)
    addNamePlayer(analyzer['players_name'], player)
    addClubName(analyzer['clubName'], player)
    addPlayerPosition(analyzer['player_positions'], player)
    updateStats(analyzer, player)
    addSalary(analyzer["wage_eur"], player)
    addDob(analyzer['dob'], player)
    addOverall(analyzer["overall"], player)
    addPotential(analyzer["potential"], player)
    addValue(analyzer["value_eur"], player)
    addAge(analyzer["age"], player)
    addHeight(analyzer["height_cm"], player)
    addWeight(analyzer["weight_kg"], player)
    addReleaseClause(analyzer["release_clause_eur"], player)
    return analyzer

def addNamePlayer(players, player):
    try:
        short_name = player["short_name"]
        existname = mp.contains(players, short_name)
        if existname:
            mapentry = mp.get(players,short_name)
            name_search = me.getValue(mapentry)
        else:
            name_search = lt.newList(datastructure = "ARRAY_LIST")
            mp.put(players, short_name, name_search)
        lt.addLast(name_search, player)
    except Exception:
        return None



def updateStats(analyzer, player):
    age = int(float(player["age"]))
    height =  int(float(player["height_cm"]))
    potential =  int(float(player["potential"]))
    cost =  int(float(player["value_eur"]))

    if me.getValue(mp.get(analyzer["stats"], "min_potential")) > potential:
        mp.put(analyzer['stats'], "min_potential", potential)
    if me.getValue(mp.get(analyzer["stats"], "max_potential")) < potential:
        mp.put(analyzer['stats'], "max_potential", potential)

    if me.getValue(mp.get(analyzer["stats"], "min_age")) > age:             
        mp.put(analyzer['stats'], "min_age", age)
    if me.getValue(mp.get(analyzer["stats"], "max_age")) < age:
        mp.put(analyzer['stats'], "max_age", age)

    if me.getValue(mp.get(analyzer["stats"], "min_height")) > height:
        mp.put(analyzer['stats'], "min_height", height)
    if me.getValue(mp.get(analyzer["stats"], "max_height")) < height:
        mp.put(analyzer['stats'], "max_height", height)

    if me.getValue(mp.get(analyzer["stats"], "min_cost")) > cost:
        mp.put(analyzer['stats'], "min_cost", cost)
    if me.getValue(mp.get(analyzer["stats"], "max_cost")) < cost:
        mp.put(analyzer['stats'], "max_cost", cost)

def addClubName(map, player):
    try:
        club = player["club_name"]
        mapentry = om.get(map, club)    
        if mapentry is None:
            club_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, club, club_search)
        else:
            club_search = me.getValue(mapentry)
        lt.addLast(club_search, player)
    except Exception:
        return None


def addPlayerPosition(map, player):
    try:
        playerPositions = player["player_positions"].split(", ")
        for position in playerPositions:
            mapentry = om.get(map, position)    
            if mapentry is None:
                position_search = lt.newList(datastructure = "ARRAY_LIST")
                om.put(map, position, position_search)
            else:
                position_search = me.getValue(mapentry)
            lt.addLast(position_search, player)
    except Exception:
        return None

def addSalary(map, player):
    try:
        salary = float(player["wage_eur"])
        mapentry = om.get(map, salary)    
        if mapentry is None:
            salary_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, salary, salary_search)
        else:
            salary_search = me.getValue(mapentry)
        lt.addLast(salary_search, player)
    except Exception:
        return None

def addDob(map, player):
    try:
        dob = datetime.datetime.strptime(player["dob"], "%Y-%m-%d")
        player["dob"] = dob
        mapentry = om.get(map, dob)    
        if mapentry is None:
            dob_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, dob, dob_search)
        else:
            dob_search = me.getValue(mapentry)
        lt.addLast(dob_search, player)
    except Exception:
        return None

def addOverall(map, player):
    try:
        overall = float(player["overall"])
        mapentry = om.get(map, overall)    
        if mapentry is None:
            overall_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, overall, overall_search)
        else:
            overall_search = me.getValue(mapentry)
        lt.addLast(overall_search, player)
    except Exception:
        return None

def addPotential(map, player):
    try:
        potential = float(player["potential"])
        mapentry = om.get(map, potential)    
        if mapentry is None:
            potential_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, potential, potential_search)
        else:
            potential_search = me.getValue(mapentry)
        lt.addLast(potential_search, player)
    except Exception:
        return None

def addValue(map, player):
    try:
        value = float(player["value_eur"])
        mapentry = om.get(map, value)    
        if mapentry is None:
            value_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, value, value_search)
        else:
            value_search = me.getValue(mapentry)
        lt.addLast(value_search, player)
    except Exception:
        return None

def addAge(map, player):
    try:
        age = float(player["age"])
        mapentry = om.get(map, age)    
        if mapentry is None:
            age_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, age, age_search)
        else:
            age_search = me.getValue(mapentry)
        lt.addLast(age_search, player)
    except Exception:
        return None

def addWeight(map, player):
    try:
        weight = float(player["weight_kg"])
        mapentry = om.get(map, weight)    
        if mapentry is None:
            weight_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, weight, weight_search)
        else:
            weight_search = me.getValue(mapentry)
        lt.addLast(weight_search, player)
    except Exception:
        return None

def addHeight(map, player):
    try:
        height = float(player["height_cm"])
        mapentry = om.get(map, height)    
        if mapentry is None:
            height_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, height, height_search)
        else:
            height_search = me.getValue(mapentry)
        lt.addLast(height_search, player)
    except Exception:
        return None

def addReleaseClause(map, player):
    try:
        release_clause = float(player["release_clause_eur"])
        mapentry = om.get(map, release_clause)    
        if mapentry is None:
            release_clause_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, release_clause, release_clause_search)
        else:
            release_clause_search = me.getValue(mapentry)
        lt.addLast(release_clause_search, player)
    except Exception:
        return None

# Funciones para creacion de datos

# Funciones de consulta

def playersSize(analyzer):
    """
    Número de jugadores
    """
    return lt.size(analyzer['players'])

def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['clubName'])


def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['clubName'])


def minKey(analyzer, propiedad):
    """
    Llave mas pequena
    """
    return om.minKey(analyzer[propiedad])


def maxKey(analyzer, propiedad):
    """
    Llave mas grande
    """
    return om.maxKey(analyzer[propiedad])

# Requerimiento 1
def getPlayersByClub(analyzer, club):
    map = analyzer["clubName"]
    mapentry = om.get(map, club) 
    if mapentry is not None:
        club_search = me.getValue(mapentry)        
        adquisiciones = lt.size(club_search)
        sorted_list = ms.sort(club_search, compareDates)
        if adquisiciones > 5:
            sub_list = lt.subList(sorted_list, 1, 5)
        else:
            sub_list = sorted_list
        return adquisiciones, sub_list
    else:
        return None

#Requerimiento 2
def getPlayersByPositionInRange(analyzer, position, overall_lo, overall_hi, potential_lo, potential_hi, wage_lo, wage_hi):
    PlayersByPositionInRange = lt.newList(datastructure = "ARRAY_LIST")   
    map = analyzer['player_positions']
    mapentry = om.get(map, position) 
    if mapentry is not None:
        lst_players = me.getValue(mapentry)
        for player in lt.iterator(lst_players):
            if int(float(player["overall"])) >= overall_lo and int(float(player["overall"])) <= overall_hi:
                if int(float(player["potential"])) >= potential_lo and int(float(player["potential"])) <= potential_hi:
                    if int(float(player["wage_eur"])) >= wage_lo and int(float(player["wage_eur"])) <= wage_hi:
                        lt.addLast(PlayersByPositionInRange, player)
    sorted_list = ms.sort(PlayersByPositionInRange, comparePlayersByPositionInRange)
    return sorted_list                

# Requerimiento 3
def getPlayersBySalaryTags(analyzer, salarylo, salaryhi, tag):
    map = analyzer["wage_eur"]
    lst = om.values(map, salarylo, salaryhi)
    playersBySalaryTag = lt.newList(datastructure = "ARRAY_LIST")
    for lst_players in lt.iterator(lst):
        for player in lt.iterator(lst_players):
            if tag in player["player_tags"]:
                lt.addLast(playersBySalaryTag, player)
    sorted_list = ms.sort(playersBySalaryTag, compareSalary)
    return sorted_list

#Requerimiento 4
def getPlayersByDobTraits(analyzer, dob_lo, dob_hi, trait):
    try:
        map = analyzer["dob"]
        dob_lo = datetime.datetime.strptime(dob_lo, "%Y-%m-%d")
        dob_hi = datetime.datetime.strptime(dob_hi, "%Y-%m-%d")
        lst_dob = om.values(map, dob_lo, dob_hi)
        PlayersByDobTraits = lt.newList(datastructure = "ARRAY_LIST")
        for lst_players in lt.iterator(lst_dob):
            for player in lt.iterator(lst_players):
                if trait in player["player_traits"]:
                    lt.addLast(PlayersByDobTraits, player)
        sorted_list = ms.sort(PlayersByDobTraits, compareDatesOfBirth)    
        return sorted_list
    
    except Exception:
        return None

#Requerimiento 5
def getHistogramByProperty(analyzer, N, x, propiedad):
    # Se accede al mapa a partir de la propiedad dada por el usuario
    map = analyzer[propiedad]
    
    # Buscar la llave maxima y minima y su diferencia
    llave_max = om.maxKey(map)
    llave_min = om.minKey(map)
    num_elem = llave_max - llave_min

    # Tamaño de cada rango
    tam = num_elem / N

    # Armar los intervalos y buscar sus valores.
    #intervalos, valores = [], []
    total = 0
    n = 0
    minima = llave_min
    maxima = llave_min + tam
    dic = {}
    while n < N:
        lista = om.values(map, minima, maxima)
        #intervalos.append((minima, maxima))
        count = 0
        #PlayersByProperty = lt.newList(datastructure = "ARRAY_LIST")
        for lst_players in lt.iterator(lista):
            player = lt.getElement(lst_players, 1)
            if minima != player[propiedad]:
                count += lt.size(lst_players)
                total += lt.size(lst_players)

        dic[(minima,maxima)] = {"count": count, "lvl": count//x, "mark": "* "*(count//x)}
        #valores.append(PlayersByProperty)
        minima = maxima 
        maxima += tam
        n += 1
    return dic, total, llave_min, llave_max

#Requerimiento 6 (BONO)
def getPlayersMoreSimilar(analyzer, short_name, position):
    player_goal = getPlayer(analyzer, short_name)
    if player_goal != None:
        vr_goal = getValorRepresentativo(analyzer, player_goal)
        player_goal["vr"] = vr_goal
        map = analyzer['player_positions']
        mapentry = om.get(map, position) 
        if mapentry is not None:
            lst_players = me.getValue(mapentry) #se obtiene la lista de jugadores con es posición
            numberPlayersInPosition  =lt.size(lst_players)
            min_diff = 4.1
            playersMoreSimilar = lt.newList(datastructure = "ARRAY_LIST")
            for player in lt.iterator(lst_players):
                if player["short_name"] != short_name:
                    vr = getValorRepresentativo(analyzer, player)
                    player["vr"] = vr
                    diff = round(abs(vr_goal - vr), 6)
                    if diff <= min_diff:
                        if diff < min_diff:
                            min_diff = diff
                            playersMoreSimilar = lt.newList(datastructure = "ARRAY_LIST")
                        lt.addLast(playersMoreSimilar, player)
        return player_goal, numberPlayersInPosition, playersMoreSimilar 
    return None

def getPlayer(analyzer, short_name):
    entry = mp.get(analyzer["players_name"], short_name)
    if entry is not None:
        name_search = me.getValue(entry)
        i = 1
        print("Se encontraron los siguientes jugadores con el nombre corto {}:".format(short_name))
        for player in lt.iterator(name_search):
            print("{}) {}".format(i, player["long_name"]))
            i += 1
        posicion = int(input("Ingrese el número del jugador que desea consultar: "))
        return lt.getElement(name_search, posicion)
    return None

def getValorRepresentativo(analyzer, player):
    age = int(float(player["age"]))
    height =  int(float(player["height_cm"]))
    potential =  int(float(player["potential"]))
    cost =  int(float(player["value_eur"]))

    vr = 0
    vr += (age-me.getValue(mp.get(analyzer["stats"], "min_age"))) / (me.getValue(mp.get(analyzer["stats"], "max_age")) - me.getValue(mp.get(analyzer["stats"], "min_age")))
    vr += (height-me.getValue(mp.get(analyzer["stats"], "min_height"))) / (me.getValue(mp.get(analyzer["stats"], "max_height")) - me.getValue(mp.get(analyzer["stats"], "min_height")))
    vr += (potential-me.getValue(mp.get(analyzer["stats"], "min_potential"))) / (me.getValue(mp.get(analyzer["stats"], "max_potential")) - me.getValue(mp.get(analyzer["stats"], "min_potential")))
    vr += (cost-me.getValue(mp.get(analyzer["stats"], "min_cost"))) / (me.getValue(mp.get(analyzer["stats"], "max_cost")) - me.getValue(mp.get(analyzer["stats"], "min_cost")))
    return round(vr, 6)


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(player1, player2):
    if player1["club_joined"] > player2["club_joined"]:
        return True
    elif player1["club_joined"] == player2["club_joined"]:
        if int(player1["age"]) < int(player2["age"]):
            return True
        elif int(player1["age"]) == int(player2["age"]):
            if player1["dob"] < player2["dob"]:
                return True
            elif player1["dob"] == player2["dob"]:
                if player1["short_name"].lower() < player2["short_name"].lower():
                    return True
    return False

def comparePlayersByPositionInRange(player1, player2):
    if int(float(player1["overall"])) > int(float(player2["overall"])):
        return True
    elif int(float(player1["overall"])) == int(float(player2["overall"])):
        if int(float(player1["potential"])) > int(float(player2["potential"])):
            return True
        elif int(float(player1["potential"])) == int(float(player2["potential"])):
            if float(player1["wage_eur"]) > float(player2["wage_eur"]):
                return True
            elif float(player1["wage_eur"]) == float(player2["wage_eur"]):
                if int(player1["age"]) < int(player2["age"]):
                    return True
                elif int(player1["age"]) == int(player2["age"]):
                    if player1["short_name"].lower() < player2["short_name"].lower():
                        return True
    return False
                
def compareSalary(player1, player2):
    if float(player1["wage_eur"]) > float(player2["wage_eur"]):
        return True
    elif float(player1["wage_eur"]) == float(player2["wage_eur"]):
        if int(float(player1["overall"])) > int(float(player2["overall"])):
            return True
        elif int(float(player1["overall"])) == int(float(player2["overall"])):
            if int(float(player1["potential"])) > int(float(player2["potential"])):
                return True
            elif int(float(player1["potential"])) == int(float(player2["potential"])):
                if player1["long_name"].lower() < player2["long_name"].lower():
                    return True
    return False

def compareDatesOfBirth(player1, player2):
    """Compara dos fechas"""
    if player1["dob"] >  player2["dob"]:
        return True
    elif player1["dob"] == player2["dob"]:
        if float(player1["overall"]) > float(player2["overall"]):
            return True
        elif float(player1["overall"]) == float(player2["overall"]):
            if float(player1["potential"]) > float(player2["potential"]):
                return True
            elif float(player1["potential"]) == float(player2["potential"]):
                if player1["long_name"].lower() < player2["long_name"].lower():
                    return True
    return False
    


