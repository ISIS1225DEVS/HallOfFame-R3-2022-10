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


from doctest import OutputChecker
from filecmp import cmp
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf
from datetime import datetime as dt



"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
our_prime = 12345678910987654321
our_loadfactor = 0.1

# ___________________________________________________
#  Creacion del catalogo
# ___________________________________________________
def new_catalog():
    catalog = { 
               "players": None,
               'R1_players_by_club': None,
               "R2_position_trees": None,
               'R3_by_tag_wage': None,
               "R4_trait_trees":None,
               "R6_name_hash" : None,
               "R6_min_max_for_PVAH":None,
               "R6_RBT_vr_scores":None
    }

    catalog["players"]    = lt.newList("ARRAY_LIST")
    catalog['R1_by_club'] = mp.newMap(numelements=701,
                                      maptype='PROBING', 
                                      loadfactor=our_loadfactor,
                                      prime=our_prime)

    catalog["R2_position_trees"] = mp.newMap(numelements=20,
                                             maptype='PROBING', 
                                             loadfactor=our_loadfactor,
                                             prime=our_prime,
                                             comparefunction=comparePositions)


    catalog['R3_by_tag_wage'] = mp.newMap(numelements=20,
                                          maptype='PROBING',
                                          loadfactor=our_loadfactor,
                                          prime=our_prime)

    catalog["R4_trait_trees"] = mp.newMap(numelements=30,
                                          maptype='PROBING',
                                          loadfactor=our_loadfactor,
                                          prime=our_prime,
                                          comparefunction= compareTraits)

    catalog['R5_by_overall']   = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_potential'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_value_eur'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_wage_eur'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_age'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_height_cm'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_weight_kg'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)
    catalog['R5_by_release_clause_eur'] = om.newMap(omaptype='RBT',
                                           comparefunction=cmp_r5)                                                                                                                                                      

    catalog["R6_name_hash"] = mp.newMap(numelements=19000,
                                        maptype='PROBING', 
                                        loadfactor=our_loadfactor,
                                        prime=our_prime,
                                        comparefunction= compareNames)

    catalog["R6_min_max_for_PVAH"] = mp.newMap(numelements=19000,
                                               maptype='PROBING',
                                               loadfactor=our_loadfactor,
                                               prime=our_prime,
                                               comparefunction= comparePositions)

    catalog["R6_hash_vr_scores"] = mp.newMap(numelements=21,
                                        maptype='PROBING', 
                                        loadfactor=our_loadfactor,
                                        prime=our_prime,
                                        comparefunction= comparePositions)
    
                                    
    return catalog 



def add_player(catalog, player):
    #Cambios de tipo de datos
    #R1
    player["club_joined"] = str_to_date(player["club_joined"])
    player['age'] = int(float(player['age']))
    player["dob"] = str_to_date(player["dob"])

    #R2
    #Ya se cambia en otros req

    #R3
    player['wage_eur']  = int(float(player['wage_eur']))
    player['overall']   = int(float(player['overall']))
    player['potential'] = int(float(player['potential']))

    #R4
    #Ya se cambia en otros req

    #R5
    if player['value_eur'] == '':
       player['value_eur'] = -1
    else:
        player['value_eur'] = int(float(player['value_eur']))
    player['height_cm'] = int(float(player['height_cm']))
    player['weight_kg'] = int(float(player['weight_kg']))
    if player['release_clause_eur'] == '':
        player['release_clause_eur'] = -1
    else:
        player['release_clause_eur'] = int(float(player['release_clause_eur']))
    
    #R6
    mp.put(catalog["R6_name_hash"], player["short_name"], player)

    #Carga a estructuras de datos para req.
    R1_map_by_club(catalog, player)
    
    R2_RBT_for_pos(catalog,player)

    R3_by_tag_wage(catalog, player)
    
    R4_RBT_for_trait(catalog, player)

    R5_all_histograms(catalog, player)

    R6_min_max_for_PVAH(catalog, player)

    #Agregar a la lista
    lt.addLast(catalog["players"], player)



def str_to_date(string): 
    return dt.strptime(string, "%Y-%m-%d").date()

#------------------------------------------------------------
# Requerimiento 1
#------------------------------------------------------------

