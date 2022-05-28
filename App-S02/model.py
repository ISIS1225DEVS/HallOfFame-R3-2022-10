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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mgs
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'players': None}
    analyzer['players'] = lt.newList('ARRAY_LIST')
    analyzer['playersByClubName'] = mp.newMap(numelements = 200, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByTraits'] = mp.newMap(numelements = 50, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByTags'] = mp.newMap(numelements = 7, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByTagsLt'] = mp.newMap(numelements = 7, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByPosition'] = mp.newMap(numelements = 20, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByOverall'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByPotential'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByValue_eur'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByWage_eur'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByAge'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByHeight_cm'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByWeight_kg'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersByRelease_clause_eur'] = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
    analyzer['playersBySName'] = mp.newMap(numelements = 18100, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersByPositionVr'] = mp.newMap(numelements = 20 , maptype = 'PROBING', loadfactor = 0.5)
    analyzer['playersPropertiesMinMax'] = mp.newMap(numelements = 20, maptype = 'PROBING', loadfactor = 0.5)
    analyzer['totalPlayersWOUnknown'] = mp.newMap(numelements = 30, maptype = 'PROBING', loadfactor = 0.5)
    return analyzer

# Funciones para agregar informacion al catalogo

def addPlayer(analyzer, player):
    player['dob'] = stringToDateFormat(player['dob'])
    player['club_joined'] = stringToDateFormat(player['club_joined'])
    player['club_contract_valid_until'] = int(float(player['club_contract_valid_until']))
    player['player_tags'] = player['player_tags'].split(',')
    player['player_traits'] = player['player_traits'].split(',')
    player['wage_eur'] = int(float(player['wage_eur']))
    player['age'] = int(float(player['age']))
    player['overall'] = int(player['overall'])
    player['potential'] = int(player['potential'])
    if player['value_eur'] == '':
        player['value_eur'] = -1
    else:
        player['value_eur'] = int(float(player['value_eur']))
    if player['release_clause_eur'] == '':
        player['release_clause_eur'] = -1
    else:
        player['release_clause_eur'] = int(float(player['release_clause_eur']))
    player['player_positions'] = player['player_positions'].split(',')
    for characteristic in player:
        if player[characteristic] == '':
            player[characteristic] = 'Unknown'
    lt.addLast(analyzer['players'], player)
    addPlayerByClub(analyzer, player['club_name'], player)
    addPlayerByTrait(analyzer, player)
    addPlayerByTag(analyzer, player)
    addPlayerByPosition(analyzer, player)
    addPlayerByKey(analyzer, analyzer['playersByOverall'], player, 'overall')
    addPlayerByKey(analyzer, analyzer['playersByPotential'], player, 'potential')
    addPlayerByKey(analyzer, analyzer['playersByValue_eur'], player, 'value_eur')
    addPlayerByKey(analyzer, analyzer['playersByWage_eur'], player, 'wage_eur')
    addPlayerByKey(analyzer, analyzer['playersByAge'], player, 'age')
    addPlayerByKey(analyzer, analyzer['playersByHeight_cm'], player, 'height_cm')
    addPlayerByKey(analyzer, analyzer['playersByWeight_kg'], player, 'weight_kg')
    addPlayerByKey(analyzer, analyzer['playersByRelease_clause_eur'], player, 'release_clause_eur')
    addPlayerByPositionForVr(analyzer, player)
    return analyzer

def addPlayerForVrTree(analyzer):
    for player in lt.iterator(analyzer['players']):
        addPlayersVr(analyzer, player)
        addPlayerBySName(analyzer, player)

def addPlayerByKey(analyzer, fifaTree, player, key):
    if player[key] != 'Unknown' or player[key] > 0:
        player[key] = int(float(player[key]))
        if mp.contains(analyzer['totalPlayersWOUnknown'], key):
            count = me.getValue(mp.get(analyzer['totalPlayersWOUnknown'], key)) + 1
            mp.put(analyzer['totalPlayersWOUnknown'], key, count)
        else:
            mp.put(analyzer['totalPlayersWOUnknown'], key, 1)

        if om.contains(fifaTree, player[key]):
            players = me.getValue(om.get(fifaTree, player[key]))
            lt.addLast(players, player)
        else:
            players = lt.newList('ARRAY_LIST')
            lt.addLast(players, player)
            om.put(fifaTree, player[key], players)

def addPlayerByKeyFloat(fifaTree, player, key):
    if player[key] != 'Unknown' or player[key] > 0:
        player[key] = float(player[key])
        if om.contains(fifaTree, player[key]):
            players = me.getValue(om.get(fifaTree, player[key]))
            lt.addLast(players, player)
        else:
            players = lt.newList('ARRAY_LIST')
            lt.addLast(players, player)
            om.put(fifaTree, player[key], players)

def addPlayerByClub(analyzer, clubName, player):
    if mp.contains(analyzer['playersByClubName'], clubName):
        treeByJoin = me.getValue(mp.get(analyzer['playersByClubName'], clubName))
        if om.contains(treeByJoin, player['club_joined']):
            treeByAge = me.getValue(om.get(treeByJoin, player['club_joined']))
            if om.contains(treeByAge, player['age']):
                treeByDob = me.getValue(om.get(treeByAge, player['age']))
                if om.contains(treeByDob, player['dob']):
                    playersBySName = me.getValue(om.get(treeByDob, player['dob']))
                    om.put(playersBySName, player['short_name'], player)
                else:
                    playersBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    om.put(playersBySName, player['short_name'], player)
                    om.put(treeByDob, player['dob'], playersBySName)
            else:
                treeByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                playersBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                om.put(playersBySName, player['short_name'], player)
                om.put(treeByDob, player['dob'], playersBySName)
                om.put(treeByAge, player['age'], treeByDob)
        else:
            treeByAge = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            treeByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playersBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            om.put(playersBySName, player['short_name'], player)
            om.put(treeByDob, player['dob'], playersBySName)
            om.put(treeByAge, player['age'], treeByDob)
            om.put(treeByJoin, player['club_joined'], treeByAge)
    else:
        treeByJoin = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMaxToMin)
        treeByAge = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
        treeByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
        playersBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
        om.put(playersBySName, player['short_name'], player)
        om.put(treeByDob, player['dob'], playersBySName)
        om.put(treeByAge, player['age'], treeByDob)
        om.put(treeByJoin, player['club_joined'], treeByAge)
        mp.put(analyzer['playersByClubName'], clubName, treeByJoin)

