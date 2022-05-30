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
assert cf



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("====="*20)
    print("          >>               Bienvenido                    <<     ")
    print("  [R0]   q- Cargar información en el catálogo.")
    print("  [R1]   1- Reportar las cinco adquisiciones más recientes de un club.")
    print("  [R2]   2- Reportar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario.")
    print("  [R3]   3- Reportar los jugadores dentro de un rango salarial y con cierta etiqueta.")
    print("  [R4]   4- Reportar los jugadores con cierto rasgo característico y nacidos en un periodo de tiempo. ")
    print("  [R5]   5- Graficar el histograma de una propiedad para los jugadores FIFA.")
    print("  [R6]   6- Encontrar posibles sustituciones para los jugadores FIFA")
    print("         0- Salir")
    print("====="*20)


def printJugadores(catalog):
    num_jugadores = lt.size(catalog["players"])
    pos_for_prints = [1,2,3,4,5, num_jugadores-4, num_jugadores-3, num_jugadores-2,num_jugadores-1, num_jugadores]
    
    print("====="*20)
    print("      Número Total de Jugadores: {0}".format(num_jugadores))


    print(">>>   Primeros 5 jugadores cargados...   >>>")
    for pos in pos_for_prints:
        jugador = lt.getElement(catalog["players"], pos)
        if jugador['player_tags'] == '':
            jugador['player_tags'] = 'Unknown'
        if jugador['player_traits'] == '':
            jugador['player_traits'] = 'Unknown'
        print(
            "\033[1m" +
            "Nombre: " + 
            str(jugador["long_name"]) + 
            "\033[0m" +
            
            "-"*(35 - len(jugador['long_name'])) +

            "\n      Edad: " + 
            str(jugador["age"]) + 
            " "*(40 - len(str(jugador['age'])) -4)+ "Altura (cm): " + 
            str(jugador["height_cm"]) + 

            "\n      Peso (Kg): " +
            str(jugador["weight_kg"]) + 
            " "*(40 - len(str(jugador['weight_kg'])) -9)+ "Nacionalidad: " +  
            str(jugador["nationality_name"]) + 

            "\n      Desempeño general: " + 
            str(jugador['overall']) + 
            " "*(40 - len(str(jugador['overall'])) -17)+ "Potencial: "  +
            str(jugador['potential']) +

            "\n      Valor contrato (€): " +  
            str(jugador["value_eur"]) +           
            " "*(40 - len(str(jugador['value_eur'])) -18)+ "Salario (€): " +  
            str(jugador["wage_eur"]) + 

            "\n      Clausula de liberación (€): " +  
            str(jugador["release_clause_eur"]) + 
            " "*(40 - len(str(jugador['release_clause_eur'])) -26)+ "Liga: " +  
            str(jugador["league_name"]) + 

            "\n      Club: " +  
            str(jugador["club_name"]) +             
            " "*(40 - len(str(jugador['club_name'])) -4)+ "Fecha de vinculación al club: " +  
            str(jugador["club_joined"]) +

            "\n      Posiciones del jugador: " +  
            str(jugador["player_positions"]) +                          
            " "*(40 - len(str(jugador['player_positions'])) -22)+ "Reputación internacional: " +  
            str(jugador["international_reputation"]) +  

            "\n      Tags: " +  
            str(jugador["player_tags"]) +             
            " "*(40 - len(str(jugador['player_tags'])) -4)+ "Comentarios: " +  
            str(jugador["player_traits"]) +

            "\n      URL: " + 
            str(jugador['player_url']) +     
            "\n"
        )
        if pos == 5:
                print(">>>   Últimos 5 jugadores cargados...   >>>")
    