def R1_map_by_club(catalog, player):
    club_name = player['club_name']
    
    
    exist_club = mp.get(catalog['R1_by_club'], club_name)
    if (exist_club is None):
        new_om = om.newMap(omaptype='RBT', comparefunction= cmp_r1)
        mp.put(catalog['R1_by_club'], club_name, new_om)
    
    ordered_map = mp.get(catalog['R1_by_club'], club_name)['value']
    llave_compuesta = (player['club_joined'], player['age'], player['dob'], player['short_name'])
    om.put(ordered_map, llave_compuesta, player)



def cmp_r1(p1, p2):
    """
    Compara dos jugadores por los criterios del R1
    """
    x = 1
    #Fecha de unión al club
    if (p1[0] > p2[0]):
        x= -1
    elif (p1[0] < p2[0]):
        x= 1

    elif (p1[0] == p2[0]):
        #Edad
        if(p1[1] > p2[1]):
            x= -1
        
        elif(p1[1] < p2[1]):
            x= 1

        elif(p1[1] == p2[1]):
            #Fecha de nacimiento
            if(p1[2] > p2[2]):
                x= -1

            elif(p1[2] < p2[2]):
                x= 1

            elif(p1[2] == p2[2]):
                #Nombre corto
                if(p1[3] > p2[3]):
                    x= 1
                elif(p1[3] < p2[3]):
                    x= -1
                elif(p1[3] == p2[3]):
                    x= 0
    return x

#------------------------------------------------------------
# Requerimiento 2
#------------------------------------------------------------

def R2_RBT_for_pos(catalog, player):
    pos_list = player["player_positions"].split(",")
    for pos in pos_list:
        pos = pos.strip(" ")
        
        exist_pos = mp.get(catalog["R2_position_trees"], pos)

        if exist_pos is None:
            new_rbt =  om.newMap(omaptype="RBT", comparefunction= cmp_r2)
            mp.put(catalog["R2_position_trees"], pos, new_rbt)

        ordered_map = mp.get(catalog["R2_position_trees"], pos)['value']
        llave_compuesta = (player["overall"], player["potential"], player["wage_eur"], player['age'], player["short_name"])
        om.put(ordered_map, llave_compuesta, player)



def cmp_r2(p1, p2):
    overall_p1, potential_p1, wage_p1, age_p1, S_name_p1  = p1
    overall_p2, potential_p2, wage_p2, age_p2, S_name_p2  = p2

    if overall_p1 > overall_p2:
        return 1
    elif overall_p1 < overall_p2:
        return -1
    elif overall_p1 == overall_p2:
     
        if potential_p1 > potential_p2:
            return 1
        elif potential_p1 < potential_p2:
            return -1
        elif potential_p1 == potential_p2:

            if wage_p1 >  wage_p2:
                return 1
            elif wage_p1 <  wage_p2:
                return -1
            elif wage_p1 ==  wage_p2:
                
                if age_p1 > age_p2:
                    return 1
                elif age_p1 < age_p2:
                    return -1
                elif age_p1 == age_p2:

                    if S_name_p1 > S_name_p2:
                        return 1
                    elif S_name_p1 < S_name_p2:
                        return -1
                    elif S_name_p1 == S_name_p2:
                        return 0

def comparePositions(pos1,pos2):
    pos2 = me.getKey(pos2)
    if (pos1 == pos2):
        return 0
    elif (pos1 > pos2):
        return 1
    else:
        return -1

#------------------------------------------------------------
# Requerimiento 3
#------------------------------------------------------------

def R3_by_tag_wage(catalog, player):
    list_tags = player['player_tags'].split(',')
    for tag in list_tags:

        if tag == '':
            pass
        else:
            tag = tag.strip(' ')
            exist_tag = mp.get(catalog['R3_by_tag_wage'], tag)

            if (exist_tag is None):
                new_om = om.newMap(omaptype='RBT', comparefunction=cmp_r3)
                mp.put(catalog['R3_by_tag_wage'], tag, new_om)
            
            ordered_map = mp.get(catalog['R3_by_tag_wage'], tag)['value']
            #llave con 4 criterios
            llave_compuesta = (player['wage_eur'], player['overall'], player['potential'], player['long_name'])
            om.put(ordered_map, llave_compuesta, player)
            

