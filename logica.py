import pandas as pd
def calcular_stats():
    equipos  = pd.read_excel("data/equipos.xlsx")
    partidos = pd.read_excel("data/partidos.xlsx")
    stats = equipos.copy()  # copiamos la tabla de equipos, no modifico el excel

    stats["pj"] = 0     #estas columnas son solamente auxiliares
    stats["gf"] = 0
    stats["gc"] = 0
    stats["puntos"] = 0

    for eid in equipos["id"]:  #recorre todos los equipos

        local = partidos[partidos["equipo1"] == eid]    #con local y visitante me refiero a los partidos
        visitante = partidos[partidos["equipo2"] == eid] #en donde el equipo fue el equipo 1 o el 2

        pj = len(local) + len(visitante)
        gf = int(local["goles1"].sum()) + int(visitante["goles2"].sum())
        gc = int(local["goles2"].sum()) + int(visitante["goles1"].sum())



        #las comparaciones devuelven una serie de pandas, de true o false, .sum da la cantidad de trues 
        puntos = int((local["goles1"]     > local["goles2"]).sum())     * 3     #si la condicion es cierta 
        puntos+= int((local["goles1"]    == local["goles2"]).sum())     * 1     #multiplico por 3 si es que gano y
        puntos+= int((visitante["goles2"] > visitante["goles1"]).sum()) * 3     #por 1 si es que empato
        puntos+= int((visitante["goles2"] == visitante["goles1"]).sum()) * 1

        # asignar los valores
        stats.loc[stats["id"] == eid, "pj"]     = pj
        stats.loc[stats["id"] == eid, "gf"]     = gf
        stats.loc[stats["id"] == eid, "gc"]     = gc
        stats.loc[stats["id"] == eid, "puntos"] = puntos

    stats["dg"] = stats["gf"] - stats["gc"]

    return stats

def ingresar_equipo(id_eq, pais, grupo, prefijo, confederacion):
    df = pd.read_excel("data/equipos.xlsx") #Lee el dataframe
    df.loc[len(df)] = [id_eq, pais, grupo, prefijo, confederacion] #Guarda en el dataframe
    df.to_excel("data/equipos.xlsx", index=False) #Guarda en el excel sin indice

def ver_equipos():

    df = calcular_stats()
    df = df.sort_values(
        by=["puntos", "dg", "gf", "prefijo"],       #ordena antes de imprimir los equipos siguiendo los 4 criterios
        ascending=[False, False, False, False] #en cualquier caso se ordena de forma descendente
    )

    print(df.to_string(index=False))    #se tiene que imprimir de esta forma para que no imprima los indices

def ingresar_partido():
    df_par= pd.read_excel("data/partidos.xlsx")
    
    fecha=input("Fecha DD/MM/AAAA: ")
    hora=input("Hora HH:MM: ")
    lugar=input("Lugar: ")
    eq1=input("ID equipo 1: ").upper()
    eq2=input("ID equipo 2: ").upper()
    g1=int(input("Goles equipo 1: "))
    g2=int(input("Goles equipo 2: "))
    pen1=int(input("Penales equipo 1 (0 si no hubo): "))
    pen2=int(input("Penales equipo 2 (0 si no hubo): "))
    fase=input("Fase (Grupos/Octavos/Cuartos/Semifinal/Final): ")

    df_par.loc[len(df_par)] = [fecha, hora, lugar, eq1, eq2, g1, g2, pen1, pen2, fase]
    df_par.to_excel("data/partidos.xlsx", index=False)
    print("Partido agregado correctamente")

def ver_partidos():
    df=pd.read_excel("data/partidos.xlsx")
    print(df.to_string(index=False))

#Informes
def informe_partidos_por_fecha(fecha):
    df = pd.read_excel("data/partidos.xlsx")

    # convertimos la columna a texto para comparar sin problemas de formato
    df["fecha"] = df["fecha"].astype(str)

    resultado = df[df["fecha"] == fecha]

    if resultado.empty:     #Metodo de pandas para verificar si un dataframe esta vacio
        print(f"No hay partidos para la fecha {fecha}")
        return

    print(f"\nPartidos del {fecha}:")
    print("-" * 50)

    for i in range(len(resultado)):
        fila = resultado.iloc[i]  # iloc obtiene la fila por posicion
        print(f"{fila['hora']} hs — {fila['lugar']}")
        print(f"  {fila['equipo1']}  {int(fila['goles1'])} : {int(fila['goles2'])}  {fila['equipo2']}")
        print(f"  Fase: {fila['fase']}")
        print()