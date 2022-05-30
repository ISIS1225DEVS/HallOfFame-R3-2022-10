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
import time
import tracemalloc

csv.field_size_limit(2147483647)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de FIFA
def iniciarCatalogo():
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    catalog = model.iniciarCatalogo()
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return catalog, delta_time, delta_memory


# Funciones para la carga de datos
def loadPlayer(catalog):
    file = cf.data_dir + "FIFA/fifa-players-2022-utf8-large.csv"
    input = csv.DictReader(open(file, encoding="utf-8"))
    for player in input:
        model.addPlayer(catalog, player)


def creatClubIndex(catalog):
    model.creatClubIndex(catalog)


def creatPositionIndex(catalog):
    model.creatPositionIndex(catalog)


def createTagIndex(catalog):
    model.createTagIndex(catalog)


def creatTraitIndex(catalog):
    model.creatTraitIndex(catalog)


def creatPruebaIndex(catalog):
    model.creatPruebaIndex(catalog)


def creatPlayerInfoIndex(catalog):
    model.creatPlayerInfoIndex(catalog)


# Funciones de ordenamiento
def organizarID(catalog):
    catalog = model.organizarID(catalog)

    return catalog


# Funciones de consulta sobre el catálogo


def getRecentPlayersByClub(catalog, club):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta = model.getRecentPlayersByClub(catalog, club)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return respuesta, delta_time, delta_memory


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
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta = model.getPlayersByPositionPotentialWage(
        catalog,
        position,
        low_overall,
        high_overall,
        low_potential,
        high_potential,
        low_wage,
        high_wage,
    )
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return respuesta, delta_time, delta_memory


def getPlayersByTagWage(catalog, player_tag, low_wage, high_wage):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta = model.getPlayersByTagWage(catalog, player_tag, low_wage, high_wage)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return respuesta, delta_time, delta_memory


def getPlayerByTraitsDob(catalog, player_traits, low_dob, high_dob):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta = model.getPlayerByTraitsDob(catalog, player_traits, low_dob, high_dob)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return respuesta, delta_time, delta_memory


def getCantidadJugadoresPorPropiedadRango(catalog, propiedad, segmentos_rango, niveles):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    respuesta, total = model.getCantidadJugadoresPorPropiedadRango(
        catalog, propiedad, segmentos_rango, niveles
    )
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return respuesta, total, delta_time, delta_memory


# Funciones de tiempo
def getTime():
    return float(time.perf_counter() * 1000)


def getMemory():
    return tracemalloc.take_snapshot()


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory / 1024.0
    return delta_memory
