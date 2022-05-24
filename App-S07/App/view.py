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

from traceback import print_exception
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
import pandas as pd
from tabulate import tabulate

assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def searchInputReq5(info_ask):
    if info_ask == 1:
        return "overall"
    elif info_ask == 2:
        return "potential"
    elif info_ask == 3:
        return "value_eur"
    elif info_ask == 4:
        return "wage_eur"
    elif info_ask == 5:
        return "age"
    elif info_ask == 6:
        return "height_cm"
    elif info_ask == 7:
        return "weight_kg"
    elif info_ask == 8:
        return "release_clause_eur"


def printMenu():
    print("\n")
    print("--------------------------------------------")
    print("Bienvenido")
    print("0- Crear catálogo y cargar información")
    print("1- Dar las 5 adquisicions mas recientes de un club (Req-1)")
    print(
        "2- Dar los jugadores de cierta posición dentro de un rango de desempeño, potencial y salario (Req-2)"
    )
    print(
        "3- Dar los jugadores dentro de un rango salarial y con cierta etiqueta (Req-3)"
    )
    print(
        "4- Dar los jugadores con ciertos rasgos característico y nacido en un periodo de tiempo (Req-4)"
    )
    print("5- Graficar el histograma de una propiedad para los jugadores FIFA (Req-5)")
    print("--------------------------------------------")


