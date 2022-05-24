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

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# ___________________________________________________
# Inicialización del Catálogo de jugadores
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
# Funciones para la carga de datos
# ___________________________________________________


def loadData(analyzer, playersFile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    playersFile = cf.data_dir + playersFile
    input_file = csv.DictReader(open(playersFile, encoding="utf-8"),
                                delimiter=",")
    # Por que se destruye al iterarse?
    input_file2 = csv.DictReader(open(playersFile, encoding="utf-8"),
                                 delimiter=",")
    for player in input_file2:
        model.normalizer(analyzer, player)

    for player in input_file:
        model.addPlayer(analyzer, player)
    return analyzer

# ___________________________________________________
# Funciones de ordenamiento
# ___________________________________________________

# ___________________________________________________
# Funciones de consulta sobre el catálogo
# ___________________________________________________


def playersSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.playerSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)


def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)


def lastPLayer(club, analyzer):
    return model.LastPlayers(club, analyzer)


def totalClubPlayers(club, analyzer):
    return model.totalPlayers(club, analyzer)


def posPLayers(info, analyzer):
    return model.posPlayers(info, analyzer)


def tagsAndWage(inferior, superior, tag, analyzer):
    return model.tagsAndWage(inferior, superior, tag, analyzer)


def histograma(segmentos, niveles, propiedad, analyzer):
    return model.Histograma(segmentos, niveles, propiedad, analyzer)


def playersbyTrait(trait, inferior, superior, analyzer):
    return model.playersbyTrait(trait, inferior, superior, analyzer)


def playerReplace(name, pos, analyzer):
    return model.playerReplace(name, pos, analyzer)

def sortplayers(lista):
    return model.sortById(lista)