def addPlayerByTrait(analyzer, player):
    for trait in player['player_traits']:
        trait = trait.strip()
        if mp.contains(analyzer['playersByTraits'], trait):
            treesByDob = me.getValue(mp.get(analyzer['playersByTraits'], trait))
            if om.contains(treesByDob, player['dob']):
                treesByOverall = me.getValue(om.get(treesByDob, player['dob']))
                if om.contains(treesByOverall, player['overall']):
                    treesByPotential = me.getValue(om.get(treesByOverall, player['overall']))
                    if om.contains(treesByPotential, player['potential']):
                        playersByLongname = me.getValue(om.get(treesByPotential, player['potential']))
                        om.put(playersByLongname, player['long_name'], player)
                    else:
                        playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                        om.put(playersByLongname, player['long_name'], player)
                        om.put(treesByPotential, player['potential'], playersByLongname)
                else:
                    treesByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    om.put(playersByLongname, player['long_name'], player)
                    om.put(treesByPotential, player['potential'], playersByLongname)
                    om.put(treesByOverall, player['overall'], treesByPotential)
            else:
                treesByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                treesByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                om.put(playersByLongname, player['long_name'], player)
                om.put(treesByPotential, player['potential'], playersByLongname)
                om.put(treesByOverall, player['overall'], treesByPotential)
                om.put(treesByDob, player['dob'], treesByOverall)
        else:
            treesByDob = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            treesByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            treesByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playersByLongname = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            om.put(playersByLongname, player['long_name'], player)
            om.put(treesByPotential, player['potential'], playersByLongname)
            om.put(treesByOverall, player['overall'], treesByPotential)
            om.put(treesByDob, player['dob'], treesByOverall)
            mp.put(analyzer['playersByTraits'], trait, treesByDob)

