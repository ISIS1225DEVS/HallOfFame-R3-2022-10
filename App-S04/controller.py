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

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    playersfile = cf.data_dir + "FIFA/fifa-players-2022-utf8-large.csv"
    input_file = csv.DictReader(open(playersfile, encoding="utf-8"),
                                delimiter=",")
    for player in input_file:
        model.addPlayer(analyzer, player)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def playersSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.playersSize(analyzer)

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


def minKey(analyzer, propiedad):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer, propiedad)


def maxKey(analyzer, propiedad):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer, propiedad)

#Requerimiento 1
def getPlayersByClub(analyzer, club):
    return model.getPlayersByClub(analyzer, club)

#Requerimiento 2
def getPlayersByPositionInRange(analyzer, position, overall_lo, overall_hi, potential_lo, potential_hi, wage_lo, wage_hi):
    return model.getPlayersByPositionInRange(analyzer, position, overall_lo, overall_hi, potential_lo, potential_hi, wage_lo, wage_hi)

#Requerimiento 3
def getPlayersBySalaryTags(analyzer, salarylo, salaryhi, tag):
    return model.getPlayersBySalaryTags(analyzer, salarylo, salaryhi, tag)

#Requerimiento 4
def getPlayersByDobTraits(analyzer, dob_lo, dob_hi, trait):
    return model.getPlayersByDobTraits(analyzer, dob_lo, dob_hi, trait)

#Requerimiento 5
def getHistogramByProperty(analyzer, N, x, propiedad):
    return model.getHistogramByProperty(analyzer, N, x, propiedad)

#Requerimiento 6 (BONO)
def getPlayersMoreSimilar(analyzer, short_name, position):
    return model.getPlayersMoreSimilar(analyzer, short_name, position)
