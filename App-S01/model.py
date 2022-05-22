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


from email.policy import default
import config as cf
from copy import deepcopy
from typing import Any
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as megsort
import datetime
assert cf

# !!! Valor estándar para separate chaining
LOADFACTOR_LIMIT = 4.0

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

INF = int(1e10)

EMPTY_VALUE = {
    'int': -1,
    'str': 'Unknown',
    'float': -1.0,
    'bool': None,
    'set': {'Unknown'}
}

EMPTY_MAX_PLAYER = {
    'sofifa_id': '999999',
    'player_url': None,
    'short_name': 'ZZZZZZ',
    'long_name': 'ZZZZZZ',
    'player_positions': None,
    'overall': INF,
    'potential': INF,
    'value_eur': float(INF),
    'wage_eur': float(INF),
    'age': 100,
    'dob': 9999-99-99,
    'height_cm': INF,
    'weight_kg': INF,
    'club_joined': 9999-99-99,
    'international_reputation': INF,
    'release_clause_eur': float(INF)
}

EMPTY_MIN_PLAYER = {
    'sofifa_id': '000000',
    'player_url': None,
    'short_name': 'AAAAAA',
    'long_name': 'AAAAAA',
    'player_positions': None,
    'overall': -INF,
    'potential': -INF,
    'value_eur': float(-INF),
    'wage_eur': float(-INF),
    'age': -INF,
    'dob': 0000-00-00,
    'height_cm': -INF,
    'weight_kg': -INF,
    'club_joined': 0000-00-00,
    'international_reputation': -INF,
    'release_clause_eur': float(-INF)
}


def cmpPlayersByID(a: dict, b: dict)->int:
    if (a["sofifa_id"] < b["sofifa_id"]): return -1
    elif (a["sofifa_id"] == b["sofifa_id"]): return 0
    else: return 1


# Opción 0 - Carga de datos
def newCatalog()->Any:
    """
    Crea el catálogo para todos los TAD lista, mapa y set que se va a utilizar

    Returns:
        Any: retorna el catalogo
    """
    catalog = {
        "players": None,
        "ids": None,
        "club_name_players": None,
        "players_wages": None
    }

    catalog["players"] = lt.newList('ARRAY_LIST', cmpfunction=cmpPlayersByID)
    catalog["clubs"] = lt.newList('ARRAY_LIST')

    #TODO: Definir el tamaño óptimo de los mapas
    # Req. 1
    catalog["club_name_players"] = mp.newMap(5000, maptype="CHAINING", loadfactor=LOADFACTOR_LIMIT)
    # Req. 2
    catalog["pos_overall"] = mp.newMap(100, maptype="CHAINING", loadfactor=LOADFACTOR_LIMIT)
    catalog["pos_potential"] = mp.newMap(100, maptype="CHAINING", loadfactor=LOADFACTOR_LIMIT)
    catalog["pos_wage"] = mp.newMap(100, maptype="CHAINING", loadfactor=LOADFACTOR_LIMIT)

    # Req. 3
    catalog["players_wages"] = om.newMap(omaptype='RBT', comparefunction=cmpReq3)
    # Req. 4
    # Req. 5 - se hace directamente desde la carga porque cada función de comparación es distinta
    # Req. 6
    catalog['short_player'] = mp.newMap(50000, maptype="CHAINING", loadfactor=LOADFACTOR_LIMIT)
    catalog['positions_players'] = mp.newMap(50000, maptype="CHAINING", loadfactor=LOADFACTOR_LIMIT)
    return catalog