def cmp_r3(p1, p2):
    x = 1
    #Salario
    if (p1[0] > p2[0]):
        x= -1
    elif (p1[0] < p2[0]):
        x= 1

    elif (p1[0] == p2[0]):
        #Desempeño
        if(p1[1] > p2[1]):
            x= -1
        
        elif(p1[1] < p2[1]):
            x= 1

        elif(p1[1] == p2[1]):
            #potencial
            if(p1[2] > p2[2]):
                x= 1

            elif(p1[2] < p2[2]):
                x= -1

            elif(p1[2] == p2[2]):
                #Nombre completo
                if(p1[3] > p2[3]):
                    x= 1
                elif(p1[3] < p2[3]):
                    x= -1
                elif(p1[3] == p2[3]):
                    x= 0
    return x


#------------------------------------------------------------
# Requerimiento 4
#------------------------------------------------------------
def compareTraits(trait1, trait2):
    trait2 = me.getKey(trait2)
    if (trait1 == trait2):
        return 0
    elif (trait1 > trait2):
        return 1
    else:
        return -1    

def R4_RBT_for_trait(catalog, player):
    if player["player_traits"] == "":
        pass
    else:
        list_traits = player["player_traits"].split(",")
        for trait in list_traits:
            trait = trait.strip(" ")
            
            exist_trait = mp.get(catalog["R4_trait_trees"], trait)

            if exist_trait is None:
                new_rbt =  om.newMap(omaptype="RBT", comparefunction= cmp_r4)
                mp.put(catalog["R4_trait_trees"], trait, new_rbt)
            
            ordered_map = mp.get(catalog["R4_trait_trees"], trait)['value']

            llave = (player["dob"], float(player["overall"]), float(player["potential"]), player["long_name"])
            om.put(ordered_map, llave, player)
                

def cmp_r4(p1, p2):
    dob1, over1, poten1, long1 = p1
    dob2, over2, poten2, long2 = p2

    if dob1 > dob2:
        return 1
    elif dob1 < dob2:
        return -1
    elif dob1 == dob2:

        if over1 > over2:
            return 1
        elif over1 < over2:
            return -1
        elif over1 == over2:

            if poten1 > poten2:
                return 1
            elif poten1 < poten2:
                return -1
            elif poten1 == poten2:

                if long1 > long2:
                    return 1
                elif long1 < long2:
                    return -1
                return 0

#------------------------------------------------------------
# Requerimiento 5
#------------------------------------------------------------

def R5_all_histograms(catalog, player):
    properties = ['overall', 'potential', 'value_eur', 'wage_eur', 'age', 'height_cm', 'weight_kg', 'release_clause_eur']
    for i in range(8):
        prop = properties[i]
        exist_key = om.get(catalog['R5_by_{0}'.format(prop)], player[prop])
        if exist_key is None:
            new_list = lt.newList('ARRAY_LIST')
            om.put(catalog['R5_by_{0}'.format(prop)], player[prop], new_list)
            exist_key = om.get(catalog['R5_by_{0}'.format(prop)], player[prop])
        
        lt.addLast(exist_key['value'], player)


def cmp_r5(p1, p2):
    x = 1
    #potencial
    if (p1 > p2):
        x= 1
    elif (p1 < p2):
        x= -1
    elif (p1 == p2):
        x = 0
    return x


# ___________________________________________________
#  R6
# ___________________________________________________
def compareNames(pos1,pos2):
    pos2 = me.getKey(pos2)
    if (pos1 == pos2):
        return 0
    elif (pos1 > pos2):
        return 1
    else:
        return -1

def comparePositions(pos1, pos2):
    pos2 = me.getKey(pos2)
    if (pos1 == pos2):
        return 0
    elif (pos1 > pos2):
        return 1
    else:
        return -1

def compareVr(pos1, pos2):
    if (pos1 == pos2):
        return 0
    elif (pos1 > pos2):
        return 1
    else:
        return -1