def printreq5Menu():
    print("\n--------------------------------------------")
    print("PROPIEDADES")
    print("1- Overall")
    print("2- Potential")
    print("3- Value in eur")
    print("4- Wage in eur")
    print("5- age")
    print("6- Height in cm")
    print("7- Weight in Kg")
    print("8- release clause in eur")
    print("--------------------------------------------")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar\n")

    # ---------------------------------------------------------------------------------------------------------------------------------------

    if int(inputs[0]) == 0:

        catalog, delta_time, delta_memory = controller.iniciarCatalogo()
        print("\n" + "Se ha creado el catalogo (☞ﾟヮﾟ)☞")
        print("Cargando información de los archivos ....")
        controller.loadPlayer(catalog)
        catalog = controller.organizarID(catalog)

        columns = [
            "long_name",
            "age",
            "dob",
            "overall",
            "nationality_name",
            "wage_eur",
            "value_eur",
            "potential",
            "player_positionss",
            "release_clause_eur",
            "player_tags",
            "player_traitss",
            "club_name",
        ]
        df = pd.DataFrame(catalog["players"]["elements"], columns=columns)

        first5 = df.head(5)
        last5 = df.tail(5)
        tabla = first5.append(last5)
        tabla["long_name"] = tabla["long_name"].str.wrap(10)
        tabla["club_name"] = tabla["club_name"].str.wrap(10)
        tabla["player_traitss"] = tabla["player_traitss"].str.wrap(10)
        tabla["player_positionss"] = tabla["player_positionss"].str.wrap(10)

        print("\nLos 5 primeros y 5 ultimos datos cargados:")
        print(tabulate(tabla, headers=columns, tablefmt="grid", showindex=False))
        print("Se ha cargado la informacion del archivo ☜(ﾟヮﾟ☜)")
        print(f"El tiempo de carga es de: {round(delta_time,3)} ms")
        print(f"La memoria es de {round(delta_memory,3)} kB")

    # ---------------------------------------------------------------------------------------------------------------------------------------

    elif int(inputs[0]) == 1:
        controller.creatClubIndex(catalog)
        print("=" * 30 + " Input " + "=" * 30)
        club = input(
            "Ingrese el nombre del club del que desea buscar sus 5 ingresos mas recientes: "
        )
        respuesta, delta_time, delta_memory = controller.getRecentPlayersByClub(
            catalog, club
        )
        if type(respuesta) == str:
            print("\n" + "=" * 30 + " Req No. 1 Input " + "=" * 30)
            print("Las 5 adquisiciones mas recientes de " + "'" + club + "'")
            print("\n" + "=" * 30 + " Req No. 1 Answers " + "=" * 30)
            print(respuesta)

        else:
            columns = [
                "short_name",
                "age",
                "dob",
                "overall",
                "nationality_name",
                "wage_eur",
                "value_eur",
                "club_joined",
                "player_positionss",
                "release_clause_eur",
                "player_tags",
                "player_traitss",
                "club_joined",
            ]
            df = pd.DataFrame(respuesta["elements"], columns=columns)
            df["player_traitss"] = df["player_traitss"].str.wrap(16)
            df["player_positionss"] = df["player_positionss"].str.wrap(16)
            first5 = df.head(5)
            size = respuesta["size"]
            league_level = lt.firstElement(respuesta)["league_level"]
            league_name = lt.firstElement(respuesta)["league_name"]

            print("\n" + "=" * 30 + " Req No. 1 Input " + "=" * 30)
            print(f"Las 5 adquisiciones mas recientes de '{club}'")

            print("\n" + "=" * 30 + " Req No. 1 Answers " + "=" * 30)
            print(f"Total de jugadores adquiridos por {club}: {size}")
            print("----Datos sobre la liga----")
            print(f"Nombre de la liga: '{league_name}'")
            print(f"Nivel de la liga: {league_level}")
            print(tabulate(first5, headers=columns, tablefmt="grid", showindex=False))
            print(f"El tiempo de carga es de: {round(delta_time,3)} ms")
            print(f"La memoria es de {round(delta_memory,3)} kB")

    # ---------------------------------------------------------------------------------------------------------------------------------------

    elif int(inputs[0]) == 2:
        controller.creatPositionIndex(catalog)

        print("=" * 30 + " Inputs " + "=" * 30)
        position = input("Ingrese la posicion que desea buscar: ")
        low_overall = int(input("Ingrese el desepeño minimo que desea buscar: "))
        high_overall = int(input("Ingrese el desepeño maximo que desea buscar: "))
        low_potential = int(input("Ingrese el potencial minimo que desea buscar: "))
        high_potential = int(input("Ingrese el potencial maximo que desea buscar: "))
        low_wage = float(input("Ingrese el sueldo minimo en euros que desea buscar: "))
        high_wage = float(input("Ingrese el sueldo maximo en euros que desea buscar: "))

        (
            respuesta,
            delta_time,
            delta_memory,
        ) = controller.getPlayersByPositionPotentialWage(
            catalog,
            position,
            low_overall,
            high_overall,
            low_potential,
            high_potential,
            low_wage,
            high_wage,
        )
        if type(respuesta) == str:
            print("\n" + "=" * 30 + " Req No. 2 Input " + "=" * 30)
            print(f"Se busco los jugadores con la posicion: '{position}'")
            print("----Rangos----")
            print(f"Rango de 'Overall': ({low_overall} , {high_overall})")
            print(f"Rango de 'Potential': ({low_potential} , {high_potential})")
            print(f"Rango de 'Wage_eur': ({low_wage} , {high_wage})")
            print("\n" + "=" * 30 + " Req No. 2 Answers " + "=" * 30)
            print(respuesta)

        else:
            columns = [
                "short_name",
                "age",
                "dob",
                "overall",
                "nationality_name",
                "wage_eur",
                "value_eur",
                "potential",
                "player_positionss",
                "release_clause_eur",
                "player_tags",
                "player_traitss",
            ]
            df = pd.DataFrame(respuesta["elements"], columns=columns)
            df["player_traitss"] = df["player_traitss"].str.wrap(16)
            df["player_positionss"] = df["player_positionss"].str.wrap(16)
            df["player_traitss"] = df["player_traitss"].str.wrap(16)
            first3 = df.head(3)
            last3 = df.tail(3)
            tabla = first3.append(last3)
            size = respuesta["size"]

            print("\n" + "=" * 30 + " Req No. 2 Input " + "=" * 30)
            print(f"Se busco los jugadores con la posicion: '{position}'")
            print("----Rangos----")
            print(f"Rango de 'Overall': ({low_overall} , {high_overall})")
            print(f"Rango de 'Potential': ({low_potential} , {high_potential})")
            print(f"Rango de 'Wage_eur': ({low_wage} , {high_wage})")

            print("\n" + "=" * 30 + " Req No. 2 Answers " + "=" * 30)
            print(f"Total de jugadores encontrados: {size}")
            print("Los primero 3 y los ultimos 3 jugadores en el rango...")
            print(tabulate(tabla, headers=columns, tablefmt="grid", showindex=False))
            print(f"El tiempo de carga es de: {round(delta_time,3)} ms")
            print(f"La memoria es de {round(delta_memory,3)} kB")

    # ---------------------------------------------------------------------------------------------------------------------------------------

    elif int(inputs[0]) == 3:
        controller.createTagIndex(catalog)

        low_wage = float(
            input("Ingrese el valor minimo de sueldo en euros que desea buscar: ")
        )
        high_wage = float(
            input("Ingrese el valor maximo de sueldo en euros que desea buscar: ")
        )
        player_tag = input("Ingrese el player tag que desea buscar: ")
        respuesta, delta_time, delta_memory = controller.getPlayersByTagWage(
            catalog, player_tag, low_wage, high_wage
        )
        if type(respuesta) == str:
            print("\n" + "=" * 30 + " Req No. 3 Input " + "=" * 30)
            print(f"Se busco los jugadores con el tag: '{player_tag}'")
            print("----Rango----")
            print(f"Rango de 'Wage_eur': ({low_wage} , {high_wage})")
            print("\n" + "=" * 30 + " Req No. 3 Answers " + "=" * 30)
            print(respuesta)

        else:
            columns = [
                "short_name",
                "age",
                "dob",
                "overall",
                "nationality_name",
                "wage_eur",
                "value_eur",
                "potential",
                "player_positionss",
                "release_clause_eur",
                "player_tagss",
                "player_traitss",
                "club_name",
            ]
            df = pd.DataFrame(respuesta["elements"], columns=columns)
            df["player_traitss"] = df["player_traitss"].str.wrap(16)
            df["player_positionss"] = df["player_positionss"].str.wrap(16)
            df["player_tagss"] = df["player_tagss"].str.wrap(20)
            df["club_name"] = df["club_name"].str.wrap(16)
            first3 = df.head(3)
            last3 = df.tail(3)
            tabla = first3.append(last3)
            size = respuesta["size"]

            print("\n" + "=" * 30 + " Req No. 3 Input " + "=" * 30)
            print(f"Se busco los jugadores con el tag: '{player_tag}'")
            print("----Rango----")
            print(f"Rango de 'Wage_eur': ({low_wage} , {high_wage})")
            print("\n" + "=" * 30 + " Req No. 3 Answers " + "=" * 30)
            print(f"Total de jugadores encontrados: {size}")
            print("Los primero 3 y los ultimos 3 jugadores en el rango...")
            print(tabulate(tabla, headers=columns, tablefmt="grid", showindex=False))
            print(f"El tiempo de carga es de: {round(delta_time,3)} ms")
            print(f"La memoria es de {round(delta_memory,3)} kB")

    # ---------------------------------------------------------------------------------------------------------------------------------------

    elif int(inputs[0]) == 4:
        controller.creatTraitIndex(catalog)
        low_dob = input("Ingrese el dob menor: ")
        high_dob = input("Ingrese el dob mayor: ")
        player_traits = input("Ingrese el player trait que desea buscar: ")

        respuesta, delta_time, delta_memory = controller.getPlayerByTraitsDob(
            catalog, player_traits, low_dob, high_dob
        )
        if type(respuesta) == str:
            print("\n" + "=" * 30 + " Req No. 4 Input " + "=" * 30)
            print(f"Se busco los jugadores con el tag: '{player_tag}'")
            print("----Rango----")
            print(f"Rango de 'dob': ({low_dob} , {high_dob})")
            print("\n" + "=" * 30 + " Req No. 4 Answers " + "=" * 30)
            print(respuesta)

        else:
            columns = [
                "long_name",
                "age",
                "dob",
                "overall",
                "nationality_name",
                "wage_eur",
                "value_eur",
                "potential",
                "player_positionss",
                "release_clause_eur",
                "player_tags",
                "player_traitss",
                "club_name",
            ]
            df = pd.DataFrame(respuesta["elements"], columns=columns)
            df["player_traitss"] = df["player_traitss"].str.wrap(16)
            df["player_positionss"] = df["player_positionss"].str.wrap(16)
            df["player_traitss"] = df["player_traitss"].str.wrap(16)
            df["club_name"] = df["club_name"].str.wrap(16)
            df["long_name"] = df["long_name"].str.wrap(16)
            first3 = df.head(3)
            last3 = df.tail(3)
            tabla = first3.append(last3)
            size = respuesta["size"]

            print("\n" + "=" * 30 + " Req No. 4 Input " + "=" * 30)
            print(f"Se busco los jugadores con el tag: '{player_tag}'")
            print("----Rango----")
            print(f"Rango de 'dob': ({low_dob} , {high_dob})")
            print("\n" + "=" * 30 + " Req No. 4 Answers " + "=" * 30)
            print(f"Total de jugadores encontrados: {size}")
            print(tabulate(tabla, headers=columns, tablefmt="grid", showindex=False))
            print(f"El tiempo de carga es de: {round(delta_time,3)} ms")
            print(f"La memoria es de {round(delta_memory,3)} kB")

    # ---------------------------------------------------------------------------------------------------------------------------------------

    elif int(inputs[0]) == 5:
        controller.creatPlayerInfoIndex(catalog)

        printreq5Menu()

        info_ask = int(input("Por cual propiedad desea buscar: "))
        propiedad = searchInputReq5(info_ask)
        segmentos_rango = int(
            input("Numero de segmentos en el que se divide el rango de propiedad: ")
        )
        niveles = int(
            input("Numero de niveles en que se dividen las marcas de jugadores: ")
        )

        (
            respuesta,
            total,
            delta_time,
            delta_memory,
        ) = controller.getCantidadJugadoresPorPropiedadRango(
            catalog, propiedad, segmentos_rango, niveles
        )
        columns = ["bin", "count", "lvl", "mark"]
        df = pd.DataFrame(respuesta["elements"], columns=columns)
        df["mark"] = df["mark"].str.wrap(60)

        print("\n" + "=" * 30 + " Req No. 5 Input " + "=" * 30)
        print(f"El histrograma se hizo de: '{propiedad}'")
        print(f"Se dividio en segmentos de: '{segmentos_rango}'")
        print(f"Son'{niveles}' de jugadores por nivel")
        print("\n" + "=" * 30 + " Req No. 5 Answers " + "=" * 30)
        print(f"Note: Cada '*' representa {niveles} jugadores")
        print(f"Se cargaron {total} jugadores")

        print(tabulate(df, headers=columns, tablefmt="grid", showindex=False))
        print(f"El tiempo de carga es de: {round(delta_time,3)} ms")
        print(f"La memoria es de {round(delta_memory,3)} kB")

    else:

        sys.exit(0)
sys.exit(0)