def addPlayer(catalog: Any, p: Any):
    """
    Añade el jugador a la lista principal del catálogo y a la lista de IDs
    Se revisan las llaves individualmente para hacer el typecast

    Args:
        catalog (Any): modelo del control
        p (Any): jugador a añadir
    """
    p_keys = list(p)
    to_int_conversion = {"overall", "potential", "age",
    "height_cm", "weight_kg", "league_level", "club_jersey_number",
    "nationality_id", "nation_team_id", "nation_jersey_number", "weak_foot", "international_reputation"}
    to_float_conversion = {"value_eur", "wage_eur", "release_clause_eur"}
    to_set_conversion_comma = {"player_tags", "player_traits", "player_positions"}
    to_set_conversion_slash = {"work_rate"}
    to_string = {"club_name"}
    fixed_p = {}

    # TODO: Checkear que exista el valor. Puede ser NONE
    for key in p_keys:
        if (key in to_int_conversion):
            if (p[key] == ''):
                fixed_p[key] = EMPTY_VALUE['int']
            else:
                fixed_p[key] = int(float(p[key]))

        elif (key in to_float_conversion):
            if (p[key] == ''):
                fixed_p[key] = EMPTY_VALUE['float']
            elif (p[key].lower() == 'no'):
                fixed_p[key] = 0.0
            else:
                fixed_p[key] = float(p[key])

        elif (key in to_set_conversion_comma):
            if (p[key] == ''):
                fixed_p[key] = EMPTY_VALUE['set']
            else:
                fixed_p[key] = set(p[key].split(", "))
        elif (key in to_set_conversion_slash):
            if (p[key] == ''):
                fixed_p[key] = EMPTY_VALUE['set']
            else:
                fixed_p[key] = set(p[key].split("/"))
        elif (key in to_string):
            if (p[key] == ''):
                fixed_p[key] = EMPTY_VALUE['string']
            else:
                fixed_p[key] = p[key].strip()

        else:
            if (p[key] == ''):
                fixed_p[key] = EMPTY_VALUE['str']
            else:
                fixed_p[key] = p[key]

    # se añade al catalogo
    lt.addLast(catalog["players"], fixed_p)

    return


def createMaps(catalog: Any):
    """
    Crea los mapas necesarios para los requerimientos

    Args:
        catalog (Any): datos del modelo
    """
    # sofifa_id -> players
    createMapIDPlayers(catalog)
    
    # Req. 1  Keys (clubs) -> values (RBT con players de cada club)
    map_ClubName_RBTplayers(catalog)
    # Req. 2
    createSetStats(catalog)
    # Req. 3
    tags_wages(catalog)
    # Req. 4
    createMapPTraits(catalog)
    # Req. 5
    properties = ['overall', 'potential', 'value_eur', 'wage_eur', 'age',
    'height_cm', 'weight_kg', 'release_clause_eur']
    # Req. 6
    createMapPositions(catalog)
    createRBTvs(catalog)

    # guarda los mínimos y máximos
    for prop in properties:
        createMinMax(catalog, prop)

    # se crean los sets correspondientes
    for prop in properties:
        createSetProp(catalog, prop)
    
    return 

def createSetStats(catalog: Any):
    """
    Crea un 'set' de los jugadores con respecto a sus stats de overall, potential, wage_eur

    Args:
        catalog (Any): datos del modelo
    """

    for p in lt.iterator(catalog["players"]):
        # todas las posiciones del jugador
        for pos in p["player_positions"]:
            # overall
            if (not mp.contains(catalog["pos_overall"], pos)):
                mp.put(catalog["pos_overall"], pos, om.newMap("RBT", cmpReq2Overall))

            posov = me.getValue(mp.get(catalog["pos_overall"], pos))

            # potential
            if (not mp.contains(catalog["pos_potential"], pos)):
                mp.put(catalog["pos_potential"], pos, om.newMap("RBT", cmpReq2Potential))

            pospot = me.getValue(mp.get(catalog["pos_potential"], pos))

            # wage
            if (not mp.contains(catalog["pos_wage"], pos)):
                mp.put(catalog["pos_wage"], pos, om.newMap("RBT", cmpReq2Wage))

            poswage = me.getValue(mp.get(catalog["pos_wage"], pos))

            # añadimos al jugador a los distintos mapas
            om.put(posov, p, None)
            om.put(pospot, p, None)
            om.put(poswage, p, None)

    return 