def R6_min_max_for_PVAH (catalog, player):
    positions = player["player_positions"].split(",")
    for position in positions:
        position = position.strip(" ")
        
        exist_pos = mp.get(catalog["R6_min_max_for_PVAH"], position)

        if exist_pos == None:
            mp.put(catalog["R6_min_max_for_PVAH"], position, lt.newList("ARRAY_LIST"))
        
        list_pos = mp.get(catalog["R6_min_max_for_PVAH"], position)["value"]

        if lt.isEmpty(list_pos):
            lt.addLast(list_pos, float(player["potential"])) #valor min potential 1
            lt.addLast(list_pos, float(player["potential"])) #valor max potential 2
            lt.addLast(list_pos, float(player["value_eur"])) #valor min value 3
            lt.addLast(list_pos, float(player["value_eur"])) #valor max value 4
            lt.addLast(list_pos, float(player["age"])) #valor min age 5
            lt.addLast(list_pos, float(player["age"])) #valor max age 6
            lt.addLast(list_pos, float(player["height_cm"])) #valor min height 7
            lt.addLast(list_pos, float(player["height_cm"])) #valor max height 8

        else:
            if float(player["potential"]) < lt.getElement(list_pos, 1):
                lt.changeInfo(list_pos, 1, float(player["potential"]))

            if float(player["potential"]) > lt.getElement(list_pos, 2):
                lt.changeInfo(list_pos, 2, float(player["potential"]))

            if float(player["value_eur"]) < lt.getElement(list_pos, 3):
                lt.changeInfo(list_pos, 3, float(player["value_eur"]))

            if float(player["value_eur"]) > lt.getElement(list_pos, 4):
                lt.changeInfo(list_pos, 4, float(player["value_eur"]))

            if float(player["age"]) < lt.getElement(list_pos, 5):
                lt.changeInfo(list_pos, 5, float(player["age"]))

            if float(player["age"]) > lt.getElement(list_pos, 6):
                lt.changeInfo(list_pos, 6, float(player["age"]))

            if float(player["height_cm"]) < lt.getElement(list_pos, 7):
                lt.changeInfo(list_pos, 7, float(player["height_cm"]))

            if float(player["height_cm"]) > lt.getElement(list_pos, 8):
                lt.changeInfo(list_pos, 8, float(player["height_cm"]))


def calc_vr(player, catalog):
    min_max_hash = catalog["R6_min_max_for_PVAH"]
    
    positions = player["player_positions"].split(",")
    for pos in positions:
        pos = pos.strip(" ")
        
        if  om.size(om.get(catalog["R2_position_trees"],pos)["value"]) > 1:

            min_max_of_pos = mp.get(min_max_hash,pos)["value"]

            min_P_pos =  lt.getElement(min_max_of_pos,1)
            max_P_pos =  lt.getElement(min_max_of_pos,2)
            min_V_pos =  lt.getElement(min_max_of_pos,3)
            max_V_pos =  lt.getElement(min_max_of_pos,4)
            min_A_pos =  lt.getElement(min_max_of_pos,5)
            max_A_pos =  lt.getElement(min_max_of_pos,6)
            min_H_pos =  lt.getElement(min_max_of_pos,7)
            max_H_pos =  lt.getElement(min_max_of_pos,8)

        
            vr_P = (float(player["potential"]) - min_P_pos) / (max_P_pos - min_P_pos)
            vr_V = (float(player["value_eur"]) - min_V_pos) / (max_V_pos - min_V_pos)
            vr_A = (float(player["age"]) - min_A_pos) / (max_A_pos - min_A_pos)
            vr_H = (float(player["height_cm"]) - min_H_pos) / (max_H_pos - min_H_pos)
            
            vr_score_in_pos = round(vr_P + vr_V + vr_A + vr_H, 5)

            exist_pos = mp.get(catalog["R6_hash_vr_scores"], pos)
            
            if exist_pos is None:
                new_rbt =  om.newMap(omaptype="RBT", comparefunction= compareVr)
                mp.put(catalog["R6_hash_vr_scores"], pos, new_rbt)

            ordered_map = mp.get(catalog["R6_hash_vr_scores"], pos)['value']

            exist_score = om.get(ordered_map, vr_score_in_pos)

            if exist_score is None:
                new_list = lt.newList("ARRAY_LIST")
                om.put(ordered_map, vr_score_in_pos, new_list)
            
            score_list = om.get(ordered_map, vr_score_in_pos)["value"]

            lt.addLast(score_list, player)