def printR1(n, player_list, league_name, league_level, inp_club):
    print("====="*20)
    print('El club {0} ha adquirido un total de {1} jugadores'.format(inp_club, n))
    print('El club está en la liga: "{0}" en el nivel: "{1}"'.format(league_name, int(float(league_level))))
    print("====="*20)
    if n is None:
        print('Busque con un club válido')
    else:
        if n < 5:
            out_n = n
        else:
            out_n = 5
        print('Los últimos {0} jugadores adquiridos son...'.format(out_n))
        for jugador in lt.iterator(player_list):
            
            if jugador['player_tags'] == '':
                jugador['player_tags'] = 'Unknown'
            if jugador['player_traits'] == '':
                jugador['player_traits'] = 'Unknown'

            print(
                "\033[1m" +
                "Nombre corto: " + 
                str(jugador["short_name"]) + 
                "\033[0m" +
                
                "-"*(35 - len(jugador['short_name'])) +

                "\n      Edad: " + 
                str(jugador["age"]) + 
                " "*(40 - len(str(jugador['age'])) -2)+ "Fecha de nacimiento: " + 
                str(jugador["dob"]) + 


                "\n      Desempeño general: " + 
                str(jugador['overall']) + 
                " "*(40 - len(str(jugador['overall'])) -15)+ "Nacionalidad: " +  
                str(jugador["nationality_name"]) +
                

                "\n      Valor contrato (€): " +  
                str(jugador["value_eur"]) +           
                " "*(40 - len(str(jugador['value_eur'])) -16)+ "Salario (€): " +  
                str(jugador["wage_eur"]) + 

                "\n      Clausula de liberación (€): " +  
                str(jugador["release_clause_eur"]) +
                " "*(40 - len(str(jugador['release_clause_eur'])) -24)+ "Fecha de vinculación al club: " +  
                str(jugador["club_joined"]) +


                "\n      Posiciones del jugador: " +  
                str(jugador["player_positions"]) +
                " "*(40 - len(str(jugador['player_positions'])) -20)+ "Posición dentro del club: " +  
                str(jugador["club_position"]) +                           


                "\n      Tags: " +  
                str(jugador["player_tags"]) +             
                " "*(40 - len(str(jugador['player_tags'])) -2)+ "Comentarios: " +  
                str(jugador["player_traits"]) +
        
                "\n"
            )

def printR2(list_jugadores, num_jugadores):
    print("\nJugadores encontrados: {0}".format(num_jugadores))
    print("Los primeros 3 Jugadores son: ")
    cuenta = 1
    for jugador in lt.iterator(list_jugadores):
        if jugador['player_tags'] == '':
            jugador['player_tags'] = 'Unknown'
        if jugador['player_traits'] == '':
            jugador['player_traits'] = 'Unknown'
        
        print(  "\033[1m" +
                "Nombre corto: " + 
                str(jugador["short_name"]) + 
                "\033[0m" +
                
                "-"*(35 - len(jugador['short_name'])) +

                "\n      Edad: " + 
                str(jugador["age"]) + 
                " "*(40 - len(str(jugador['age'])) -10)+ "Fecha de nacimiento: " + 
                str(jugador["dob"]) + 


                "\n      Nacionalidad: " + 
                str(jugador["nationality_name"]) + 
                " "*(40 - len(str(jugador["nationality_name"])) -18)+ "Valor contrato (€): " +  
                str(jugador["value_eur"]) +
                

                "\n      Salario (€): " +  
                str(jugador["wage_eur"]) +           
                " "*(40 - len(str(jugador['value_eur'])) -15)+ "Clausula de liberación (€): " +  
                str(jugador["release_clause_eur"]) + 

                "\n      Potencial: " +  
                str(jugador["potential"]) +
                " "*(40 - len(str(jugador["potential"])) -15)+ "Desempeño general: " +  
                str(jugador["overall"]) +


                "\n      Posiciones del jugador: " +  
                str(jugador["player_positions"]) +
                " "*(40 - len(str(jugador['player_positions'])) -28)+ "Tags: " +  
                str(jugador["player_tags"]) +                           


                "\n      Comentarios: " +  
                str(jugador["player_traits"]) +             
               
                "\n")
        
        cuenta += 1
        if cuenta == 4:
            print("Los últimos 3 Jugadores son: ")


