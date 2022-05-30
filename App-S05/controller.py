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
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
size = "large" 

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def call_new_catalog():
    catalog = model.new_catalog()
    return catalog

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def load_data(catalog):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    players_file = cf.data_dir + "FIFA/fifa-players-2022-utf8-{0}.csv".format(size)
    input_file = csv.DictReader(open(players_file , encoding="utf-8"), delimiter=",")
    for player in input_file:
        model.add_player(catalog, player)

    for player in lt.iterator(catalog["players"]):
        model.calc_vr(player, catalog)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    return time, memory

    
#====================================================
#  Funciones de cada requerimiento
#====================================================

def callR1(catalog, inp_club_name):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    #Actual requirement
    n_adquisitions, player_list, league_name, league_level, height, n_elements = model.r1_answer(catalog, inp_club_name)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (n_adquisitions, player_list, league_name, league_level, height, n_elements, time, memory)

def callR2(catalog, pos_player, min_overall, max_overall, min_potential, max_potential, min_wage, max_wage):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    list_jugadores, num_jugadores = model.R2_answer(catalog, pos_player, min_overall, max_overall, min_potential, max_potential, min_wage, max_wage)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if list_jugadores == None:
        return None, None, None, None

    return time, memory, list_jugadores, num_jugadores

def callR3(catalog, in_wage_lo, in_wage_hi, in_tag):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    #Actual requirement
    n_elements, rta_list = model.r3_answer(catalog, in_wage_lo, in_wage_hi, in_tag)


    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return (n_elements, rta_list, time, memory)

def callR4(catalog,  trait, min_dob, max_dob):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    resp_list, num_jugadores = model.R4_answer(catalog,  trait, min_dob, max_dob)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    
    if resp_list == None:
        return None, None, None, None

    return time, memory, resp_list, num_jugadores

def callR5(catalog, in_bins, in_scale, prop):

    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    #Actual requirement
    n_consulted, n_used, llave_min, llave_max, ranks, total_elements, height = model.r5_answer(catalog, in_bins, in_scale, prop)
    
    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return n_consulted, n_used, llave_min, llave_max, ranks, total_elements, height, time, memory

# ___________________________________________________
#  Requerimiento 6
# ___________________________________________________
def callR6(jugador, pos, catalog):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    sustitucion , tam_jugadores_in_pos = model.R6_answer(jugador, pos, catalog)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    if sustitucion is None:
        return None, None, None, None

    return time, memory, sustitucion , tam_jugadores_in_pos

def vr_given_name(player, pos, catalog):
    return model.vr_for_name(player, pos, catalog)

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

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
    delta_memory = delta_memory/1024.0
    return delta_memory