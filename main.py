from logica import *
class Menu:
    def __init__(self, opciones):
        self.opciones=opciones
    def elegir(self):
        for i in range(len(self.opciones)):
            print(f"{i+1}. {self.opciones[i]}")
        opcion=int(input())
        while opcion<=0 or opcion>len(self.opciones):
            opcion=int(input("Opcion invalida, ingrese una opcion:\n"))
        return opcion



main_menu = Menu([
    "Configuración del Torneo",
    "Registro de Resultados",
    "Emisión de Informes",
    "Salir"
])

opcion = main_menu.elegir()

while opcion != 4:

    if opcion == 1:

        confi = Menu([
            "Ingresar equipos",
            "Ingresar partidos",
            "Ver tabla de equipos",
            "Ver tabla de partidos",
            "Volver"
        ])

        sub_opcion1 = confi.elegir()

        while sub_opcion1 != 5:

            if sub_opcion1 == 1:
                ingresar_equipo()

            elif sub_opcion1 == 2:
                ingresar_partido()

            elif sub_opcion1 == 3:
                ver_equipos()

            elif sub_opcion1 == 4:
                ver_partidos()

            sub_opcion1 = confi.elegir()

    elif opcion == 2:
        print("Registro de Resultados")

    elif opcion == 3:
        print("Emisión de Informes")

    opcion = main_menu.elegir()

print("Programa finalizado")
