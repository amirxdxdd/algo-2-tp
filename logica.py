import pandas as pd
def ingresar_equipo():
    df = pd.read_excel("data/equipos.xlsx")

    id = int(input("ID: "))
    pais = input("País: ")
    grupo = input("Grupo: ")
    prefijo = int(input("Prefijo: "))
    confederacion = input("Confederación: ")

    df.loc[len(df)]=[id,pais,grupo,prefijo,confederacion,0,0,0,0]
    df.to_excel("data/equipos.xlsx", index=False)
    print("Equipo agregado correctamente")

def ver_equipos():
    df=pd.read_excel("data/equipos.xlsx")
    print(df.to_string(index=False))