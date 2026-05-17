import pandas as pd
def ingresar_equipo():
    df = pd.read_excel("data/equipos.xlsx")

    id = int(input("ID: "))
    pais = input("País: ")
    grupo = input("Grupo: ")
    prefijo = int(input("Prefijo: "))
    confederacion = input("Confederación: ")

    df.loc[len(df)]=[id,pais,grupo,prefijo,confederacion,0,0,0,0]   #pone al equipo al final
    df.to_excel("data/equipos.xlsx", index=False)
    print("Equipo agregado correctamente")

def ver_equipos():

    df = pd.read_excel("data/equipos.xlsx")

    # diferencia de gol 
    df["dg"] = df["gf"] - df["gc"]

    
    df = df.sort_values(
        by=["puntos", "dg", "gf", "prefijo"],       #ordena antes de imprimir los equipos siguiendo los 4 criterios
        ascending=[False, False, False, False]
    )

    print(df.to_string(index=False))

def ingresar_partido():
    df_eq = pd.read_excel("data/equipos.xlsx")
    df_eq["pj"] = df_eq["pj"].astype(int)
    df_eq["gf"] = df_eq["gf"].astype(int)
    df_eq["gc"] = df_eq["gc"].astype(int)
    df_eq["puntos"] = df_eq["puntos"].astype(int)
    df_par= pd.read_excel("data/partidos.xlsx")
    fecha = input("Ingrese la fecha DD/MM/AAAA: ")
    eq1=int(input("ID del equipo 1: "))
    eq2=int(input("ID del equipo 2: "))

    g1=int(input("Goles equipo 1: "))
    g2=int(input("Goles del equipo 2: "))

    df_par.loc[len(df_par)]=[fecha,eq1,eq2,g1,g2]

    #busca las filas de los equipos
    i1 = df_eq[df_eq["id"] == eq1].index[0]
    i2 = df_eq[df_eq["id"] == eq2].index[0]
    
    #Actualizar los partidos jugados
    df_eq.loc[i1, "pj"] += 1
    df_eq.loc[i2, "pj"] += 1

    # actualizar goles a favor y en contra
    df_eq.loc[i1, "gf"] += g1
    df_eq.loc[i1, "gc"] += g2

    df_eq.loc[i2, "gf"] += g2
    df_eq.loc[i2, "gc"] += g1

    # actualizar puntos
    
    if g1 > g2:
        df_eq.loc[i1, "puntos"] += 3       #Si el eq1 gana

    elif g1 == g2:
        df_eq.loc[i1, "puntos"] += 1    #Si empatan
        df_eq.loc[i2, "puntos"] += 1

    else:
        df_eq.loc[i2, "puntos"] += 3    #Si el eq2 gana

    df_eq.to_excel("data/equipos.xlsx", index=False)
    df_par.to_excel("data/partidos.xlsx", index=False)
    print("Partido agregado correctamente")

def ver_partidos():
    df=pd.read_excel("data/partidos.xlsx")
    print(df.to_string(index=False))