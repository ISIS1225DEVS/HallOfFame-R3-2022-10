"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
import time
assert cf

# -----------------------------------------------------
# NEW CONTROLLER
# -----------------------------------------------------

def newController():
    control = controller.newController()
    return control

def printMenu():
    print('\n /$$$$$$$$ /$$$$$$ /$$$$$$$$ /$$$$$$         /$$$$$$  /$$   /$$  /$$$$$$  /$$   /$$     /$$ /$$$$$$$$ /$$$$$$$$ /$$$$$$$ ')
    print('| $$_____/|_  $$_/| $$_____//$$__  $$       /$$__  $$| $$$ | $$ /$$__  $$| $$  |  $$   /$$/|_____ $$ | $$_____/| $$__  $$')
    print('| $$        | $$  | $$     | $$  \ $$      | $$  \ $$| $$$$| $$| $$  \ $$| $$   \  $$ /$$/      /$$/ | $$      | $$  \ $$')
    print('| $$$$$     | $$  | $$$$$  | $$$$$$$$      | $$$$$$$$| $$ $$ $$| $$$$$$$$| $$    \  $$$$/      /$$/  | $$$$$   | $$$$$$$/')
    print('| $$__/     | $$  | $$__/  | $$__  $$      | $$__  $$| $$  $$$$| $$__  $$| $$     \  $$/      /$$/   | $$__/   | $$__  $$')
    print('| $$        | $$  | $$     | $$  | $$      | $$  | $$| $$\  $$$| $$  | $$| $$      | $$      /$$/    | $$      | $$  \ $$')
    print('| $$       /$$$$$$| $$     | $$  | $$      | $$  | $$| $$ \  $$| $$  | $$| $$$$$$$$| $$     /$$$$$$$$| $$$$$$$$| $$  | $$')
    print('|__/      |______/|__/     |__/  |__/      |__/  |__/|__/  \__/|__/  |__/|________/|__/    |________/|________/|__/  |__/\n')

    print('0 - Load Players')
    print('1 - Report of the five more acquisitions recent from a club')
    print('2 - Report the players of a certain position within an overall, potential and salary range')
    print('3 - Report the players within a salary range and with a certain label')
    print('4 - Report the players with a certain trait characteristic and born in a period of time')
    print('5 - Graph the histogram of a property for the FIFA players')
    print('6 - Find possible substitutions for FIFA players\n')

# -----------------------------------------------------
# GENERIC FUNCTIONS
# -----------------------------------------------------

def subListElements(list, pos, len):
    return controller.subList(list, pos, len)

def listSize(list):
    return controller.listSize(list)

def mapSize(map):
    return controller.mapSize(map)

def treeSize(tree):
    return controller.treeSize(tree)

# -----------------------------------------------------
# PRINT FUNCTIONS
# -----------------------------------------------------

def printCharge(players):
    for player in lt.iterator(players):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        if player['player_traits'] == '':
            player['player_traits'] = 'UNKNOWN'
        print('Sofifa_id: ' + str(player['sofifa_id']) + ' | Long Name: ' + player['long_name'] + ' | Age: ' + str(player['age']) + ' | Height: ' + str(player['height_cm']) + ' | Weight: ' + str(player['weight_kg']) + ' | Nationality: ' + player['nationality_name'] + ' | Overall: ' + str(player['overall']) + ' | Value: ' + str(player['value_eur']) + ' | Wage: ' + str(player['wage_eur']) + ' | Release Caluse: ' + str(player['release_clause_eur']) + ' | League: ' + player['league_name'] + ' | Club: ' + player['club_name'] + ' | Club Joined: ' + player['club_joined'] + ' | Positions: ' + str(player['player_positions']) + ' | Tags: ' + str(player['player_tags']) + ' | Traits: ' + str(player['player_traits']) + ' | Player URL: ' + player['player_url'])
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')

def printReq1(players):
    for player in lt.iterator(players):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        if player['player_traits'] == '':
            player['player_traits'] = 'UNKNOWN'
        print('Club Joined: ' + player['club_joined'] + ' | Age: ' + str(player['age']) + ' | Dob: ' + player['dob'] + ' | Short Name: ' + player['short_name'] + ' | Overall: ' + str(player['overall']) + ' | Nationality: ' + player['nationality_name'] + ' | Value: ' + str(player['value_eur']) + ' | Wage: ' + str(player['wage_eur']) + ' | Release Caluse: ' + str(player['release_clause_eur']) + ' | Club Contract: ' + str(player['club_contract_valid_until']) + ' | Positions: ' + str(player['player_positions']) + ' | Club Position: ' + player['club_position'] + ' | Tags: ' + str(player['player_tags']) + ' | Traits: ' + str(player['player_traits']))
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')