def printR3(n, player_list, in_wage_lo, in_wage_hi, tag):
    print("====="*20)
    print('Con un salario entre {0} y {1} con la característica {2} hay {3} jugadores'.format(in_wage_lo, in_wage_hi, tag, n))
    print("====="*20)
    if n is None:
        print('Busque con un rango/característica válido/a')
    elif player_list is None:
        print('Busque con un rango/característica válido/a')
    else:
        print(">>>   Los primeros jugadores son...   >>>")
        tam = lt.size(player_list)
        for i in range(tam):
            jugador = lt.getElement(player_list, i+1)
            
            if jugador['player_tags'] == '':
                jugador['player_tags'] = 'Unknown'
            if jugador['player_traits'] == '':
                jugador['player_traits'] = 'Unknown'

            print(
                "\033[1m" +
                "Nombre: " + 
                str(jugador["long_name"]) + 
                "\033[0m" +
                
                "-"*(35 - len(jugador['short_name'])) +

                "\n      Edad: " + 
                str(jugador["age"]) + 
                " "*(40 - len(str(jugador['age'])) -2)+ "Fecha de nacimiento: " + 
                str(jugador["dob"]) + 


                "\n      Posiciones del jugador: " +  
                str(jugador["player_positions"]) +
                " "*(40 - len(str(jugador['player_positions'])) -20)+ "Nacionalidad: " +  
                str(jugador["nationality_name"]) + 


                "\n      Club actual: " +  
                str(jugador["club_name"]) +
                " "*(40 - len(str(jugador['club_name'])) -9)+ "Liga del club: " +  
                str(jugador["league_name"]) +


                "\n      Valor contrato (€): " +  
                str(jugador["value_eur"]) +           
                " "*(40 - len(str(jugador['value_eur'])) -16)+ "Salario (€): " +  
                str(jugador["wage_eur"]) + 


                "\n      Potencial: " + 
                str(jugador['potential']) + 
                " "*(40 - len(str(jugador['potential'])) -7)+ "Desempeño general: " +
                str(jugador['overall']) +
                

                "\n      Tags: " +  
                str(jugador["player_tags"]) +             
                " "*(40 - len(str(jugador['player_tags'])) -2)+ "Comentarios: " +  
                str(jugador["player_traits"]) +
        
                "\n"
            )
            if i == 2:
                    print(">>>   Los últimos jugadores son...   >>>")

def printR4(resp_list, num_jugadores):
    print("\nJugadores encontrados: {0}".format(num_jugadores))
    print("Los primeros 3 Jugadores son: ")

    cuenta = 1
    for jugador in lt.iterator(resp_list):
        if jugador['player_tags'] == '':
            jugador['player_tags'] = 'Unknown'
        if jugador['player_traits'] == '':
            jugador['player_traits'] = 'Unknown' 

        print(
                "\033[1m" +
                "Nombre: " + 
                str(jugador["long_name"]) + 
                "\033[0m" +
                
                "-"*(35 - len(jugador['long_name'])) +

                "\n      Edad: " + 
                str(jugador["age"]) + 
                " "*(40 - len(str(jugador['age'])) -2)+ "Fecha de nacimiento: " + 
                str(jugador["dob"]) + 


                "\n      Posiciones del jugador: " +  
                str(jugador["player_positions"]) +
                " "*(40 - len(str(jugador['player_positions'])) -20)+ "Nacionalidad: " +  
                str(jugador["nationality_name"]) + 


                "\n      Club actual: " +  
                str(jugador["club_name"]) +
                " "*(40 - len(str(jugador['club_name'])) -9)+ "Liga del club: " +  
                str(jugador["league_name"]) +


                "\n      Valor contrato (€): " +  
                str(jugador["value_eur"]) +           
                " "*(40 - len(str(jugador['value_eur'])) -16)+ "Salario (€): " +  
                str(jugador["wage_eur"]) + 


                "\n      Potencial: " + 
                str(jugador['potential']) + 
                " "*(40 - len(str(jugador['potential'])) -7)+ "Desempeño general: " +
                str(jugador['overall']) +
                

                "\n      Tags: " +  
                str(jugador["player_tags"]) +             
                " "*(40 - len(str(jugador['player_tags'])) -2)+ "Comentarios: " +  
                str(jugador["player_traits"]) +
        
                "\n"
            )
        cuenta  +=1 
    
        if cuenta == 4:
            print("Los últimos 3 Jugadores son: ")