def vr_for_name(player, pos, catalog):
    min_max_hash = catalog["R6_min_max_for_PVAH"]
    if  om.size(om.get(catalog["R2_position_trees"],pos)["value"]) > 1:

        min_max_of_pos = mp.get(min_max_hash,pos)["value"]

        min_P_pos =  lt.getElement(min_max_of_pos,1)
        max_P_pos =  lt.getElement(min_max_of_pos,2)
        min_V_pos =  lt.getElement(min_max_of_pos,3)
        max_V_pos =  lt.getElement(min_max_of_pos,4)
        min_A_pos =  lt.getElement(min_max_of_pos,5)
        max_A_pos =  lt.getElement(min_max_of_pos,6)
        min_H_pos =  lt.getElement(min_max_of_pos,7)
        max_H_pos =  lt.getElement(min_max_of_pos,8)


        vr_P = (float(player["potential"]) - min_P_pos) / (max_P_pos - min_P_pos)
        vr_V = (float(player["value_eur"]) - min_V_pos) / (max_V_pos - min_V_pos)
        vr_A = (float(player["age"]) - min_A_pos) / (max_A_pos - min_A_pos)
        vr_H = (float(player["height_cm"]) - min_H_pos) / (max_H_pos - min_H_pos)
        
        vr_score_in_pos = round(vr_P + vr_V + vr_A + vr_H, 5)
        
        return vr_score_in_pos
    else:
        return None
                
#============================================================
# Ejecución de cada requerimiento
#============================================================

#------------------------R1----------------------------------
def r1_answer(catalog, inp_club_name):

    exist_club = mp.get(catalog['R1_by_club'], inp_club_name)  #O(1)
    #Contención de error
    if (exist_club is None):
        return None, None, None, None, None, None
    
    ordered_map = exist_club['value']                          #O(1)
    n_adquisitions = om.size(ordered_map)                      #O(1)
    
    player_list = tomar_5_ultimos(ordered_map, n_adquisitions) #O(log(n))
    player_x = lt.getElement(player_list, 1)                   #O(1)
    league_name = player_x['league_name']                      #O(1)
    league_level = player_x['league_level']                    #O(1)

    #Lab9
    height = indexHeight(ordered_map)                          #O(1)
    n_elements = indexSize(ordered_map)                        #O(1)

    

    return n_adquisitions, player_list, league_name, league_level, height, n_elements

def tomar_5_ultimos(ordered_map, tam):

    if tam < 5:
        rta = lt.newList('ARRAY_LIST')
        for i in range(tam):

            key = om.select(ordered_map, i)
            value = om.get(ordered_map, key)['value']
            lt.addLast(rta, value)
    else:
        rta = lt.newList('ARRAY_LIST')
        for i in range(5):

            key = om.select(ordered_map, i)
            value = om.get(ordered_map, key)['value']
            lt.addLast(rta, value)
            
    return rta


#------------------------R2----------------------------------

def R2_answer(catalog, pos_player, min_overall, max_overall, min_potential, max_potential, min_wage, max_wage):
    exist_map = mp.get(catalog["R2_position_trees"],pos_player)

    if exist_map == None:
        return None, None
    
    RBT = exist_map["value"]

    low_key = (min_overall, min_potential,  min_wage,  0,"")
    high_key = ( max_overall,  max_potential, max_wage, 200,"zzzzzzzzzzzzzzzz")
    
    keys_in_range = om.keys(RBT,low_key, high_key)
    keys_in_range = correct_range(keys_in_range, min_potential, max_potential, min_wage, max_wage)

    list_jugadores_keys = lt.newList("ARRAY_LIST")

    num_jugadores = lt.size(keys_in_range)

    for i in range(1,7):
        if i < 4:
            jugador = lt.getElement(keys_in_range, i)
            lt.addFirst(list_jugadores_keys, jugador) 
        else:
            jugador = lt.getElement(keys_in_range, num_jugadores - (6-i))
            lt.addFirst(list_jugadores_keys, jugador)

    list_jugadores = lt.newList("ARRAY_LIST")
    
    for key in lt.iterator(list_jugadores_keys):
        jugador = om.get(RBT, key)["value"]
        lt.addLast(list_jugadores, jugador)

    return list_jugadores, num_jugadores


def correct_range(keys, min_potential, max_potential, min_wage, max_wage):
    
    list_good_elems = lt.newList("ARRAY_LIST")
    for key in lt.iterator(keys):
        overall, potential,  wage,  age, name = key

        if potential in range(min_potential, max_potential+1):
            if wage in range(min_wage, max_wage+1):
                lt.addLast(list_good_elems, key)

    return list_good_elems 
    


