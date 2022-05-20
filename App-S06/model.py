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

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
assert cf
import time

# -----------------------------------------------------
# NEW ANALYZER
# -----------------------------------------------------

def newAnalyzer():

    analyzer = {
        'players': None,
        'players_ids': None,
        'players_long_name': None,
        'players_short_name': None,
        'clubs': None,
        'players_positions': None,
        'players_tags': None,
        'players_potential': None,
        'players_value': None,
        'overall': None,
        'potential': None,
        'value': None,
        'wage': None,
        'age': None,
        'height': None,
        'weight': None,
        'release_clause': None
                }

    analyzer['players'] = lt.newList('ARRAY_LIST')

    analyzer['players_ids'] = mp.newMap(18000,
                                    maptype='PROBING',
                                    loadfactor=0.5)

    analyzer['players_long_name'] = mp.newMap(18000,
                                    maptype='PROBING',
                                    loadfactor=0.5)

    analyzer['players_short_name'] = mp.newMap(18000,
                                    maptype='PROBING',
                                    loadfactor=0.5)
                                            
    analyzer['clubs'] = om.newMap(omaptype='RBT',
                                comparefunction=cmpTreeElements)

    analyzer['players_positions'] = mp.newMap(40,
                                            maptype='PROBING',
                                            loadfactor=0.5)

    analyzer['players_tags'] = mp.newMap(50,
                                        maptype='PROBING',
                                        loadfactor=0.5)

    analyzer['player_traits'] = mp.newMap(50,
                                        maptype='PROBING',
                                        loadfactor=0.5)

    analyzer['players_potential'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['players_value'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['players_age'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['overall'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)
    
    analyzer['potential'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['value'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['wage'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['age'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['height'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['weight'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    analyzer['release_clause'] = om.newMap(omaptype='RBT',
                                            comparefunction=cmpTreeElements)

    return analyzer

# -----------------------------------------------------
# ADD DATA FUNCTIONS
# -----------------------------------------------------

def addPlayer(analyzer, player):

    player['sofifa_id'] = int(player['sofifa_id'])

    if player['overall'] == '':
        player['overall'] = 0
    else:
        player['overall'] = int(player['overall'])

    if player['potential'] == '':
        player['potential'] = 0
    else:
        player['potential'] = int(player['potential'])

    if player['value_eur'] == '':
        player['value_eur'] = 0
    else:
        player['value_eur'] = float(player['value_eur'])

    if player['wage_eur'] == '':
        player['wage_eur'] = 0
    else:
        player['wage_eur'] = float(player['wage_eur'])

    if player['age'] == '':
        player['age'] = 0
    else:
        player['age'] = int(player['age'])

    if player['height_cm'] == '':
        player['height_cm'] = 0
    else:
        player['height_cm'] = int(player['height_cm'])

    if player['weight_kg'] == '':
        player['weight_kg'] = 0
    else:
        player['weight_kg'] = int(player['weight_kg'])

    if player['release_clause_eur'] == '':
        player['release_clause_eur'] = 0
    else:
        player['release_clause_eur'] = float(player['release_clause_eur'])

    player['player_positions'] = player['player_positions'].split(',')
    player['player_positions'] = list(player['player_positions'])
    for i in range (0, len(player['player_positions'])):
        player['player_positions'][i] = player['player_positions'][i].replace('[', '')
        player['player_positions'][i] = player['player_positions'][i].replace(']', '')
        player['player_positions'][i] = player['player_positions'][i].replace('\'', '')
        player['player_positions'][i] = player['player_positions'][i].replace(' ', '')
        player['player_positions'][i] = player['player_positions'][i].strip()

    if player['player_tags'] == '':
        player['player_tags'] = 'UNKNOWN'
    player['player_tags'] = player['player_tags'].split(',')
    player['player_tags'] = list(player['player_tags'])
    for i in range (0, len(player['player_tags'])):
        player['player_tags'][i] = player['player_tags'][i].replace('[', '')
        player['player_tags'][i] = player['player_tags'][i].replace(']', '')
        player['player_tags'][i] = player['player_tags'][i].replace('\'', '')
        player['player_tags'][i] = player['player_tags'][i].replace(' ', '')
        player['player_tags'][i] = player['player_tags'][i].strip()

    new_player = newPlayer(player['sofifa_id'], player['short_name'], player['long_name'], player['player_positions'], player['overall'], player['potential'], player['value_eur'], player['wage_eur'], player['age'], player['dob'], player['height_cm'], player['weight_kg'], player['club_name'], player['league_name'], player['club_joined'], player['nationality_name'], player['release_clause_eur'], player['player_tags'], player['player_traits'], player['league_level'], player['player_url'], player['club_contract_valid_until'], player['club_position'])

    lt.addLast(analyzer['players'], new_player)
    addSingleTree(analyzer['players_ids'], player['sofifa_id'], new_player)
    addPlayerTree(analyzer['clubs'], new_player, 'club_name')
    addSingleMap(analyzer['players_long_name'], player['long_name'], new_player)
    addSingleMap(analyzer['players_short_name'], player['short_name'], new_player)
    addPlayerListMap(analyzer['players_positions'], new_player, 'player_positions')
    addPlayerListMap(analyzer['players_tags'], new_player, 'player_tags')
    addPlayerTree(analyzer['overall'], new_player, 'overall')
    addPlayerTree(analyzer['potential'], new_player, 'potential')
    addPlayerTree(analyzer['value'], new_player, 'value_eur')
    addPlayerTree(analyzer['wage'], new_player, 'wage_eur')
    addPlayerTree(analyzer['age'], new_player, 'age')
    addPlayerTree(analyzer['height'], new_player, 'height_cm')
    addPlayerTree(analyzer['weight'], new_player, 'weight_kg')
    addPlayerTree(analyzer['release_clause'], new_player, 'release_clause_eur')
    agregar_trait(analyzer, new_player)
    
def agregar_trait(analyzer, player):
    traits = player['player_traits']
    lista_traits = traits.split(',')
    for trait in lista_traits:
        trait = trait.strip()
        exist_property = mp.contains(analyzer['player_traits'], trait)
        if exist_property:
            entry = mp.get(analyzer['player_traits'], trait)
            arbol_jugador = me.getValue(entry)
        else:
            arbol_jugador = om.newMap(omaptype='RBT',
                                        comparefunction=compareDates)
            mp.put(analyzer['player_traits'], trait, arbol_jugador)
        om.put(arbol_jugador, player['dob'], player)

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    newbirth1 = time.strptime(str(date1), "%Y-%m-%d")
    newbirth2 = time.strptime(str(date2), "%Y-%m-%d")

    if (newbirth1 == newbirth2):
        return 0
    elif (newbirth1 > newbirth2):
        return 1
    else:
        return -1

# -----------------------------------------------------
# ADD DATA FUNCTIONS (MAPS)     
# -----------------------------------------------------

def addPlayerMap(map, player, property_name):
    property = player[f'{property_name}']
    exist_property = mp.contains(map, property)
    if exist_property:
        entry = mp.get(map, property)
        property_players = me.getValue(entry)
    else:
        property_players = newProperty(property)
        mp.put(map, property, property_players)
    lt.addLast(property_players['players'], player)

def addSingleMap(map, property, player):
    mp.put(map, property, player)

def addPlayerListMap(map, player, property_name):
    property = player[f'{property_name}']
    for property_index in property:
        exist_property = mp.contains(map, property_index)
        if exist_property:
            entry = mp.get(map, property_index)
            property_players = me.getValue(entry)
        else:
            property_players = newProperty(property_index)
            mp.put(map, property_index, property_players)
        lt.addLast(property_players['players'], player)

# -----------------------------------------------------
# ADD DATA FUNCTION (TREES)
# -----------------------------------------------------

def addPlayerTree(tree, player, property_name):
    property = player[f'{property_name}']
    exist_property = om.contains(tree, property)
    if exist_property:
        entry = om.get(tree, property)
        property_players = me.getValue(entry)
    else:
        property_players = newProperty(property)
        om.put(tree, property, property_players)
    lt.addLast(property_players['players'], player)

def addSingleTree(tree, property, player):
    om.put(tree, property, player)

# -----------------------------------------------------
# CREATE DATA FUNCTIONS
# -----------------------------------------------------

def newPlayer(sofifa_id, short_name, long_name, player_positions, overall, potential, value_eur, wage_eur, age, dob, height_cm, weight_kg, club_name, league_name, club_joined, nationality_name, release_clause_eur, player_tags, player_traits, league_level, player_url, club_contract_valid_until, club_position):

    player = {'sofifa_id': '', 'short_name': '', 'long_name': '', 'player_positions': '', 'overall': '', 'potential': '', 'value_eur': '', 'wage_eur': '', 'age': '', 'dob': '', 'height_cm': '', 'weight_kg': '', 'club_name': '', 'league_name': '', 'club_joined': '', 'nationality_name': '', 'release_clause_eur': '', 'player_tags': '', 'player_traits': '', 'league_level': '', 'player_url': '', 'club_contract_valid_until': '', 'club_position': '', 'potential_rep': '', 'value_rep': '', 'age_rep': '', 'height_rep': '', 'rep_value': '', 'total_rep_value': ''}

    player['sofifa_id'] = sofifa_id
    player['short_name'] = short_name
    player['long_name'] = long_name
    player['player_positions'] = player_positions
    player['overall'] = overall
    player['potential'] = potential
    player['value_eur'] = value_eur
    player['wage_eur'] = wage_eur
    player['age'] = age
    player['dob'] = dob
    player['height_cm'] = height_cm
    player['weight_kg'] = weight_kg
    player['club_name'] = club_name
    player['league_name'] = league_name
    player['club_joined'] = club_joined
    player['nationality_name'] = nationality_name
    player['release_clause_eur'] = release_clause_eur
    player['player_tags'] = player_tags
    player['player_traits'] = player_traits
    player['league_level'] = league_level
    player['player_url'] = player_url
    player['club_contract_valid_until'] = club_contract_valid_until
    player['club_position'] = club_position
    player['potential_rep'] = ''
    player['value_rep'] = ''
    player['age_rep'] = ''
    player['height_rep'] = ''
    player['rep_value'] = ''
    player['total_rep_value'] = ''

    return player

def newProperty(property):
    entry = {f'{property}': '', 'players': None}
    entry[f'{property}'] = property
    entry['players'] = lt.newList('ARRAY_LIST')
    return entry

# -----------------------------------------------------
# GENERIC FUNCTIONS
# -----------------------------------------------------

def sortList(list, cmp_function):
    return merge.sort(list, cmp_function)

def subList(list, pos, len):
    return lt.subList(list, pos, len)

def listSize(list):
    return lt.size(list)

def mapSize(map):
    return mp.size(map)

def treeSize(tree):
    return om.size(tree)

# -----------------------------------------------------
# CMP FUNCTIONS
# -----------------------------------------------------

def cmpTreeElements(element1, element2):
    if element1 == element2:
        return 0
    elif element1 > element2:
        return 1
    else:
        return -1

def cmpPlayersByJoined(player1, player2):
    date_1 = str(player1['club_joined'])
    date_2 = str(player2['club_joined'])
    newdate1 = time.strptime(date_1, "%Y-%m-%d")
    newdate2 = time.strptime(date_2, "%Y-%m-%d")
    newbirth1 = time.strptime(str(player1['dob']), "%Y-%m-%d")
    newbirth2 = time.strptime(str(player2['dob']), "%Y-%m-%d")

    if newdate1 > newdate2:
        return True
    elif newdate1 == newdate2:
        if player1['age'] > player2['age']:
            return True
        elif player1['age'] == player2['age']:
            if newbirth1 > newbirth2:
                return True
            elif newbirth1 == newbirth2:
                if player1['short_name'] > player2['short_name']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def cmpPlayersByOverall(player1, player2):
    if player1['overall'] > player2['overall']:
        return True
    elif player1['overall'] == player2['overall']:
        if player1['potential'] > player2['potential']:
            return True
        elif player1['potential'] == player2['potential']:
            if player1['wage_eur'] > player2['wage_eur']:
                return True
            elif player1['wage_eur'] == player2['wage_eur']:
                if player1['age'] > player2['age']:
                    return True
                elif player1['age'] == player2['age']:
                    if player1['short_name'] > player2['short_name']:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def cmpPlayersByDOB(player1, player2):
    if player1['dob'] > player2['dob']:
        return True
    elif player1['dob'] == player2['dob']:
        if player1['overall'] > player2['overall']:
            return True
        elif player1['overall'] == player2['overall']:
            if player1['potential'] > player2['potential']:
                return True
            elif player1['potential'] == player2['potential']:
                if player1['long_name'] > player2['long_name']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def cmpPlayersByWage(player1, player2):

    if player1['wage_eur'] > player2['wage_eur']:
        return True
    elif player1['wage_eur'] == player2['wage_eur']:
        if player1['overall'] > player2['overall']:
            return True
        elif player1['overall'] == player2['overall']:
            if player1['potential'] > player2['potential']:
                return True
            elif player1['potential'] == player2['potential']:
                if player1['long_name'] > player2['long_name']:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

# -----------------------------------------------------
# REQUIREMENTS FUNCTIONS
# -----------------------------------------------------

def requirement_1(analyzer, club_name):
    # Get players by club
    players = getPlayersTree(analyzer['clubs'], club_name)

    if players != None:
        # Number players in team
        number_players = lt.size(players)

        # Sort players
        sorted_players = sortList(players, cmpPlayersByJoined)

        # League info
        league_name = lt.firstElement(sorted_players)['league_name']
        league_level = lt.firstElement(sorted_players)['league_level']

        if lt.size(sorted_players) >= 5:
            first_five_players = subList(sorted_players, 1, 5)
            return first_five_players, 5, league_level, league_name, number_players
        else:
            return sorted_players, lt.size(sorted_players), league_level, league_name, number_players

    else:
        return None

def requirement_2(analyzer, position, initial_overall, final_overall, initial_potential, final_potential, initial_wage, final_wage):
    # Get players by position
    players_by_position = getPlayersMap(analyzer['players_positions'], position)

    if players_by_position != None:

        # Create tree (players in position by overall)
        position_overall_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
        # Add position players in tree by overall
        for player in lt.iterator(players_by_position):
            addPlayerTree(position_overall_tree, player, 'overall')
            
        # Get players in position by overall
        players_by_position_overall = getIntervalPlayers(position_overall_tree, initial_overall, final_overall)

        if players_by_position_overall != None:

            # Create tree (players in position and overall by potential)
            position_potential_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
            # Add position and overall players in tree by potential
            for intervals in lt.iterator(players_by_position_overall):
                for player in lt.iterator(intervals['players']):
                    addPlayerTree(position_potential_tree, player, 'potential')
            # Get players in position and overall by potential
            players_by_position_potential = getIntervalPlayers(position_potential_tree, initial_potential, final_potential)

            if players_by_position_potential != None:
                # Create tree (players in position, overall and potential by wage)
                position_wage_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
                # Add position, overall and potential players in tree by wage
                for intervals in lt.iterator(players_by_position_potential):
                    for player in lt.iterator(intervals['players']):
                        addPlayerTree(position_wage_tree, player, 'wage_eur')
                # Get players in position, overall and potential by wage
                players_by_position_wage = getIntervalPlayers(position_wage_tree, initial_wage, final_wage)

                if players_by_position_wage != None:
                    # Unify players
                    players = lt.newList('ARRAY_LIST')
                    for intervals in lt.iterator(players_by_position_wage):
                        for player in lt.iterator(intervals['players']):
                            lt.addLast(players, player)

                    # Clean trees
                    position_overall_tree = None
                    position_potential_tree = None
                    position_wage_tree = None

                    return sortList(players, cmpPlayersByOverall)

                else:
                    # Clean trees
                    position_overall_tree = None
                    position_potential_tree = None
                    position_wage_tree = None
                    return None

            else:
                # Clean trees
                position_overall_tree = None
                position_potential_tree = None
                return None

        else:
            # Clean trees
            position_overall_tree = None
            return None

    else:
        return None

def requirement_3(analyzer, tag, initial_wage, final_wage):
    # Get players by tag
    players_by_tag = getPlayersMap(analyzer['players_tags'], tag)

    if players_by_tag != None:

        # Create tree (players in tag by wage)
        tag_wage_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
        # Add tag players in tree by wage
        for player in lt.iterator(players_by_tag):
            addPlayerTree(tag_wage_tree, player, 'wage_eur')

        # Get players in tag by wage
        players_by_tag_wage = getIntervalPlayers(tag_wage_tree, initial_wage, final_wage)

        # Unify players
        players = lt.newList('ARRAY_LIST')
        for intervals in lt.iterator(players_by_tag_wage):
            for player in lt.iterator(intervals['players']):
                if player['value_eur'] == 0:
                    player['value_eur'] = 'UNKNOWN'
                if player['release_clause_eur'] == 0:
                    player['release_clause_eur'] = 'UNKNOWN'
                lt.addLast(players, player)

        # Clean Tree
        tag_wage_tree = None

        return sortList(players, cmpPlayersByWage)

    else:

        return None

def requierement_4(analyzer, trait, initial_dob, final_dob):
    player_traits = analyzer['player_traits']
    arbol_fechas = me.getValue(mp.get(player_traits, trait))
    jugadores = om.values(arbol_fechas, initial_dob, final_dob)

    players = lt.newList('ARRAY_LIST')

    for player in lt.iterator(jugadores):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        lt.addLast(players, player)

    sorted_players = sortList(players, cmpPlayersByDOB)
    
    return sorted_players

def requirement_5(analyzer, number, number_bins):
    # Selection of the property
    
    if number == 1:
        property_tree = analyzer['overall']
    elif number == 2:
        property_tree = analyzer['potential']
    elif number == 3:
        property_tree = analyzer['value_eur']
    elif number == 4:
        property_tree = analyzer['wage_eur']
    elif number == 5:
        property_tree = analyzer['age']
    elif number == 6:
        property_tree = analyzer['height_cm']
    elif number == 7:
        property_tree = analyzer['weight_kg']
    elif number == 8:
        property_tree = analyzer['release_clause_eur']

    # Init counter before data filter
    before_count = 0

    # Count number of players before data filter
    for interval in lt.iterator(om.valueSet(property_tree)):
        before_count += lt.size(interval['players'])

    # Data filter
    property_players = om.contains(property_tree, 0)
    if property_players:
        om.remove(property_tree, 0)

    # Init counter after data filter
    after_count = 0

    # Count number of players after data filter
    for interval in lt.iterator(om.valueSet(property_tree)):
        after_count += lt.size(interval['players'])
    
    # Number of keys
    total_intervals = om.maxKey(property_tree) - om.minKey(property_tree)

    # Increment
    incrase = total_intervals/number_bins
    min_key = om.minKey(property_tree)

    flag = True

    # Put all the intervals in the list
    values = lt.newList('ARRAY_LIST')
    while flag:
        min_key += incrase
        if min_key >= om.maxKey(property_tree):
            flag = False
        else:
            lt.addLast(values, min_key)

    if lt.size(values) >= number_bins:
        lt.removeLast(values)
    lt.addFirst(values, int(om.minKey(property_tree)))
    lt.addLast(values, int(om.maxKey(property_tree)))

    # Makes the interval tuples
    intervals = lt.newList('ARRAY_LIST')
    for pos_1 in range (0, lt.size(values)-1):
        pos_1+=1
        pos_2 = pos_1 + 1

        pos1 = lt.getElement(values, pos_1)
        pos2 = lt.getElement(values, pos_2)
        if type(pos1) is not float or type(pos2) is not float:
            pass
        else:
            if pos1.is_integer() == True:
                pos1 += 0.1
        lt.addLast(intervals, [pos1, pos2])

    # Count the number of players in the interval tuple
    players = lt.newList('ARRAY_LIST')
    interval_list = lt.newList('ARRAY_LIST')
    for pos in lt.iterator(intervals):
        lt.addLast(interval_list, [pos[0], pos[1]])
        interval_players = getIntervalPlayers(property_tree, pos[0], pos[1])
        count = 0
        for players_interval in lt.iterator(interval_players):
            count += lt.size(players_interval['players'])
        interval_value = [pos[0], pos[1], count]
        lt.addLast(players, interval_value)

    # Clean tree
    property_tree = None 

    return players, before_count, after_count
    
def requirement_6(analyzer, player_name, player_position):
    # Get player info
    player_info = getPlayerMap(analyzer['players_short_name'], player_name)
    if player_info == None:
        player_info = getPlayerMap(analyzer['players_long_name'], player_name)
    player_id = player_info['sofifa_id']

    # Get players by position
    players_info = getPlayersMap(analyzer['players_positions'], player_position)
    number_players_position = lt.size(players_info)
    
    # Create tree (players in position(s) by potential)
    potential_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
    # Players by potential
    for player in lt.iterator(players_info):
        addPlayerTree(potential_tree, player, 'potential')
    players_potential = potential_tree
    max_potential = om.maxKey(players_potential)
    min_potential = om.minKey(players_potential)
    # Calculate players representative potential
    for potential_player in lt.iterator(players_info):
        potential_player['potential_rep'] = (potential_player['potential'] - min_potential) / (max_potential - min_potential)
    
    # Create tree (players in position(s) by value)
    value_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
    # Players by value
    for player in lt.iterator(players_info):
        addPlayerTree(value_tree, player, 'value_eur')
    # Data filter
    data_filter = om.contains(value_tree, 0)
    if data_filter:
        om.remove(value_tree, 0)
    players_value = value_tree
    max_value = om.maxKey(players_value)
    min_value = om.minKey(players_value)
    # Calculate players representative value eur
    for value_player in lt.iterator(players_info):
        value_player['value_rep'] = (value_player['value_eur'] - min_value) / (max_value - min_value)

    # Create tree (players in position(s) by age)
    age_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
    # Players by age
    for player in lt.iterator(players_info):
        addPlayerTree(age_tree, player, 'age')
    players_age = age_tree
    max_age = om.maxKey(players_age)
    min_age = om.minKey(players_age)
    # Calculate players representative age
    for age_player in lt.iterator(players_info):
        age_player['age_rep'] = (age_player['age'] - min_age) / (max_age - min_age)

    # Create tree (players in position(s) by height)
    height_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
    # Players by age
    for player in lt.iterator(players_info):
        addPlayerTree(height_tree, player, 'height_cm')
    players_height = height_tree
    max_height = om.maxKey(players_height)
    min_height = om.minKey(players_height)
    # Calculate players representative height
    for height_player in lt.iterator(players_info):
        height_player['height_rep'] = (height_player['height_cm'] - min_height) / (max_height - min_height)
        height_player['rep_value'] = round(height_player['height_rep'] + height_player['age_rep'] + height_player['value_rep'] + height_player['potential_rep'], 4)

    # Players by id
    pos = 0
    for player in lt.iterator(players_info):
        pos += 1
        if player['sofifa_id'] == player_id:
            representative_value = player['rep_value']
            player['rep_value'] = 5
            
    # Create tree (players in by total representative value)
    rep_value_tree = om.newMap(omaptype='RBT', comparefunction=cmpTreeElements)
    for rep_player in lt.iterator(players_info):
        rep_player['total_rep_value'] = abs(rep_player['rep_value'] - representative_value)
        addPlayerTree(rep_value_tree, rep_player, 'total_rep_value')

    replace_players = getPlayersTree(rep_value_tree, om.minKey(rep_value_tree))
    number_replace_players = lt.size(replace_players)

    # Clean trees
    potential_tree = None
    value_tree = None
    age_tree = None
    height_tree = None

    return replace_players, number_players_position, number_replace_players

# -----------------------------------------------------
# GET DATA FUNCTIONS
# -----------------------------------------------------

def getPlayersTree(tree, property):
    if om.contains(tree, property):
        property_players = om.get(tree, property)
        if property_players:
            return me.getValue(property_players)['players']
    else:
        return None

def getPlayerTree(tree, property):
    if om.contains(tree, property):
        property_players = om.get(tree, property)
        if property_players:
            return me.getValue(property_players)
    else:
        return None
    
def getPlayersMap(map, property):
    if mp.contains(map, property):
        property_players = mp.get(map, property)
        if property_players:
            return me.getValue(property_players)['players']
    else:
        return None

def getPlayerMap(map, property):
    if mp.contains(map, property):
        property_players = mp.get(map, property)
        if property_players:
            return me.getValue(property_players)
    else:
        return None

def getIntervalPlayers(tree, initial_interval, final_interval):
    try:
        interval_players = om.values(tree, initial_interval, final_interval)
        return interval_players
    except Exception:
        return None