def printR5(n_consulted, n_used, llave_min, llave_max, ranks, total_elements, height, bins, scale, prop):
    print("====="*20)
    print('     Para {0} bins, {1} como scale y propiedad: "{2}" '.format(bins, scale, prop))
    print('     Se tienen {0} jugadores con esta propiedad registrada'.format(n_consulted))
    print('     Este histograma cuenta {0} jugadores, teniendo como rango registrado: [{1}, {2}]\n'.format(n_used, llave_min, llave_max))
     
            
    print("\033[1m" +'     Rango                         Cuenta    Lvl       Marca'+"\033[0m")

    if lt.isEmpty(ranks):
        print('Busque con otros parámetros válidos')
    else:
        tam = lt.size(ranks)
        for i in range(tam):
            j = i+1
            intervalo = lt.getElement(ranks, j)
            count = lt.getElement(total_elements, j)
            altura= lt.getElement(height, j)
            printIntervalo(intervalo, count, altura)
    print("\n")
    print("====="*20)

def printIntervalo(intervalo, count, height):
    string  = '     '
    string += intervalo
    string += ' '*(30-len(intervalo))
    string += str(count)
    string += ' '*(10-len(str(count)))
    string += str(height)
    string += ' '*(10-len(str(height)))
    string += '|'
    if height > 100:
        string += 'Escoja unos niveles de marca más altos, por favor'
    else:
        string += '*'*(height)
    print(string)