def createMinMax(catalog: Any, prop: str):
    """
    Consigue los valores mínimos y máximos para la propiedad prop

    Args:
        catalog (Any): datos del modelo
        prop (str): propiedad a evaluar
    """
    min_val = deepcopy(EMPTY_MAX_PLAYER[prop])
    max_val = deepcopy(EMPTY_MIN_PLAYER[prop])

    for p in lt.iterator(catalog["players"]):
        if (p[prop] < min_val): min_val = p[prop]
        if (p[prop] > max_val): max_val = p[prop]

    # se añaden al catálogo
    minmax_name = "minmax_" + prop
    catalog[minmax_name] = {"min" : min_val, "max" : max_val}

    return



def createSetProp(catalog: Any, prop: str):
    """
    Crea un set (mapa con llaves y valroes None)

    Args:
        catalog (Any): datos del modelo
        prop (str): propiedad con la que se quiere crear el mapa
    """
    map_name = "map_" + prop

    # mapa se crea aquí por el comparador especial
    catalog[map_name] = om.newMap('RBT', simpleCmpF[prop])

    currom = catalog[map_name]

    # llenamos el mapa
    for p in lt.iterator(catalog["players"]):
        om.put(currom, p, True)



def createMapIDPlayers(catalog: Any):
    """
    Llena el mapa id_players que relaciona el sofifa_id con los diccionarios de los jugadores

    Args:
        catalog (Any): datos del modelo
    """
    sz = lt.size(catalog["players"])
    catalog["id_players"] = mp.newMap(3*sz, maptype="CHAINING", loadfactor=1.0)

    # guarda a cada jugador por su ID
    for p in lt.iterator(catalog["players"]):
        mp.put(catalog["id_players"], p["sofifa_id"], p)

    return


# Opción 1 - Reportar las cinco adquisiciones más recientes de un club

def map_ClubName_RBTplayers(catalog):
    """
    Se decidió un mapa con llave club y valor un RBT
    de jugadores ordenados por lo que solicitan. 
    """
    map = catalog["club_name_players"]

    # saca los clubes
    for jugador in lt.iterator(catalog["players"]):
        club = jugador["club_name"]
        if (not mp.contains(map, club)):
            mp.put(map, club, om.newMap(omaptype='RBT', comparefunction=compareDates))
            
        # debe existir el RBT
        tree = me.getValue(mp.get(map, club))
        if (not om.contains(tree, jugador)):
            om.put(tree, jugador, 0)     
    return

def getRecentAdquisitions(catalog, club)->Any:
    """
    Retorna la lista con los jugadores que pertenecen al equipo
    Args:
        catalog (Any): control["model"]
        club (str): club de futbol a buscar

    Returns:
        Any: RBT con los jugadores ordenados
    """

    retorno = None

    if (mp.contains(catalog["club_name_players"], club)):
        RBT = me.getValue(mp.get(catalog["club_name_players"], club))

        retorno = RBT
    
    return retorno