def addPlayerByPosition(analyzer, player):
    for playerPosition in player['player_positions']:
        playerPosition = playerPosition.strip()

        if mp.contains(analyzer['totalPlayersWOUnknown'], playerPosition):
            count = me.getValue(mp.get(analyzer['totalPlayersWOUnknown'], playerPosition)) + 1
            mp.put(analyzer['totalPlayersWOUnknown'], playerPosition, count)
        else:
            mp.put(analyzer['totalPlayersWOUnknown'], playerPosition, 1)

        if mp.contains(analyzer['playersByPosition'], playerPosition):
            treeByOverall = me.getValue(mp.get(analyzer['playersByPosition'], playerPosition))
            if om.contains(treeByOverall, player['overall']):
                treeByPotential = me.getValue(mp.get(treeByOverall, player['overall']))
                if om.contains(treeByPotential, player['potential']):
                    treeByWage = me.getValue(om.get(treeByPotential, player['potential']))
                    if om.contains(treeByWage, player['wage_eur']):
                        treeByAge = me.getValue(om.get(treeByWage, player['wage_eur']))
                        if om.contains(treeByAge, player['age']):
                            treeBySName = me.getValue(om.get(treeByAge, player['age']))
                            om.put(treeBySName, player['short_name'], player)
                        else:
                            treeBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                            om.put(treeBySName, player['short_name'], player)
                            om.put(treeByAge, player['age'], treeBySName)
                    else:
                        playerByAge = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                        playerBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                        om.put(playerBySName, player['short_name'], player)
                        om.put(playerByAge, player['age'], playerBySName)
                        om.put(treeByWage, player['wage_eur'], playerByAge)
                else:
                    playersByWage = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    playerByAge = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    playerBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    om.put(playerBySName, player['short_name'], player)
                    om.put(playerByAge, player['age'], playerBySName)
                    om.put(playersByWage, player['wage_eur'], playerByAge)
                    om.put(treeByPotential, player['potential'], playersByWage)
            else:
                playerByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                playersByWage = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                playerByAge = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                playerBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                om.put(playerBySName, player['short_name'], player)
                om.put(playerByAge, player['age'], playerBySName)
                om.put(playersByWage, player['wage_eur'], playerByAge)
                om.put(playerByPotential, player['potential'], playersByWage)
                om.put(treeByOverall, player['overall'], playerByPotential)
        else:
            playersByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playerByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playersByWage = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playerByAge = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playerBySName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)

            om.put(playerBySName, player['short_name'], player)
            om.put(playerByAge, player['age'], playerBySName)
            om.put(playersByWage, player['wage_eur'], playerByAge)
            om.put(playerByPotential, player['potential'], playersByWage)
            om.put(playersByOverall, player['overall'], playerByPotential)
            mp.put(analyzer['playersByPosition'], playerPosition, playersByOverall)

def addPlayerByTag(analyzer,player):
    for tag in player['player_tags']:
        tag = tag.strip()
        if mp.contains(analyzer['playersByTags'], tag):
            treeByWage = me.getValue(mp.get(analyzer['playersByTags'], tag))
            if om.contains(treeByWage, player['wage_eur']):
                treeByOverall = me.getValue(om.get(treeByWage, player['wage_eur']))
                if om.contains(treeByOverall, player['overall']):
                    treeByPotential = me.getValue(om.get(treeByOverall, player['overall']))
                    if om.contains(treeByPotential, player['potential']):
                        treeByLName = me.getValue(om.get(treeByPotential, player['potential']))
                        om.put(treeByLName, player['long_name'], player)
                    else:
                        treeByLName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                        om.put(treeByLName, player['long_name'], player)
                        om.put(treeByPotential, player['potential'], treeByLName)
                else:
                    treeByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    treeByLName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                    om.put(treeByLName, player['long_name'], player)
                    om.put(treeByPotential, player['potential'], treeByLName)
                    om.put(treeByOverall, player['overall'], treeByPotential)
            else:
                treeByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                treeByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                treeByLName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
                om.put(treeByLName, player['long_name'], player)
                om.put(treeByPotential, player['potential'], treeByLName)
                om.put(treeByOverall, player['overall'], treeByPotential)
                om.put(treeByWage, player['wage_eur'], treeByOverall)
        else:
            playersByWage = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playersByOverall = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playerByPotential = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            playerByLName = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            om.put(playerByLName, player['long_name'], player)
            om.put(playerByPotential, player['potential'], playerByLName)
            om.put(playersByOverall, player['overall'], playerByPotential)
            om.put(playersByWage, player['wage_eur'], playersByOverall)
            mp.put(analyzer['playersByTags'], tag, playersByWage)