#------------------------R3----------------------------------
def r3_answer(catalog, in_wage_lo, in_wage_hi, in_tag):
    exist_tag = mp.get(catalog['R3_by_tag_wage'], in_tag)   #O(1)
    #Contención error
    if exist_tag is None:
        return None, None
    
    ordered_map = exist_tag['value']                    #O(1)
    
    rta_list = lt.newList('ARRAY_LIST')                 #O(1)

    low_key = (in_wage_hi, 99999999999, 9999999999, "zzzzzzzzzzzzzzzz")  #O(1)
    high_key = (in_wage_lo, 0, 0, '')                   #O(1)

    keys_in_range = om.keys(ordered_map, low_key, high_key) #O(altura + numelementos)
    #out
    n_elements = lt.size(keys_in_range)  #O(1)
    
    rta_list = get3first_3last(keys_in_range, ordered_map)  #O(1)
    
    return n_elements, rta_list 

#------------------------R4----------------------------------

def R4_answer(catalog, trait, min_dob, max_dob):

    min_dob = str_to_date(min_dob)
    max_dob = str_to_date(max_dob)

    exists_trait = mp.get(catalog["R4_trait_trees"], trait)

    if exists_trait is None:
        return None, None
    
    trait_RBT = exists_trait["value"]

    keylo = (min_dob,0, 0, "")
    keyhi = (max_dob, 0, 0, "" )

    keys_in_range = om.keys(trait_RBT, keylo, keyhi)
    
    list_jugadores = lt.newList("ARRAY_LIST")
    
    for key in lt.iterator(keys_in_range):
        jugador = om.get(trait_RBT, key)["value"]
        lt.addLast(list_jugadores, jugador)

    resp_list = lt.newList("ARRAY_LIST")
    num_jugadores = lt.size(list_jugadores)
    for i in range(1,7):
        if i < 4:
            jugador = lt.getElement(list_jugadores, i)
            lt.addFirst(resp_list, jugador)
        else:
            jugador = lt.getElement(list_jugadores, num_jugadores - (6-i))
            lt.addFirst(resp_list, jugador)
    
    return resp_list, num_jugadores
   



def order_players(player1, player2):
    if player1["dob"] < player2["dob"]:
        return True
    elif player1["dob"] > player2["dob"]:
        return False
    if player1["dob"] == player2["dob"]:

        if player1["overall"] < player2["overall"]:
            return True
        elif player1["overall"] > player2["overall"]:
            return False
        elif player1["overall"] == player2["overall"]:

            if player1["potential"] < player2["potential"]:
                return True
            elif player1["potential"] > player2["potential"]:
                return False
            elif player1["potential"] == player2["potential"]:

                if player1["long_name"] < player2["long_name"]:
                    return True
                elif player1["long_name"] > player2["long_name"]:
                    return False
                return True

#------------------------R5----------------------------------

