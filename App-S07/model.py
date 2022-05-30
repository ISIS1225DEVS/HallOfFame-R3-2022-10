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


from csv import list_dialects
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from datetime import datetime
import math

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def iniciarCatalogo():
    """Iniciar catalogo"""

    catalog = {
        "players": lt.newList("ARRAY_LIST"),
        "club_index": None,
        "position_index": None,
        "tag_index": None,
        "trait_index": None,
        "player_info_index": mp.newMap(16, maptype="PROBING", loadfactor=0.5),
    }

    return catalog


# Funciones para agregar informacion al catalogo
def addPlayer(catalog, FIFA_data):

    date = datetime.strptime(FIFA_data["club_joined"], "%Y-%m-%d").date()
    dob = datetime.strptime(FIFA_data["dob"], "%Y-%m-%d").date()
    positions = FIFA_data["player_positions"].replace(",", "").split()

    if FIFA_data["player_tags"] == "":
        tags = "Unknown"
    else:
        tags = FIFA_data["player_tags"].split(",")
        for posicion in range(0, len(tags)):
            tag = tags[posicion]
            if tag[0] == " ":
                tags[posicion] = tag[1:]

    if FIFA_data["player_traits"] == "":
        traits = "Unkown"
    else:
        traits = FIFA_data["player_traits"].split(",")
        for posicion in range(0, len(traits)):
            trait = traits[posicion]
            if trait[0] == " ":
                traits[posicion] = trait[1:]

    if FIFA_data["value_eur"] == "":
        value_eur = "Unkown"
    else:
        value_eur = float(FIFA_data["value_eur"])

    if FIFA_data["release_clause_eur"] == "":
        release_clause_eur = "Unkown"
    else:
        release_clause_eur = float(FIFA_data["release_clause_eur"])

    player_info = {
        # player personal information
        "sofifa_id": FIFA_data["sofifa_id"],
        "long_name": FIFA_data["long_name"],
        "short_name": FIFA_data["short_name"],
        "age": int(FIFA_data["age"]),
        "dob": dob,
        "nationality_name": FIFA_data["nationality_name"],
        "height_cm": int(FIFA_data["height_cm"]),
        "weight_kg": int(FIFA_data["weight_kg"]),
        "potential": int(FIFA_data["potential"]),
        "overall": int(FIFA_data["overall"]),
        "wage_eur": float(FIFA_data["wage_eur"]),
        "value_eur": value_eur,
        "release_clause_eur": release_clause_eur,
        "player_tags": tags,
        "player_tagss": ", ".join(map(str, tags)),
        "player_traits": traits,
        "player_traitss": ",".join(map(str, traits)),
        # player club information
        "club_name": FIFA_data["club_name"],
        "club_joined": date,
        "player_positions": positions,
        "player_positionss": ",".join(map(str, positions)),
        "league_name": FIFA_data["league_name"],
        "league_level": round(float(FIFA_data["league_level"])),
    }
    lt.addLast(catalog["players"], player_info)


# Funciones para creacion de datos
def creatClubIndex(catalog):
    catalog["club_index"] = om.newMap(omaptype="RBT")
    club_index = catalog["club_index"]

    for player in lt.iterator(catalog["players"]):
        club_name = player["club_name"]

        if om.contains(club_index, club_name):
            player_list = om.get(club_index, club_name)["value"]
            lt.addLast(player_list, player)

        else:
            player_list = lt.newList("ARRAY_LIST")
            lt.addLast(player_list, player)
            om.put(club_index, club_name, player_list)


def creatPositionIndex(catalog):
    catalog["position_index"] = om.newMap(omaptype="RBT")
    positon_index = catalog["position_index"]

    for player in lt.iterator(catalog["players"]):
        positions = player["player_positions"]

        for position in positions:

            if om.contains(positon_index, position):
                player_list = om.get(positon_index, position)["value"]
                lt.addLast(player_list, player)

            else:
                player_list = lt.newList("ARRAY_LIST")
                lt.addLast(player_list, player)
                om.put(positon_index, position, player_list)


def createTagIndex(catalog):
    catalog["tag_index"] = om.newMap(omaptype="RBT")
    tag_index = catalog["tag_index"]

    for player in lt.iterator(catalog["players"]):
        tags = player["player_tags"]

        for tag in tags:

            if om.contains(tag_index, tag):
                player_list = om.get(tag_index, tag)["value"]
                lt.addLast(player_list, player)
            else:
                player_list = lt.newList("ARRAY_LIST")
                lt.addLast(player_list, player)
                om.put(tag_index, tag, player_list)