def addPlayerByTagLst(analyzer, player):
    for tag in player['player_tags']:
        if mp.contains(analyzer['playersByTagsLt'], tag):
            treeByWage = me.getValue(mp.get(analyzer['playersByTagsLt'], tag))
            if om.contains(treeByWage, player['wage_eur']):
                lista = me.getValue(om.get(treeByWage, player['wage_eur']))
                lt.addLast(lista, player)
            else:
                lista = lt.newList('ARRAY_LIST')
                lt.addLast(lista, player)
                om.put(treeByWage, player['wage_eur'], lista)
        else:
            treeByWage = om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax)
            lista = lt.newList('ARRAY_LIST')
            lt.addLast(lista, player)
            om.put(treeByWage, player['wage_eur'], lista)
            mp.put(analyzer['playersByTagsLt'], tag, treeByWage)

def addPlayerBySName(analyzer, player):
    if mp.contains(analyzer['playersBySName'], player['short_name']):
        players = me.getValue(mp.get(analyzer['playersBySName'], player['short_name']))
        lt.addLast(players, player)
    else:
        players = lt.newList('ARRAY_LIST')
        lt.addLast(players, player)
        mp.put(analyzer['playersBySName'], player['short_name'], players)

def addPlayerByPositionForVr(analyzer, player):
    for playerPosition in player['player_positions']:
        playerPosition = playerPosition.strip()
        if mp.contains(analyzer['playersByPositionVr'], playerPosition):
            dataMap = me.getValue(mp.get(analyzer['playersByPositionVr'], playerPosition))
            if player['height_cm'] < me.getValue(mp.get(dataMap, 'minHeight')):
                mp.put(dataMap, 'minHeight', player['height_cm'])
            elif player['height_cm'] > me.getValue(mp.get(dataMap, 'maxHeight')):
                mp.put(dataMap, 'maxHeight', player['height_cm'])
            if player['age'] < me.getValue(mp.get(dataMap, 'minAge')):
                mp.put(dataMap, 'minAge', player['age'])
            elif player['age'] > me.getValue(mp.get(dataMap, 'maxAge')):
                mp.put(dataMap, 'maxAge', player['age'])
            if player['potential'] < me.getValue(mp.get(dataMap, 'minPotential')):
                mp.put(dataMap, 'minPotential', player['potential'])
            elif player['potential'] > me.getValue(mp.get(dataMap, 'maxPotential')):
                mp.put(dataMap, 'maxPotential', player['potential'])
            if (player['value_eur'] > 0) and (player['value_eur'] < me.getValue(mp.get(dataMap, 'minValue'))):
                mp.put(dataMap, 'minValue', player['value_eur'])
            elif (player['value_eur'] > 0) and (player['value_eur'] > me.getValue(mp.get(dataMap, 'maxValue'))):
                mp.put(dataMap, 'maxValue', player['value_eur'])

        else:
            dataMap = mp.newMap(numelements = 9,  maptype = 'PROBING', loadfactor = 0.5)
            mp.put(dataMap, 'minHeight', player['height_cm'])
            mp.put(dataMap, 'maxHeight', player['height_cm'])
            mp.put(dataMap, 'minAge', player['age'])
            mp.put(dataMap, 'maxAge', player['age'])
            mp.put(dataMap, 'minPotential', player['potential'])
            mp.put(dataMap, 'maxPotential', player['potential'])
            mp.put(dataMap, 'minValue', player['value_eur'])
            mp.put(dataMap, 'maxValue', player['value_eur'])
            mp.put(dataMap, 'treeByVr', om.newMap(omaptype = 'RBT', comparefunction = cmpKeysMinToMax))
            mp.put(analyzer['playersByPositionVr'], playerPosition, dataMap)

