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
 """

from App.model import cmpPlayersByID
import config as cf
import model
import csv
from typing import Any

FILE_SIZE = "large"


# Opción 0 - Carga de datos
def newController()->Any:
    """
    Crea una instancia del modelo

    Returns:
        instancia del control
    """
    control = {
        'model': None,
    }
    control['model'] = model.newCatalog()
    return control


def loadData(control: dict):
    """
    Carga los datos de los archivos en las estructuras
    correspondientes

    Args:
        control (Any): instancia
    """
    catalog = control['model']

    loadPlayers(catalog)

    players = sortPlayers(catalog)

    createMaps(catalog)
    
    return catalog["players"]


def loadPlayers(catalog: dict):
    """
    Carga a los jugadores línea por línea en el TAD lista "players" del catálogo

    Args:
        catalog (dict): modelo del control
    """
    players_file = cf.data_dir + "fifa-players-2022-utf8-" + FILE_SIZE + ".csv"

    # define columnas del CSV que se van a cargar
    input_file = csv.DictReader(open(players_file, encoding="utf-8"))

    # añadimos fila por fila cada jugador
    for player in input_file:
        model.addPlayer(catalog, player)

    return


def sortPlayers(catalog: Any):
    return model.sortPlayers(catalog)


# Opción 1 - Reportar las cinco adquisiciones más recientes de un club

def getRecentAdquisitions(control, club)->Any:
    return model.getRecentAdquisitions(control["model"], club)

# Opción 2 - Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario
def getPlayersPos(control, pos, low_ov, up_ov, low_pot, up_pot, low_sal, up_sal):
    return model.getPlayersPos(control["model"], pos, low_ov, up_ov, low_pot, up_pot, low_sal, up_sal)


# Opción 3 - Reportar los jugadores dentro de un rango salarial y con cierta etiqueta

def getWages(control, lim_inf, lim_sup, tag):
    return model.getWages(control['model'], lim_inf, lim_sup, tag)


# Opción 4 - Jugadores con una característica en un rango de tiempo de nacimiento
def getPTraitsRangeDates(control: Any, low_dob: str, up_dob: str, tra: str):
    return model.getPTraitsRangeDates(control["model"], low_dob, up_dob, tra)

def createMaps(catalog: Any):
    model.createMaps(catalog)

# Opción 5 - Crear histograma de jugadores con una propiedad
def getHistogram(control: Any, prop: str, bins: int, scale: int)->Any:
    return model.getHistogram(control["model"], prop, bins, scale)

# Opción 6
def getSustitutions(control, short_name, position):
    return model.getSustitutions(control['model'], short_name, position)