# Opción 2 - Reportar los jugadores de cierta posición dentro de un rango de de desempeño, potencial y salario
def getPlayersPos(catalog: Any, pos: str, low_ov: int, up_ov: int, low_pot: int, up_pot: int, low_sal: int, up_sal: int)->Any:
    """
    Encuentra los jugadores de una cierta posición en un rango de desempeño, potencial y salario

    Args:
        catalog (Any): datos del modelo
        pos (str): posición del jugador
        low_ov (int): cota inferior del overall
        up_ov (int): cota superior del overall
        low_pot (int): cota inferior del potential
        up_pot (int): cota superior del potential
        low_sal (int): cota inferior del salario
        up_sal (int): cota superior del salario

    Returns:
        Any: TAD lista con los jugadores
    """
    # Conseguimos cada uno de los sets correspondientes a la posición deseada
    posov = me.getValue(mp.get(catalog["pos_overall"], pos))
    pospot = me.getValue(mp.get(catalog["pos_potential"], pos))
    poswage = me.getValue(mp.get(catalog["pos_wage"], pos))

    # Conseguimos el rango para overall
    low_p_ov = deepcopy(EMPTY_MIN_PLAYER)
    low_p_ov["overall"] = low_ov
    up_p_ov = deepcopy(EMPTY_MAX_PLAYER)
    up_p_ov["overall"] = up_ov
    players_ov = om.keys(posov, low_p_ov, up_p_ov)

    # Conseguimos el rango para potential
    low_p_pot = deepcopy(EMPTY_MIN_PLAYER)
    low_p_pot["potential"] = low_pot
    up_p_pot = deepcopy(EMPTY_MAX_PLAYER)
    up_p_pot["potential"] = up_pot
    players_pot = om.keys(pospot, low_p_pot, up_p_pot)

    # Conseguimos el rango para wage
    low_p_wage = deepcopy(EMPTY_MIN_PLAYER)
    low_p_wage["wage_eur"] = low_sal
    up_p_wage = deepcopy(EMPTY_MAX_PLAYER)
    up_p_wage["wage_eur"] = up_sal
    players_wage = om.keys(poswage, low_p_wage, up_p_wage)

    # sacamos a los jugadores que tienen las tres características
    sz = lt.size(catalog["players"])
    idx = mp.newMap(sz, maptype='CHAINING')
    cnt = mp.newMap(sz, maptype='CHAINING')
    res = om.newMap("RBT", cmpReq2Selected)

    # Contamos jugadores del overall
    for p in lt.iterator(players_ov):
        if (not mp.contains(cnt, p["sofifa_id"])):
            mp.put(cnt, p["sofifa_id"], 0)
            mp.put(idx, p["sofifa_id"], p)

        player_count = me.getValue(mp.get(cnt, p["sofifa_id"]))
        mp.put(cnt, p["sofifa_id"], player_count+1)

    # Contamos jugadores del potential
    for p in lt.iterator(players_pot):
        if (not mp.contains(cnt, p["sofifa_id"])):
            mp.put(cnt, p["sofifa_id"], 0)
            mp.put(idx, p["sofifa_id"], p)

        player_count = me.getValue(mp.get(cnt, p["sofifa_id"]))
        mp.put(cnt, p["sofifa_id"], player_count+1)

    # Contamos jugadores del wage
    for p in lt.iterator(players_wage):
        if (not mp.contains(cnt, p["sofifa_id"])):
            mp.put(cnt, p["sofifa_id"], 0)
            mp.put(idx, p["sofifa_id"], p)

        player_count = me.getValue(mp.get(cnt, p["sofifa_id"]))
        mp.put(cnt, p["sofifa_id"], player_count+1)

    for pid in lt.iterator(mp.keySet(cnt)):
        if (me.getValue(mp.get(cnt, pid)) == 3):
            p = me.getValue(mp.get(idx, pid))
            om.put(res, p, None)
    

    # Usando el RBT ya ordenado, sacamos a los jugadores y los ponemos en un TAD lista
    res_lista = lt.newList()

    for p in lt.iterator(om.keySet(res)):
        lt.addLast(res_lista, p)

    return res_lista
    

# Opción 3 - Reportar los jugadores dentro de un rango salarial y con cierta etiqueta

def tags_wages(catalog):
    """
    Se decidió crear un mapa de players tags con llave tag y valor un RBT con llave jugador y valor salario. 
    """
    RBT = catalog["players_wages"]

    # saca los tags
    for jugador in lt.iterator(catalog["players"]):
        if (not om.contains(RBT, jugador)):
            om.put(RBT, jugador, None)              
    return

def getWages(catalog, lim_inf, lim_sup, tag)->Any:
    """
    Retorna la lista con los jugadores que cumplen lo necesario y su número
    Args:
        catalog (Any): control["model"]
        lim_inf (float): límite inferior de salario
        lim_sup (float): límite superior de salario

    Returns:
        Any: RBT con los jugadores ordenados
    """
    RBT = catalog['players_wages']
    
    # Código para poder comparar llaves que son jugadores
    min = deepcopy(EMPTY_MIN_PLAYER)
    min['wage_eur'] = lim_inf
    max = deepcopy(EMPTY_MAX_PLAYER)
    max['wage_eur'] = lim_sup

    keylo = om.ceiling(RBT, min)
    keyhi = om.floor(RBT, max)

    lista = om.keys(RBT, keylo, keyhi)
    retorno = lt.newList(datastructure='ARRAY_LIST')
    for jugador in lt.iterator(lista):
        if tag in jugador['player_tags']:
            lt.addLast(retorno, jugador)

    num_jugadores = lt.size(retorno)
    
    return retorno, num_jugadores