def addPlayersVr(analyzer, player):
    for playerPosition in player['player_positions']:
        playerPosition = playerPosition.strip()
        positionInfoMap = me.getValue(mp.get(analyzer['playersByPositionVr'], playerPosition))
        lowerHeight = me.getValue(mp.get(positionInfoMap, 'minHeight'))
        upperHeight = me.getValue(mp.get(positionInfoMap, 'maxHeight'))
        lowerAge = me.getValue(mp.get(positionInfoMap, 'minAge'))
        upperAge = me.getValue(mp.get(positionInfoMap, 'maxAge'))
        lowerPotential = me.getValue(mp.get(positionInfoMap, 'minPotential'))
        upperPotential = me.getValue(mp.get(positionInfoMap, 'maxPotential'))
        lowerValue = me.getValue(mp.get(positionInfoMap, 'minValue'))
        upperValue = me.getValue(mp.get(positionInfoMap, 'maxValue'))

        if lowerHeight == upperHeight:
            representativeValueHeight= 0
        else:
            representativeValueHeight = round((player['height_cm'] - lowerHeight)/(upperHeight - lowerHeight),4)
        if lowerAge == upperAge:
            representativeValueAge= 0
        else:
            representativeValueAge = round((player['age'] - lowerAge)/(upperAge - lowerAge),4)
        if lowerPotential == upperPotential:
            representativeValuePotential= 0
        else:
            representativeValuePotential = round((player['potential'] - lowerPotential)/(upperPotential - lowerPotential),4)
        if lowerValue == upperValue:
            representativeValueValue= 0
        else:
            representativeValueValue = round((player['value_eur'] - lowerValue)/(upperValue - lowerValue),4)
        totalVR = representativeValueHeight + representativeValueAge + representativeValuePotential + representativeValueValue
        keyName = playerPosition + 'vr'
        player[keyName] = totalVR
        treeByVr = me.getValue(mp.get(positionInfoMap, 'treeByVr'))
        addPlayerByKeyFloat(treeByVr, player, keyName)

# Funciones para creacion de datos

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 1]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByClubName(analyzer, clubName):
    playersByClubNameArray = lt.newList('ARRAY_LIST')
    mapByClub = mp.get(analyzer['playersByClubName'], clubName)
    if mapByClub:
        treeByJoin = me.getValue(mapByClub)
        for treesByAge in lt.iterator(om.valueSet(treeByJoin)):
            for treesByDob in lt.iterator(om.valueSet(treesByAge)):
                for playersBySName in lt.iterator(om.valueSet(treesByDob)):
                    for player in lt.iterator(om.valueSet(playersBySName)):
                        lt.addLast(playersByClubNameArray, player)
        top5lt = lt.subList(playersByClubNameArray,1,5)
        return top5lt, om.height(treeByJoin), om.size(treeByJoin), lt.size(playersByClubNameArray)
    return lt.newList(),0,0

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 2]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByPosition(analyzer, position, overallLower, overallUpper, potentialLower,potentialUpper, wageLower, wageUpper):
    playerByPositionAnsList = lt.newList('ARRAY_LIST')
    entryByPosition = mp.get(analyzer['playersByPosition'], position)
    default = lt.newList()
    if entryByPosition:
        treesByOverall = om.values(me.getValue(entryByPosition), overallLower, overallUpper)
        for potentialTree in lt.iterator(treesByOverall):
            treesByPotential = om.values(potentialTree, potentialLower, potentialUpper)
            for wageTree in lt.iterator(treesByPotential):
                treesByWage = om.values(wageTree, wageLower, wageUpper)
                for ageTree in lt.iterator(treesByWage):
                    for SNameTree in lt.iterator(om.valueSet(ageTree)):
                        for player in lt.iterator(om.valueSet(SNameTree)):
                            lt.addLast(playerByPositionAnsList, player)
        return playerByPositionAnsList
    return default

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 3]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByTag(analyzer, tag, WageLower, WageUpper):
    playersByTagAnsList = lt.newList('ARRAY_LIST')
    default = lt.newList()
    entry = mp.get(analyzer['playersByTags'], tag)
    if entry:
        treesByWage= om.values(me.getValue(entry), WageLower, WageUpper)
        for treesByOverall in lt.iterator(treesByWage):
            for treesByPotential in lt.iterator(om.valueSet(treesByOverall)):
                for playerByLName in lt.iterator(om.valueSet(treesByPotential)):
                    for player in lt.iterator(om.valueSet(playerByLName)):
                        lt.addLast(playersByTagAnsList, player)
        return playersByTagAnsList
    return default