def printReq2(players):
    for player in lt.iterator(players):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        if player['player_traits'] == '':
            player['player_traits'] = 'UNKNOWN'
        print('Overall: ' + str(player['overall']) + ' | Potential: ' + str(player['potential']) + ' | Wage: ' + str(player['wage_eur']) + ' | Short Name: ' + player['short_name'] + ' | Dob: ' + player['dob'] + ' | Age: ' + str(player['age']) + ' | Positions: ' + str(player['player_positions']) + ' | Nationality: ' + player['nationality_name'] + ' | Value: ' + str(player['value_eur']) + ' | Release Caluse: ' + str(player['release_clause_eur']) + ' | Club Position: ' + player['club_position'] + ' | Tags: ' + str(player['player_tags']) + ' | Traits: ' + str(player['player_traits']))
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')

def printReq3(players):
    for player in lt.iterator(players):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        if player['player_traits'] == '':
            player['player_traits'] = 'UNKNOWN'
        print('Wage: ' + str(player['wage_eur']) + ' | Overall: ' + str(player['overall']) + ' | Potential: ' + str(player['potential']) + ' | Long Name: ' + player['long_name'] + ' | Dob: ' + player['dob'] + ' | Age: ' + str(player['age']) + ' | League Name: ' + player['league_name'] + ' | Club Name: ' + player['club_name'] + ' | Positions: ' + str(player['player_positions']) + ' | Nationality: ' + player['nationality_name'] + ' | Value: ' + str(player['value_eur']) + ' | Release Caluse: ' + str(player['release_clause_eur']) + ' | Club Position: ' + player['club_position'] + ' | Tags: ' + str(player['player_tags']) + ' | Traits: ' + str(player['player_traits']))
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')

def printReq4(players):
    for player in lt.iterator(players):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        if player['player_traits'] == '':
            player['player_traits'] = 'UNKNOWN'
        print('Dob: ' + player['dob'] + ' | Overall: ' + str(player['overall']) + ' | Potential: ' + str(player['potential']) + ' | Long Name: ' + player['long_name'] + ' | Wage: ' + str(player['wage_eur']) + ' | Age: ' + str(player['age']) + ' | League Name: ' + player['league_name'] + ' | Club Name: ' + player['club_name'] + ' | Positions: ' + str(player['player_positions']) + ' | Nationality: ' + player['nationality_name'] + ' | Value: ' + str(player['value_eur']) + ' | Release Caluse: ' + str(player['release_clause_eur']) + ' | Club Position: ' + player['club_position'] + ' | Tags: ' + str(player['player_tags']) + ' | Traits: ' + str(player['player_traits']))
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')

def printReq6(players):
    for player in lt.iterator(players):
        if player['value_eur'] == 0:
            player['value_eur'] = 'UNKNOWN'
        if player['release_clause_eur'] == 0:
            player['release_clause_eur'] = 'UNKNOWN'
        if player['player_traits'] == '':
            player['player_traits'] = 'UNKNOWN'
        print('Long Name: ' + player['long_name'] + ' | Age: ' + str(player['age']) + ' | Dob: ' + player['dob'] + ' | Nationality: ' + player['nationality_name'] + ' | Value: ' + str(player['value_eur']) + ' | Wage: ' + str(player['wage_eur']) + ' | Club Name: ' + player['club_name'] + ' | League Name: ' + player['league_name'] + ' | Potential: ' + str(player['potential']) + ' | Overall: ' + str(player['overall']) + ' | Positions: ' + str(player['player_positions']) + ' | Representative Value: ' + str(player['rep_value']) + ' | Tags: ' + str(player['player_tags']) + ' | Traits: ' + str(player['player_traits']))
        print('------------------------------------------------------------------------------------------------------------------------------------------------------')

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

def loadData():
    players = controller.loadData(control)
    return players