# Opción 4 - Jugadores con una característica en un rango de tiempo de nacimiento
def createMapPTraits(catalog: Any):
    """
    Crea y llena el mapa con llaves las características de un jugador y valores un set de ids de jugadores que tengan esa característica

    Args:
        catalog (Any): datos del modelo
    """
    sz = lt.size(catalog["players"])
    catalog["p_traits"] = mp.newMap(2*sz, maptype="CHAINING", loadfactor=3.0) # TODO: ¿Qué tamaño debería tener?
    p_traits = catalog["p_traits"]

    for p in lt.iterator(catalog["players"]):
        traits = p["player_traits"]
        for t in traits:
            # revisamos si ya existe la llave
            if (not mp.contains(p_traits, t)):
                mp.put(p_traits, t, om.newMap("RBT", cmpReq4))

            # recuperamos el 'set'
            asoc_rbt = me.getValue(mp.get(p_traits, t))
            # se inserta al set
            om.put(asoc_rbt, p, None)
            
    return


def getPTraitsRangeDates(catalog: Any, low_dob: str, up_dob: str, tra: str)->Any:
    """
    Busca a los jugadores con tra nacidos entre low_dob y up_dob.
    Complejidad: depende de la implementación interna de om.keys() (lg N vs N)

    Args:
        catalog (Any): datos del modelo
        low_dob (str): fecha de nacimiento de inicio
        up_dob (str): fecha de nacimiento de fin
        tra (str): cualidad de player_traits

    Returns:
        Any: TAD lista con los jugadores buscados
    """
    pls_trait = me.getValue(mp.get(catalog["p_traits"], tra))

    # Copiamos los valores vacíos para usar de llaves en el mapa
    low_p = deepcopy(EMPTY_MIN_PLAYER)
    low_p['dob'] = low_dob
    up_p = deepcopy(EMPTY_MAX_PLAYER)
    up_p['dob'] = up_dob

    keylo = om.ceiling(pls_trait, low_p)
    keyhi = om.floor(pls_trait, up_p)
    
    return om.keys(pls_trait, keylo, keyhi)


# Opción 5
def getHistogram(catalog: Any, prop: str, bins: int, scale: int)->Any:
    """
    Genera la tabla del histograma con llaves (a,b) (correspondientes al rango (a, b]))

    Args:
        catalog (Any): datos del modelo
        prop (str): propiedad a revisar
        bins (int): número de buckets para dividir
        scale (int): escala del histograma

    Returns:
        Any: TAD lista de tuplas con cuatro elementos (low, up, freq, stars)
    """
    lb, ub = getExtremes(catalog, prop)

    bucket_size = (ub-lb)/bins
    low_val = lb
    up_val = lb + bucket_size
    map_name = "map_" + prop

    tabla = lt.newList("SINGLE_LINKED")

    for i in range(bins):
        # Copiamos los valores vacíos para usar de llaves en el mapa
        low_p = deepcopy(EMPTY_MIN_PLAYER)
        low_p[prop] = low_val
        up_p = deepcopy(EMPTY_MAX_PLAYER)
        up_p[prop] = up_val

        # hacemos la query para el rango
        players = om.keys(catalog[map_name], low_p, up_p)
        freq = lt.size(players)
        stars = freq//scale

        res = (low_val, up_val, freq, stars)
        lt.addLast(tabla, res)

        low_val = up_val+0.001
        up_val += bucket_size
    
    return tabla

# Opción 6