def printR6(player, pos, sustituciones , tam_jugadores_in_pos, catalog):
    num_sustituciones = lt.size(sustituciones)
    nombre_jugador = player["long_name"] 
    vr_inp_jugador = controller.vr_given_name(player, pos, catalog)
    print("\n"+"====="*20)
    print("En la posición {0} juegan {1} jugadores.".format(pos, tam_jugadores_in_pos))
    print("Se hallaron {0} sutituciones para {1}, cuyo valor representativo es {2}".format(num_sustituciones, nombre_jugador,vr_inp_jugador))
    

    if num_sustituciones >= 6:
        sus1 = lt.getElement(sustituciones,1) 
        sus2 = lt.getElement(sustituciones,2)
        sus3 = lt.getElement(sustituciones,3)
        sus4 = lt.getElement(sustituciones,num_sustituciones - 2)
        sus5 = lt.getElement(sustituciones,num_sustituciones - 1)
        sus6 = lt.getElement(sustituciones,num_sustituciones)

        lista_imprimir = [sus1,sus2,sus3,sus4,sus5,sus6]

        ejec_num = 1

        print("Las ultimas 3 sustituciones son: \n")

        for jugador in lista_imprimir:
            if jugador['player_tags'] == '':
                jugador['player_tags'] = 'Unknown'
            if jugador['player_traits'] == '':
                jugador['player_traits'] = 'Unknown' 
            
            vr_sustitucion = controller.vr_given_name(jugador, pos, catalog)
            print(
                "\033[1m" +
                "Nombre: " + 
                str(jugador["long_name"]) + 
                "\033[0m" +
                
                "-"*(35 - len(jugador['long_name'])) +

                "\n      Edad: " + 
                str(jugador["age"]) + 
                " "*(40 - len(str(jugador['age'])) -2)+ "Fecha de nacimiento: " + 
                str(jugador["dob"]) + 


                "\n      Nacionalidad: " +  
                str(jugador["nationality_name"]) +
                " "*(40 - len(str(jugador["nationality_name"])) -20)+ "Valor contrato (€): " +  
                str(jugador["value_eur"]) + 


                "\n      Salario (€): " +  
                str(jugador["wage_eur"]) +
                " "*(40 - len(str(jugador["wage_eur"])) -9)+ "Club actual: " +  
                str(jugador["club_name"]) +


                "\n      Liga del club: " +  
                str(jugador["league_name"]) +           
                " "*(40 - len(str(jugador["league_name"])) -16)+ "Potencial: " +  
                str(jugador["potential"]) + 


                "\n      Desempeño General: " + 
                str(jugador['overall']) + 
                " "*(40 - len(str(jugador['overall'])) -7)+ "Posiciones: " +
                str(jugador["player_positions"]) +
                

                "\n      Valor representativo: " +  
                str(vr_sustitucion) +             
                " "*(40 - len(str(vr_sustitucion)) -2)+ "Comentarios: " +  
                str(jugador["player_traits"]) +

                 "\n      Etiquetas: " +  
                str(jugador["player_tags"]) +    

                "\n"
            )

            if ejec_num == 3:
                print("Las ultimas 3 sustituciones son:\n")

            ejec_num += 1



    else:
        for jugador in lt.iterator(sustituciones):
            if jugador['player_tags'] == '':
                jugador['player_tags'] = 'Unknown'
            if jugador['player_traits'] == '':
                jugador['player_traits'] = 'Unknown' 

            vr_sustitucion = controller.vr_given_name(jugador, pos, catalog)
            print(
                "\033[1m" +
                "Nombre: " + 
                str(jugador["long_name"]) + 
                "\033[0m" +
                
                "-"*(35 - len(jugador['long_name'])) +

                "\n      Edad: " + 
                str(jugador["age"]) + 
                " "*(40 - len(str(jugador['age'])) -6)+ "Fecha de nacimiento: " + 
                str(jugador["dob"]) + 


                "\n      Nacionalidad: " +  
                str(jugador["nationality_name"]) +
                " "*(40 - len(str(jugador["nationality_name"])) -14)+ "Valor contrato (€): " +  
                str(jugador["value_eur"]) + 


                "\n      Salario (€): " +  
                str(jugador["wage_eur"]) +
                " "*(40 - len(str(jugador["wage_eur"])) -13)+ "Club actual: " +  
                str(jugador["club_name"]) +


                "\n      Liga del club: " +  
                str(jugador["league_name"]) +           
                " "*(40 - len(str(jugador["league_name"])) -15)+ "Potencial: " +  
                str(jugador["potential"]) + 


                "\n      Desempeño General: " + 
                str(jugador['overall']) + 
                " "*(40 - len(str(jugador['overall'])) -19)+ "Posiciones: " +
                str(jugador["player_positions"]) +
                

                "\n      Valor representativo: " +  
                str(vr_sustitucion) +             
                " "*(40 - len(str(vr_sustitucion)) -22)+ "Comentarios: " +  
                str(jugador["player_traits"]) +

                 "\n      Etiquetas: " +  
                str(jugador["player_tags"]) +    

                "\n"
            )

def printTiempo_Memoria(tiempo, memoria): 
    mensaje = "****  Tiempo [ms]: {0} | Memoria [kb]: {1}  ****".format(round(tiempo,2), round(memoria,2))
    print(mensaje)


def printHeightN(height, n_elements):
    print("====="*20)
    print('La altura del árbol del club es: {0} y tiene {1} elementos'.format(height, n_elements))