def playersByTagsLt(analyzer, tag, WageLower, WageUpper):
    playersByTraitsArray = lt.newList('ARRAY_LIST')
    entry = mp.get(analyzer['playersByTagsLt'], tag)
    if entry:
        treesByWage = om.values(me.getValue(entry), WageLower, WageUpper)
        for player in lt.iterator(treesByWage):
            for inside in lt.iterator(player):
                lt.addLast(playersByTraitsArray, inside)
        playersByTraitsArray = sortLst(playersByTraitsArray, lt.size(playersByTraitsArray), tmpCmp)

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 4]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByTraits(analyzer, trait, dobMin, dobMax):
    playersByTraitsArray = lt.newList('ARRAY_LIST')
    mapByTrait = mp.get(analyzer['playersByTraits'], trait)
    if mapByTrait:
        treesByDob = om.values(me.getValue(mapByTrait), stringToDateFormat(dobMin), stringToDateFormat(dobMax))
        for treesByOverall in lt.iterator(treesByDob):
            for treesByPotential in lt.iterator(om.valueSet(treesByOverall)):
                for playersByLongname in lt.iterator(om.valueSet(treesByPotential)):
                    for player in lt.iterator(om.valueSet(playersByLongname)):
                        lt.addLast(playersByTraitsArray, player)

        return playersByTraitsArray
    return lt.newList()

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento 5]  =^..^=    =^..^=    =^..^=    =^..^=
def playersByProperties(analyzer, bins, mark, property):
    histogramArray = lt.newList('ARRAY_LIST')
    specialKey = 'playersBy' + str(property)
    treeByDesiredProperty = analyzer[specialKey]
    lowerRank = om.minKey(treeByDesiredProperty)
    upperRank = om.maxKey(treeByDesiredProperty)
    difference = upperRank - lowerRank
    intervalRange = difference/bins
    initialRank = lowerRank
    finalRank = 0
    totalConsult = me.getValue(mp.get(analyzer['totalPlayersWOUnknown'], property.lower()))
    for line in range(1, bins + 1):
        if line < bins + 1:
            dicAns = {}
            count = 0
            finalRank = initialRank + intervalRange
            dicAns['bin'] = "(" + str(round(float(initialRank),3)) + " , " + str(round(float(finalRank),3)) + "]"
            keysRanks = om.values(treeByDesiredProperty, initialRank, finalRank)
            for propertyRankLt in lt.iterator(keysRanks):
                count += lt.size(propertyRankLt)
            marks, lvl = howManyMarks(count,mark)
            dicAns['lvl'] = lvl
            dicAns['mark'] = marks
            dicAns['count'] = count
            initialRank = finalRank #+ 0.1
            lt.addLast(histogramArray, dicAns)
        else:
            dicAns = {}
            count = 0
            finalRank = upperRank
            dicAns['bin'] = "(" + str(round(initialRank,3)) + " , " + str(round(finalRank,3)) + "]"
            keysRanks = om.values(treeByDesiredProperty, initialRank, finalRank)
            for propertyRankLt in lt.iterator(keysRanks):
                count += lt.size(propertyRankLt)
            marks, lvl = howManyMarks(count,mark)
            dicAns['lvl'] = lvl
            dicAns['mark'] = marks
            dicAns['count'] = count
            lt.addLast(histogramArray, dicAns)
    return histogramArray, totalConsult