def createMapPositions(catalog):
    map = catalog['positions_players']
    for player in lt.iterator(catalog['players']):
        # Recorrer posiciones
        for position in player['player_positions']:
            if (not mp.contains(map, position)):
                mp.put(map, position, lt.newList(datastructure='ARRAY_LIST'))
            lista = me.getValue(mp.get(map, position))
            lt.addLast(lista, player)

    return

def createRBTvs(catalog):
    mapa_positions = catalog['positions_players']
    positions = mp.keySet(mapa_positions)

    # Crear el nuevo atributo para cada jugador

    for position in lt.iterator(positions):
        lista_jugadores = me.getValue(mp.get(mapa_positions, position))
        min_potencial = 101
        max_potencial = -1
        min_edad = 100
        max_edad = 0
        min_heigth = 300
        max_height = 0
        min_value = 1e11
        max_value = -1

        for jugador in lt.iterator(lista_jugadores):
            edad = jugador['age']
            potencial = jugador['potential']
            valor = jugador['value_eur']
            altura = jugador['height_cm']

            if edad > max_edad:
                max_edad = edad
            if edad < min_edad:
                min_edad = edad
            if altura > max_height:
                max_height = altura
            if altura < min_heigth:
                min_heigth = altura
            if potencial > max_potencial:
                max_potencial = potencial
            if potencial < min_potencial:
                min_potencial = potencial
            if valor > max_value:
                max_value = valor
            if valor < min_value:
                min_value = valor
        
         # Creación del RBT

        catalog['RBT_VR'+position] = om.newMap(omaptype='RBT', comparefunction=cmpReq6)
        RBT = catalog['RBT_VR'+position]
        # Sacar el V_R para cada jugador y agregarle su atributo | Añadirlo al RBT

        for jugador in lt.iterator(lista_jugadores):
            edad = jugador['age']
            potencial = jugador['potential']
            valor = jugador['value_eur']
            altura = jugador['height_cm']
            
            if (max_edad - min_edad) == 0:
                vn_edad = 1
            else:
                vn_edad = (edad - min_edad)/(max_edad - min_edad)

            if (max_potencial - min_potencial) == 0:
                vn_potencial = 1
            else:
                vn_potencial = (potencial - min_potencial)/(max_potencial - min_potencial)
            
            if (max_value - min_value) == 0:
                vn_value = 1
            else:
                vn_value = (valor - min_value)/(max_value - min_value)

            if (max_height - min_heigth) == 0:
                vn_altura = 1
            else:
                vn_altura = (altura - min_heigth)/(max_height - min_heigth)

            VR = vn_altura + vn_edad + vn_potencial + vn_value
            jugador['VR'] = VR
            
            if not(om.contains(RBT, jugador)):
               om.put(RBT, jugador, None)
            
            # Creación del mapa short_name -> jugador con el atributo VR incluido. No se puede hacer aparte por eso mismo.
            if (not mp.contains(catalog["short_player"], jugador['short_name'])):
                mp.put(catalog["short_player"], jugador['short_name'], jugador)
    return     


def getSustitutions(catalog, short_name, position):
    jugador = me.getValue(mp.get(catalog['short_player'], short_name))
    arbol = catalog['RBT_VR' + position]
    num = lt.size(om.valueSet(arbol))
    VR_jugador = me.getKey(om.get(arbol, jugador))['VR']

    retorno = lt.newList(datastructure='ARRAY_LIST')
    siguiente = om.ceiling(arbol, jugador)
    anterior = om.floor(arbol, jugador)
    # Por default, tiene que regresar que es más cercano. Este será el de arriba o abajo.
    dif_arriba = abs(VR_jugador - siguiente['VR'])
    dif_abajo = abs(VR_jugador - anterior['VR'])

    if dif_arriba > dif_abajo:
        lt.addLast(retorno, anterior)
    else:
        lt.addLast(retorno, siguiente)
    
    default = lt.getElement(retorno, 1)
    iguales = True
    entradas = 0
    
    
    while (iguales or entradas < 2000):
        # Condición para añadirlo a la lista
        if (siguiente['VR'] == default['VR'] and siguiente != default):
            lt.addLast(retorno, siguiente)
        if (anterior['VR'] == default['VR'] and anterior != default):
            lt.addLast(retorno, anterior)
        
        # Condición para parar
        if (siguiente['VR'] != default['VR']) and (anterior['VR'] != default['VR']):
            iguales = False

        # Actualización para siguiente iteración
        siguiente = om.ceiling(arbol, siguiente)
        anterior = om.floor(arbol, anterior)
        entradas += 1
    
    return retorno, num