def r5_answer(catalog, in_bins, in_scale, prop):


    ordered_map = catalog['R5_by_{0}'.format(prop)] #O(1)

    #Para todos los players con un valor no vacío
    keys = om.keys(ordered_map, 0, 9999999999999999) #O(altura + num(elements))
    contador = 0
    for key in lt.iterator(keys):                       #O(numelements)
        lista_key = om.get(ordered_map, key)['value']
        contador += lt.size(lista_key)
    n_consulted = contador

    llave_max = om.maxKey(ordered_map)                  #O(altura)
    #Estas dos propiedades tienen vacíos y los vacíos están agrupados en la llave -1,
    #Por lo que se toma la siguiente llave después de -1 (el mínimo verdadero)
    if prop in ['value_eur','release_clause_eur']:
        llave_min = om.select(ordered_map, 1)
    else:
        llave_min = om.minKey(ordered_map)

    #Creación de los intervalos
    rango = llave_max - llave_min                       #O(1)
    longitud_intervalo = rango/in_bins                  #O(1)
    
    #Output
    ranks    = lt.newList('ARRAY_LIST')                 #O(1)
    total_elements = lt.newList('ARRAY_LIST')           #O(1)
    height = lt.newList('ARRAY_LIST')                   #O(1)

    inicio = llave_min                                  #O(1)
    #Para cada caja de intervalo...
    for i in range(in_bins):                            #O(numelements)
        intervalo_i_lo = inicio
        intervalo_i_hi = round(inicio + longitud_intervalo, 3)

        if i == (in_bins-1):
            # 93.9999... -> 94
            intervalo_i_hi = int(round(intervalo_i_hi, 1))
        

        if i == 0:
            #Añadir el rango
            string = '['+str(intervalo_i_lo)+', '+str(intervalo_i_hi)+']'
            lt.addLast(ranks, string)
            #llaves que aplican
            keys = om.keys(ordered_map, intervalo_i_lo, intervalo_i_hi)



        else:
            #Añadir el rango
            string = '('+str(intervalo_i_lo)+', '+str(intervalo_i_hi)+']'
            lt.addLast(ranks, string)

            #Llaves que aplican
            keys_not_fixed = om.keys(ordered_map, intervalo_i_lo, intervalo_i_hi)
            
            exist_key = om.get(ordered_map, intervalo_i_lo)
            if exist_key is None:
                keys = keys_not_fixed
            else:
                tam_full = lt.size(keys_not_fixed)
                keys = lt.subList(keys_not_fixed, 2, tam_full-1)
            

        #Contar elementos dentro del rango de llaves
        contador = 0
        for key in lt.iterator(keys):
            lista_key = om.get(ordered_map, key)['value']
            contador += lt.size(lista_key)
        lt.addLast(total_elements, contador)
        lt.addLast(height, contador//in_scale)

        
        
        #Iniciar desde i_hi la siguiente iteración
        inicio = intervalo_i_hi


    n_used = 0
    for i in lt.iterator(total_elements):  #O(bins)
        n_used += i



    return n_consulted, n_used, llave_min, llave_max, ranks, total_elements, height

#------------------------R6----------------------------------

def R6_answer(jugador, pos, catalog):
    tam_jugadores_in_pos = om.size(om.get(catalog["R2_position_trees"],pos)["value"])  
    vr_of_player = vr_for_name(jugador, pos, catalog)
    if vr_of_player == None:
        return None, None

    exist_pos = mp.get(catalog["R6_hash_vr_scores"], pos)
    if exist_pos is None:
        return None, None
    
    vr_RBT_of_pos = exist_pos["value"]
    exist_list = om.get(vr_RBT_of_pos, vr_of_player)
    if exist_list is None:
        return None, None
    
    vr_list = exist_list["value"]
    if lt.size(vr_list) <= 1:
        var_para_volver_a_meter = om.get(vr_RBT_of_pos, vr_of_player)["value"]
        om.remove(vr_RBT_of_pos, vr_of_player)
        floor_key = om.floor(vr_RBT_of_pos, vr_of_player)
        ceiling_key = om.ceiling(vr_RBT_of_pos, vr_of_player)
        om.put(vr_RBT_of_pos,vr_of_player, var_para_volver_a_meter)
        sustitucion = None
        if floor_key == None:
            sustitucion = om.get(vr_RBT_of_pos, ceiling_key)["value"]
        elif ceiling_key == None:
            sustitucion = om.get(vr_RBT_of_pos, floor_key)["value"]
        else:
            if abs(floor_key - vr_of_player) > abs(ceiling_key - vr_of_player):
                sustitucion = om.get(vr_RBT_of_pos, floor_key)["value"]
            else:
                sustitucion = om.get(vr_RBT_of_pos, ceiling_key)["value"]
        return sustitucion, tam_jugadores_in_pos
    else:
        list_jugadores_validos = lt.newList("ARRAY_LIST")
        for persona in lt.iterator(vr_list):
            if persona != jugador:
                lt.addLast(list_jugadores_validos, persona)
        return list_jugadores_validos, tam_jugadores_in_pos



#----------------------------------
# Funciones generales
#----------------------------------

def get3first_3last(keys_in_range, ordered_map):
    """ Esta función parte de un TAD lista con
    las llaves de interés (e.g. resultado de keys()), toma las 3 primeras y últimas
    busca estas 6 llaves en _ordered_map_ y retorna un TAD lista con los jugadores en sí """

    tam = lt.size(keys_in_range)
    rta_list = lt.newList('ARRAY_LIST')

    if lt.isEmpty(keys_in_range):
        rta_list = None
    elif tam == 0:
        rta_list = None
    elif tam < 7:
        for key in lt.iterator(keys_in_range):
            player = om.get(ordered_map, key)['value']
            lt.addLast(rta_list, player)
    elif tam >=7:
        for i in range(6):
            pos = [1,2,3, tam-2, tam-1, tam]
            key = lt.getElement(keys_in_range, pos[i])
            player = om.get(ordered_map, key)['value']
            lt.addLast(rta_list, player)
            
    return rta_list

def indexHeight(analyzer):
    """
    Altura del árbol
    """
    return om.height(analyzer)


def indexSize(analyzer):
    """
    Número de elementos en el indice
    """
    return om.size(analyzer)
        