while True:
    printMenu()
    inputs = input('Select an option to continue\n')
    if int(inputs[0]) == 0:
        control = newController()
        print("Loading information from files ....\n")
        players = loadData()
        size = treeSize(control['players_ids'])      
        print(f'Number of players: {size}')
        print('The first 5 players loaded\n')
        printCharge(subListElements(control['players'], 1, 5))
        print('\n')
        print('The last 5 players loaded\n')
        printCharge(subListElements(control['players'], -4, 5))
        print('\n')

    elif int(inputs[0]) == 1:
        club_name = input('Enter club name: ')
        club_players = controller.requirement_1(control, club_name)
        print('\n')
        if club_players == None:
            print(f'No players available for the club: {club_name}')
            print('\n')
        else:
            if club_players[1] < 5:
                print(f'{club_name} have {club_players[1]} adquisitions')
                print('\n')
            print('---- League Details ----\n')
            print(f'Name: {club_players[3]}')
            print(f'Category: {club_players[2]}\n')
            print(f'There are {club_players[4]} player in {club_name}')
            print(f'The last {club_players[1]} adquisitions of {club_name}: \n')
            printReq1(club_players[0])

    elif int(inputs[0]) == 2:
        position = input('Position: ')
        initial_overall = int(input('Enter initial overall: '))
        final_overall = int(input('Enter initial overall: '))
        initial_potential = int(input('Enter initial potential: '))
        final_potential = int(input('Enter final potential: '))
        initial_wage = float(input('Enter initial wage: '))
        final_wage = float(input('Enter final wage: '))
        print('\n')
        players = controller.requirement_2(control, position, initial_overall, final_overall, initial_potential, final_potential, initial_wage, final_wage)
        if players == None:
            print(f'No players in position: {position}')
            print('\n')
        else:
            total_players = mapSize(control['players_ids'])
            interval_players = listSize(players)
            print(f'Avilable FIFA players: {total_players}')
            print(f'Players found in range: {interval_players} and Position: {position}\n')
            if interval_players < 6:
                print(f'The {interval_players} players in range: \n')
                printReq2(players)
            else:
                print('The first 3 players in rage are: \n')
                first_three_players = subListElements(players, 1, 3)
                printReq2(first_three_players)
                print('\n')
                print('The last 3 players in rage are: \n')
                last_three_players = subListElements(players, -2, 3)
                printReq2(last_three_players)

    elif int(inputs[0]) == 3:
        tag = input('Tag: ')
        initial_wage = float(input('Enter initial wage: '))
        final_wage = float(input('Enter final wage: '))
        print('\n')
        players = controller.requirement_3(control, tag, initial_wage, final_wage)
        if players == None:
            print('There are no players in range')
        else:
            total_players = mapSize(control['players_ids'])
            interval_players = listSize(players)
            print(f'Avilable FIFA players: {total_players}')
            print(f'Players found in range: {interval_players} and Tag: {tag}\n')
            if interval_players < 6:
                print(f'The {interval_players} players in range: \n')
                printReq3(players)
            else:
                print('The first 3 players in range are: \n')
                first_three_players = subListElements(players, 1, 3)
                printReq3(first_three_players)
                print('\n')
                print('The last 3 players in rage are: \n')
                last_three_players = subListElements(players, -2, 3)
                printReq3(last_three_players)

    elif int(inputs[0]) == 4:
        trait = input('Trait: ')
        initial_dob = str(input('Enter initial dob: '))
        final_dob = str(input('Enter final dob: '))
        print('\n')
        players = controller.requierement_4(control, trait,initial_dob,final_dob )
        if players == None:
            print('There are no players in range')
        else:
            interval_players = listSize(players)
            print(f'Players found in range: {interval_players} and Trait: {trait}\n')
            if interval_players < 6:
                print(f'The {interval_players} players in range: \n')
                printReq4(players)
            else:
                print('The first 3 players in range are: \n')
                first_three_players = subListElements(players, 1, 3)
                printReq4(first_three_players)
                print('\n')
                print('The last 3 players in rage are: \n')
                last_three_players = subListElements(players, -2, 3)
                printReq4(last_three_players)

    elif int(inputs[0]) == 5:
        print(
            '1 Overall\n'
            '2 Potential\n'
            '3 Value\n'
            '4 Wage\n'
            '5 Age\n'
            '6 Height\n'
            '7 Weight\n'
            '8 Release Clause\n'
            )
        property = int(input('Select a property: '))
        number_bins = int(input('Enter number of intervals: '))
        scale = int(input('Enter de scale: '))
        count_info = controller.requirement_5(control, property, number_bins)
        print('\n')
        print(f'There are {count_info[1]} players in the record')
        print(f'The histogram counts {count_info[2]} players\n')
        for i in lt.iterator(count_info[0]):
            size_i = i[2]//scale
            c = '*'*size_i
            print(f'({i[0]}, {i[1]}] -> {i[2]}: ({size_i}) {c}\n')
        print(f'NOTE: Each * represents {scale} players')
            
    elif int(inputs[0]) == 6:
        player_name = input('Enter player name: ')
        player_position = input('Position: ')
        player = controller.requirement_6(control, player_name, player_position)
        print(f'There are {player[1]} in position {player_position}')
        print(f'There are {player[2]} similar players\n')
        printReq6(player[0])

    else:
        sys.exit(0)

sys.exit(0)