def creatTraitIndex(catalog):
    catalog["trait_index"] = om.newMap(omaptype="RBT")
    trait_index = catalog["trait_index"]

    for player in lt.iterator(catalog["players"]):
        traits = player["player_traits"]

        for trait in traits:

            if om.contains(trait_index, trait):
                player_list = om.get(trait_index, trait)["value"]
                lt.addLast(player_list, player)

            else:
                player_list = lt.newList("ARRAY_LIST")
                lt.addLast(player_list, player)
                om.put(trait_index, trait, player_list)


def creatPlayerInfoIndex(catalog):
    player_info_index = catalog["player_info_index"]

    keys = [
        "overall",
        "potential",
        "value_eur",
        "wage_eur",
        "age",
        "height_cm",
        "weight_kg",
        "release_clause_eur",
    ]
    for key in keys:

        key_index = om.newMap(omaptype="RBT")

        for player in lt.iterator(catalog["players"]):
            if player[key] == "Unkown":
                pass

            else:
                rbt_key = player[key]

                if om.contains(key_index, rbt_key):
                    player_list = om.get(key_index, rbt_key)["value"]
                    lt.addLast(player_list, player)

                else:
                    player_list = lt.newList("ARRAY_LIST")
                    lt.addLast(player_list, player)
                    om.put(key_index, rbt_key, player_list)

        mp.put(player_info_index, key, key_index)


# Funciones de consulta


# Funciones utilizadas para comparar elementos dentro de una lista


# Requerimiento 1----------------------------------------------------------------------------------------


def getRecentPlayersByClub(catalog, club):
    club_index = catalog["club_index"]

    if om.contains(club_index, club):
        player_list = om.get(club_index, club)["value"]

        return organizarDate(player_list)

    else:
        return "No existe ese club ( ´･･)ﾉ(._.`)"


# Requerimiento 2----------------------------------------------------------------------------------------


def getPlayersByPositionPotentialWage(
    catalog,
    position,
    low_overall,
    high_overall,
    low_potential,
    high_potential,
    low_wage,
    high_wage,
):
    position_index = catalog["position_index"]

    if om.contains(position_index, position):
        player_list = om.get(position_index, position)["value"]

        player_list = organizarOverall(player_list)

        list_uno = lt.newList("ARRAY_LIST")
        for player in lt.iterator(player_list):
            overall = player["overall"]
            if low_overall <= overall and overall <= high_overall:
                lt.addLast(list_uno, player)
        organizarPotential(list_uno)

        list_dos = lt.newList("ARRAY_LIST")
        for player in lt.iterator(list_uno):
            potential = player["potential"]
            if low_potential <= potential and potential <= high_potential:
                lt.addLast(list_dos, player)
        organizarWage(list_dos)

        list_final = lt.newList("ARRAY_LIST")
        for player in lt.iterator(list_dos):
            wage = player["wage_eur"]
            if low_wage <= wage and wage <= high_wage:
                lt.addLast(list_final, player)

        if lt.size(list_final) == 0:
            return "No hay jugadores en esa posicion con esas especificaciones"
        else:

            return organizarOverallPotentialWage(list_final)

    else:
        return "Esa posicion no existe ಥ_ಥ"


# Requerimiento 3----------------------------------------------------------------------------------------


def getPlayersByTagWage(catalog, player_tag, low_wage, high_wage):
    tag_index = catalog["tag_index"]

    if om.contains(tag_index, player_tag):
        player_list = om.get(tag_index, player_tag)["value"]

        list_uno = lt.newList("ARRAY_LIST")
        for player in lt.iterator(player_list):
            tags = player["player_tags"]
            for tag in tags:
                if player_tag == tag:
                    lt.addLast(list_uno, player)

        list_dos = lt.newList("ARRAY_LIST")
        for player in lt.iterator(list_uno):
            wage = player["wage_eur"]
            if low_wage <= wage and wage <= high_wage:
                lt.addLast(list_dos, player)
        if lt.size(list_dos) == 0:
            return "No hay jugadores con esta especificacion"
        else:
            return organizarWage(list_dos)
    else:
        return "Este player_tag no existe ಥ_ಥ"


# Requerimiento 4----------------------------------------------------------------------------------------