"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if inputs == "q":
        print("Cargando información de los archivos ....")

        catalog = controller.call_new_catalog()

        time, memory = controller.load_data(catalog)   


        printJugadores(catalog)
        printTiempo_Memoria(time, memory)    
    
    elif inputs == "1":
        inp_club_name = input('Nombre del equipo: ')

        n_adquisitions, player_list, league_name, league_level, height, n_elements, time, memory = controller.callR1(catalog, inp_club_name)

        printR1(n_adquisitions, player_list, league_name, league_level, inp_club_name)
        printHeightN(height, n_elements)
        printTiempo_Memoria(time, memory)

    elif inputs == "2":
        inp_pos_jugador = input("Ingrese una posicion: ")
        inp_min_overall = int(input("Ingrese min Overall: "))
        inp_max_overall = int(input("Ingrese max Overall: "))
        inp_min_potential = int(input("Ingrese min Potential: "))
        inp_max_potential = int(input("Ingrese max Potential: "))
        inp_min_wage = int(input("Ingrese min Wage: "))
        inp_max_wage = int(input("Ingrese max Wage: "))

        time, memory, list_jugadores, num_jugadores = controller.callR2(catalog, inp_pos_jugador, inp_min_overall, inp_max_overall, inp_min_potential, inp_max_potential, inp_min_wage,inp_max_wage)
        if time == None:
            print("No se pudo realizar la operacion")
        else: 
            printR2(list_jugadores, num_jugadores)
            printTiempo_Memoria(time, memory)


    elif inputs == "3":
        in_wage_lo = int(input('Lim. inferior del salario: '))
        in_wage_hi = int(input('Lim. superior del salario: '))
        tag            = input('Característica:            ')

        n_elements, rta_list, time, memory = controller.callR3(catalog, in_wage_lo, in_wage_hi, tag)

        printR3(n_elements, rta_list, in_wage_lo, in_wage_hi, tag)
        printTiempo_Memoria(time, memory)

    elif inputs == "4":
        min_dob = input("Ingrese Min DoB: ")
        max_dob = input("Ingrese Max DoB: ")
        inp_trait = input("Ingrese una Característica: ")

        time, memory, resp_list, num_jugadores = controller.callR4(catalog, inp_trait, min_dob, max_dob)

        if time == None:
            print("No se pudo realizar la operacion")
        else:
            printR4(resp_list, num_jugadores)
            printTiempo_Memoria(time, memory)

    elif inputs == "5":
        in_bins  = int(input('Número de segmentos (N):       '))
        in_scale = int(input('Número de niveles x marca (x): '))
        prop         = input('Propiedad:                     ')

        n_consulted, n_used, llave_min, llave_max, ranks, total_elements, height, time, memory = controller.callR5(catalog, in_bins, in_scale, prop)

        printR5(n_consulted, n_used, llave_min, llave_max, ranks, total_elements, height, in_bins, in_scale, prop)
        printTiempo_Memoria(time, memory)

    elif inputs == "6":
        inp_name = input("Ingrese el nombre corto del jugador: ")
        exist_jugador = mp.get(catalog["R6_name_hash"], inp_name)

        if exist_jugador is None:
            print("No se encontró el jugador.\n")

        else:
            jugador = exist_jugador["value"]
            if jugador["player_positions"] == "":
                print("El jugador juega en ninguna posición.\n")
            
            else:
                posiciones = jugador["player_positions"]
                print("\n{0} juega en las posiciones: {1}. ¿Cuál desea buscar?". format(jugador["long_name"], posiciones))
                inp_pos = input("\nIngrese la posición: ")
                if inp_pos not in posiciones:
                    print("El jugador no juega en esa posición.\n")

                else:
                    time, memory, sustitucion , tam_jugadores_in_pos = controller.callR6(jugador, inp_pos, catalog)
                    if time is None:
                        print("No se pudo realizar la operación.")
                    else:
                        printR6(jugador, inp_pos, sustitucion , tam_jugadores_in_pos, catalog)
                        printTiempo_Memoria(time, memory)

    else:
        sys.exit(0)
sys.exit(0)