def getExtremes(catalog: Any, prop: str)->tuple:
    """
    Retorna tupla con el (menor, mayor) elementos con la propiedad prop

    Args:
        catalog (Any): datos del modelo
        prop (str): propiedad a revisar

    Returns:
        tuple: (menor, mayor)
    """
    minmax_name = "minmax_" + prop
    min_val = catalog[minmax_name]["min"]
    max_val = catalog[minmax_name]["max"]

    return min_val, max_val


def sortPlayers(catalog: Any)->Any:
    """
    Ordena la TAD lista "players" de acuerdo a su comparador (por ID)

    Args:
        catalog (Any): datos del modelo
    Returns:
        Any: players ordenados
    """
    megsort.sort(catalog["players"], catalog["players"]["cmpfunction"])
    return catalog["players"]


# Funciones de comparación
def cmpOverall(a: dict, b: dict)->int:
    if (a["overall"] < b["overall"]): return -1
    elif (a["overall"] == b["overall"]): return 0
    else: return 1

def cmpPotential(a: dict, b: dict)->int:
    if (a["potential"] < b["potential"]): return -1
    elif (a["potential"] == b["potential"]): return 0
    else: return 1


def cmpLongNames(a: dict, b: dict)->int:
    if (a["long_name"] < b["long_name"]): return -1
    elif (a["long_name"] == b["long_name"]): return 0
    else: return 1

def cmpShortNames(a: dict, b: dict)->int:
    if (a["short_name"] < b["short_name"]): return -1
    elif (a["short_name"] == b["short_name"]): return 0
    else: return 1


def cmpBirth(a: dict, b: dict)->int:
    if (a["dob"] < b["dob"]): return -1
    elif (a["dob"] == b["dob"]): return 0
    else: return 1

def cmpReq2Overall(a: dict, b: dict)->int:
    res = cmpOverall(a, b)
    if (res != 0): return res
    res = cmpPlayersByID(a, b)
    return res

def cmpReq2Potential(a: dict, b: dict)->int:
    res = cmpPotential(a, b)
    if (res != 0): return res
    res = cmpPlayersByID(a, b)
    return res

def cmpReq2Wage(a: dict, b: dict)->int:
    res = cmpWageEur(a, b)
    if (res != 0): return res
    res = cmpPlayersByID(a, b)
    return res

def cmpReq2Selected(a: dict, b: dict)->int:
    res = cmpOverall(a, b)
    if (res != 0): return res
    res = cmpPotential(a, b)
    if (res != 0): return res
    res = cmpWageEur(a, b)
    if (res != 0): return res
    res = cmpAge(a, b)
    if (res != 0): return res
    res = cmpShortNames(a, b)
    return res

def cmpReq4(a: Any, b: Any)->int:
    res = cmpBirth(a, b)
    if (res != 0): return res
    res = cmpOverall(a, b)
    if (res != 0): return res
    res = cmpPotential(a, b)
    if (res != 0): return res
    res = cmpLongNames(a, b)
    return res