def getPlayerByTraitsDob(catalog, player_traits, low_dob, high_dob):
    low_dob = datetime.strptime(low_dob, "%Y-%m-%d").date()
    high_dob = datetime.strptime(high_dob, "%Y-%m-%d").date()
    trait_index = catalog["trait_index"]

    if om.contains(trait_index, player_traits):
        player_list = om.get(trait_index, player_traits)["value"]

        list_uno = lt.newList("ARRAY_LIST")
        for player in lt.iterator(player_list):
            traits = player["player_traits"]
            for trait in traits:
                if player_traits == trait:
                    lt.addLast(list_uno, player)
        list_dos = lt.newList("ARRAY_LIST")
        for player in lt.iterator(list_uno):
            dob = player["dob"]
            if low_dob <= dob and dob <= high_dob:
                lt.addLast(list_dos, player)
        if lt.size(list_dos) == 0:
            return "No hay jugadores con esta especificaion"
        else:
            return organizarDob(list_dos)
    else:
        return "Ese trait no existe"


# Requerimiento 5----------------------------------------------------------------------------------------


def getCantidadJugadoresPorPropiedadRango(catalog, propiedad, segmentos_rango, niveles):

    if mp.contains(catalog["player_info_index"], propiedad):
        propiedad_index = mp.get(catalog["player_info_index"], propiedad)["value"]
        low_key = om.minKey(propiedad_index)
        big_key = om.maxKey(propiedad_index)
        # math
        diff = (big_key - low_key) / segmentos_rango
        respuesta = lt.newList("ARRAY_LIST")
        low_key_solo = low_key - 0.004

        low_range = low_key_solo
        big_range = (low_key + diff) + 0.0004
        total = 0

        for _ in range(segmentos_rango):
            players_lists = om.values(
                propiedad_index, math.ceil(low_range), math.floor(big_range)
            )
            count = 0
            info_bin = {}
            for player in lt.iterator(players_lists):
                count += lt.size(player)

            lv = count // niveles
            info_bin = {
                "bin": (
                    "("
                    + str(round(low_range, 3))
                    + " , "
                    + str(round(big_range, 3))
                    + "]"
                ),
                "count": count,
                "lvl": lv,
                "mark": lv * "*",
            }
            lt.addLast(respuesta, info_bin)
            low_range = big_range
            big_range = low_range + diff
            total += count

        return respuesta, total
    else:
        return "Esa propiedad no existe"


# Funciones de ordenamiento
def organizarID(catalog):

    ms.sort(catalog["players"], compareFifa_id)

    return catalog


def organizarDate(player_list):

    return ms.sort(player_list, compareClubDate)


def organizarOverall(player_list):

    return ms.sort(player_list, compareOverall)


def organizarPotential(player_list):

    return ms.sort(player_list, comparePotential)


def organizarWage(player_list):

    return ms.sort(player_list, compareWage)


def organizarOverallPotentialWage(player_list):

    return ms.sort(player_list, compareOverallPotentialWage)


def organizarDob(player_list):
    return ms.sort(player_list, compareDob)


# Comparing Functions
def compareFifa_id(id1, id2):

    if id1["sofifa_id"] > id2["sofifa_id"]:
        return False
    else:
        return True


def compareClubDate(date1, date2):

    if date1["club_joined"] == date2["club_joined"]:
        if date1["age"] > date2["age"]:
            return False
        elif date1["age"] < date2["age"]:
            return True
        else:
            if date1["dob"] > date2["dob"]:
                return True
            elif date1["dob"] < date2["dob"]:
                return False
            else:
                if date1["short_name"] < date2["short_name"]:
                    return True
                else:
                    return False

    if date1["club_joined"] > date2["club_joined"]:
        return True

    else:
        return False


def compareOverall(overall1, overall2):

    if overall1["overall"] > overall2["overall"]:
        return True

    else:
        return False


def comparePotential(potential1, potential2):

    if potential1["potential"] > potential2["potential"]:
        return True

    else:
        return False


def compareWage(wage1, wage2):

    if wage1["wage_eur"] == wage2["wage_eur"]:
        if wage1["overall"] > wage2["overall"]:
            return True
        elif wage1["overall"] < wage2["overall"]:
            return False
        else:
            if wage1["potential"] > wage2["potential"]:
                return True
            elif wage1["potential"] < wage2["potential"]:
                return False
            else:
                if wage1["long_name"] < wage2["long_name"]:
                    return True
                elif wage1["long_name"] > wage2["long_name"]:
                    return False

    elif wage1["wage_eur"] > wage2["wage_eur"]:
        return True

    else:
        return False


def compareOverallPotentialWage(player1, player2):

    if player1["overall"] > player2["overall"]:
        return True

    elif player1["overall"] == player2["overall"]:

        if player1["potential"] > player2["potential"]:
            return True

        elif player1["potential"] == player2["potential"]:

            if player1["wage_eur"] > player2["wage_eur"]:
                return True

            else:
                return False

        else:
            return False

    else:
        return False


def compareDob(player1, player2):
    if player1["dob"] > player2["dob"]:
        return True
    else:
        return False
