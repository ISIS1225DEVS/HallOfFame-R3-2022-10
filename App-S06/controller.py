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
import sys

default_limit = 1000
sys.setrecursionlimit(default_limit*10)
csv.field_size_limit(2147483647)

# -----------------------------------------------------
# NEW CONTROLLER
# -----------------------------------------------------

def newController():
    analyzer = model.newAnalyzer()
    return analyzer

# -----------------------------------------------------
# LOADING DATA FUNCTIONS
# -----------------------------------------------------

def loadData(analyzer):
    players_file = cf.data_dir + 'FIFA/fifa-players-2022-utf8-large.csv'
    input_file = csv.DictReader(open(players_file, encoding='utf-8'))
    for player in input_file:
        model.addPlayer(analyzer, player)
    return analyzer['players']

# -----------------------------------------------------
# GENERIC FUNCTIONS
# -----------------------------------------------------

def subList(list, pos, len):
    return model.subList(list, pos, len)

def listSize(list):
    return model.listSize(list)

def mapSize(map):
    return model.mapSize(map)

def treeSize(tree):
    return model.treeSize(tree)

# -----------------------------------------------------
# GET DATA FUNCTIONS
# -----------------------------------------------------

def requirement_1(analyzer, club_name):
    return model.requirement_1(analyzer, club_name)

def requirement_2(analyzer, position, initial_overall, final_overall, initial_potential, final_potential, initial_wage, final_wage):
    return model.requirement_2(analyzer, position, initial_overall, final_overall, initial_potential, final_potential, initial_wage, final_wage)

def requirement_3(analyzer, tag, initial_wage, final_wage):
    return model.requirement_3(analyzer, tag, initial_wage, final_wage)

def requierement_4(analyzer, trait, initial_dob, final_dob):
    return model.requierement_4(analyzer, trait, initial_dob, final_dob)

def requirement_5(analyzer, number, number_bins):
    return model.requirement_5(analyzer, number, number_bins)

def requirement_6(analyzer, player_name, player_position):
    return model.requirement_6(analyzer, player_name, player_position)