def cmpReq5Overall(a: Any, b: Any)->int:
    res = cmpOverall(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5Potential(a: Any, b: Any)->int:
    res = cmpPotential(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5ValEur(a: Any, b: Any)->int:
    res = cmpValEur(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5WageEur(a: Any, b: Any)->int:
    res = cmpWageEur(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5Age(a: Any, b: Any)->int:
    res = cmpAge(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5Height(a: Any, b: Any)->int:
    res = cmpHeight(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5Weight(a: Any, b: Any)->int:
    res = cmpWeight(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res

def cmpReq5ReleaseClause(a: Any, b: Any)->int:
    res = cmpReleaseClause(a,b)
    if (res != 0): return res
    res = cmpPlayersByID(a,b)
    return res


# TODO: convertir retorno a int
def compareDates(player1, player2):
    """
    compara entre los jugadores por:
    1) club_joined
    2) age
    3) dob
    4) short_name

    Args:
        player1 (): primer jugador
        player2 (): segundo jugador

    Returns:
        int: resultado de la comparación
    """
    club_joined1 = datetime.datetime.strptime(player1['club_joined'], '%Y-%m-%d')
    club_joined2 = datetime.datetime.strptime(player2['club_joined'], '%Y-%m-%d')

    dob1 = datetime.datetime.strptime(player1['dob'], '%Y-%m-%d')
    dob2 = datetime.datetime.strptime(player2['dob'], '%Y-%m-%d')

    if (club_joined1 != club_joined2):
        retorno =club_joined1 > club_joined2

    elif (player1["age"] != player1["age"]):
        retorno = player1["age"] > player2["age"]

    elif (dob1 != dob2):
        retorno = dob1 > dob2

    else:
        retorno = player1["short_name"] > player2["short_name"]
    
    if retorno:
        retorno = -1
    else:
        retorno = 1
    return retorno 

def cmpReq3(player1, player2):
    """
    compara entre los jugadores por:
    1) wage_eur
    2) overall
    3) potential
    4) long_name

    Args:
        player1 (): primer jugador
        player2 (): segundo jugador

    Returns:
        int: resultado de la comparación
    """

    if (player1["wage_eur"] != player2["wage_eur"]):
        retorno = player1["wage_eur"] > player2["wage_eur"]

    elif (player1["overall"] != player1["overall"]):
        retorno = player1["overall"] < player2["overall"]

    elif (player1["potential"] != player1["potential"]):
        retorno = player1["potential"] > player2["potential"]

    elif player1["long_name"] != player2["long_name"]:
        retorno = player1["long_name"] > player2["long_name"]
    else:
        return 0
    
    if retorno:
        retorno = 1
    else:
        retorno = -1
    return retorno 

def cmpReq6(player1, player2):
    if player1['VR'] != player2['VR']:
        retorno = player1['VR'] > player2['VR']
    else:
        return 0

    if retorno:
        retorno = 1
    else:
        retorno = -1
    return retorno



def cmpValEur(a: Any, b: Any)->int:
    if (a["value_eur"] < b["value_eur"]): return -1
    elif (a["value_eur"] == b["value_eur"]): return 0
    else: return 1

def cmpWageEur(a: Any, b: Any)->int:
    if (a["wage_eur"] < b["wage_eur"]): return -1
    elif (a["wage_eur"] == b["wage_eur"]): return 0
    else: return 1

def cmpAge(a: Any, b: Any)->int:
    if (a["age"] < b["age"]): return -1
    elif (a["age"] == b["age"]): return 0
    else: return 1

def cmpHeight(a: Any, b: Any)->int:
    if (a["height_cm"] < b["height_cm"]): return -1
    elif (a["height_cm"] == b["height_cm"]): return 0
    else: return 1

def cmpWeight(a: Any, b: Any)->int:
    if (a["weight_kg"] < b["weight_kg"]): return -1
    elif (a["weight_kg"] == b["weight_kg"]): return 0
    else: return 1

def cmpReleaseClause(a: Any, b: Any)->int:
    if (a["release_clause_eur"] < b["release_clause_eur"]): return -1
    elif (a["release_clause_eur"] == b["release_clause_eur"]): return 0
    else: return 1

# Índice de comparadores
simpleCmpF = {
    'overall': cmpReq5Overall,
    'potential': cmpReq5Potential,
    'value_eur': cmpReq5ValEur,
    'wage_eur': cmpReq5WageEur,
    'age': cmpReq5Age,
    'height_cm': cmpReq5Height,
    'weight_kg': cmpReq5Weight,
    'release_clause_eur': cmpReq5ReleaseClause
}