#=^..^=   =^..^=   =^..^=    =^..^=  [Requerimiento BONO]  =^..^=    =^..^=    =^..^=    =^..^=
def playerForSutitution(analyzer, player, position):
    specialKey = position + 'vr'
    #player = lt.getElement(player, 1)
    vrToMatch = player[specialKey]
    default = lt.newList()
    playersByVRArray = lt.newList('ARRAY_LIST')
    ltPossibleVRPosition = lt.newList('ARRAY_LIST')
    entry = mp.get(analyzer['playersByPositionVr'], position)
    count = me.getValue(mp.get(analyzer['totalPlayersWOUnknown'], position))
    if entry:
        mapInfoProperties = me.getValue(entry)
        treeByVr = me.getValue(mp.get(mapInfoProperties,'treeByVr'))
        if lt.size(me.getValue(om.get(treeByVr, vrToMatch))) > 1:
            for sameVRPlayer in lt.iterator(me.getValue(om.get(treeByVr, vrToMatch))):
                if player['sofifa_id'] != sameVRPlayer['sofifa_id']:
                    lt.addLast(playersByVRArray, sameVRPlayer)
            return playersByVRArray, lt.size(playersByVRArray), om.size(treeByVr)
        else:
            ltPossibleVRPositionLKD = om.keySet(treeByVr)
            ltPossibleVRPosition = linkedToArray(ltPossibleVRPositionLKD)
            stop = False
            i = 1
            top = 0
            bottom = 0
            while i <= lt.size(treeByVr) and (stop == False):
                if float(lt.getElement(ltPossibleVRPosition, i)) == vrToMatch:
                    if i > 1 :
                        bottom = float(lt.getElement(ltPossibleVRPosition, i - 1))
                    if i < lt.size(ltPossibleVRPosition):
                        top = float(lt.getElement(ltPossibleVRPosition, i + 1))
                    stop = True
                i += 1
            if abs(bottom - vrToMatch) < abs(top - vrToMatch):
                playersByVRArray = me.getValue(mp.get(treeByVr, bottom))
            elif abs(bottom - vrToMatch) > abs(top - vrToMatch):
                playersByVRArray = me.getValue(mp.get(treeByVr, top))
            elif abs(bottom - vrToMatch) == abs(top - vrToMatch):
                playersByVRArray = listsFusion(me.getValue(om.get(treeByVr, top)), me.getValue(om.get(treeByVr, bottom)))
            return playersByVRArray, lt.size(playersByVRArray), count
    return default, 0, 0


# Funciones de consulta

def playersSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['players'])

def getLastNum(number, fifaList):
    """
    Retorna los primeros number
    """
    if number <= lt.size(fifaList):
        lasts = lt.newList('ARRAY_LIST')
        for cont in range(0, number):
            element = lt.getElement(fifaList, lt.size(fifaList) - cont)
            lt.addFirst(lasts, element)
        return lasts
    else:
        return fifaList

def getFirstNum(number, fifaList):
    """
    Retorna los ultimos number
    """
    if number <= lt.size(fifaList):
        firsts = lt.newList('ARRAY_LIST')
        for cont in range(1, number + 1):
            element = lt.getElement(fifaList, cont)
            lt.addLast(firsts, element)
        return firsts
    else:
        return fifaList

# Funciones utilizadas para comparar elementos

def tmpCmp(e1,e2):
        return e1['dob'] > e2['dob']

def binaryCmp(element1, element2, key):
    'Return True if element1[key] < element2[key], False otherwise.'
    return element1[key] < element2[key]

def OverallPotentialLNCmp(element1, element2):
    if float(element1['overall']) > float(element2['overall']):
        return True
    elif float(element1['overall']) == float(element2['overall']):
        if float(element1['potential']) > float(element2['potential']):
            return True
        elif float(element1['potential']) == float(element2['potential']):
            if element1['long_name'] > element2['long_name']:
                return True
    else:
        return False

def cmpKeysMinToMax(k1, k2):
    if (k1 == k2):
        return 0
    elif (k1 > k2):
        return 1
    else:
        return -1

def cmpKeysMaxToMin(k1, k2):
    if (k1 == k2):
        return 0
    elif (k1 < k2):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def sortLst(lst, size, parameter):
    sub_list = lt.subList(lst, 1, size)
    sorted_list = mgs.sort(sub_list, parameter)
    return sorted_list

# Funciones auxiliares

def listsFusion(lst1, lst2):
    fusionList = lt.newList('ARRAY_LIST')
    for element in lt.iterator(lst1):
        lt.addLast(fusionList, element)
    for element in lt.iterator(lst2):
        lt.addLast(fusionList, element)
    return fusionList

def stringToDateFormat(stringDate):
    if stringDate == '':
        return datetime.datetime.strptime(1,1,1,1,1,1).date()
    else:
        return datetime.datetime.strptime(stringDate, '%Y-%m-%d').date()

def UXSearch(analyzer, SName):
    entry = mp.get(analyzer['playersBySName'], SName)
    #print(entry)
    if entry:
        return me.getValue(entry), lt.size(me.getValue(entry))
    return lt.newList(), 0

def linkedToArray(ltLKD):
    newArrayLt = lt.newList('ARRAY_LIST')
    for element in lt.iterator(ltLKD):
        lt.addLast(newArrayLt, element)
    return newArrayLt

def howManyMarks(total, mark):
    howMany = total//mark
    bar = '*'*howMany
    return bar, howMany


