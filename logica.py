import pandas as pd
def calcular_stats():   #Para la fase de grupos, ayuda a hacer calculos
    equipos=pd.read_excel("data/equipos.xlsx")
    partidos=pd.read_excel("data/partidos.xlsx")
    stats = equipos.copy()  #copiamos la tabla de equipos

    stats["pj"]=0     #estas columnas son solamente auxiliares
    stats["gf"]=0
    stats["gc"]=0
    stats["puntos"]=0

    for eid in equipos["id"]:  #recorre todos los equipos

        local=partidos[partidos["equipo1"] == eid]    #con local y visitante me refiero a los partidos
        visitante=partidos[partidos["equipo2"] == eid] #en donde el equipo fue el equipo 1 o el 2

        pj=len(local) + len(visitante)
        gf=int(local["goles1"].sum()) + int(visitante["goles2"].sum())
        gc=int(local["goles2"].sum()) + int(visitante["goles1"].sum())



        #las comparaciones devuelven una serie de pandas, de true y false, .sum da la cantidad de trues 
        puntos=int((local["goles1"]>local["goles2"]).sum())*3     #si la condicion es cierta 
        puntos+=int((local["goles1"]==local["goles2"]).sum())* 1     #multiplico por 3 si es que gano y
        puntos+=int((visitante["goles2"]>visitante["goles1"]).sum()) * 3     #por 1 si es que empato
        puntos+=int((visitante["goles2"]==visitante["goles1"]).sum()) * 1

        #asignar los valores, ninguno existe dentro de equipos.xlsx, se agregan en stats
        stats.loc[stats["id"]==eid, "pj"]=pj
        stats.loc[stats["id"]==eid, "gf"]=gf
        stats.loc[stats["id"]==eid, "gc"]=gc
        stats.loc[stats["id"]==eid, "puntos"]=puntos

    stats["dg"]=stats["gf"]-stats["gc"]

    return stats


def obtener_pais(id_eq):
    df=pd.read_excel("data/equipos.xlsx")
    resultado = df[df["id"]==id_eq]  #resultado guarda el df filtrado con el unico pais que tiene ese id
    if len(resultado)==0:
        return id_eq  #si no encuentra el equipo con ese id, devuelve el id
    return resultado.iloc[0]["pais"]   #accede a la primera fila, columna "pais"

def ingresar_equipo(id_eq, pais, grupo, prefijo, confederacion):
    df = pd.read_excel("data/equipos.xlsx") #Lee el dataframe
    df.loc[len(df)] = [id_eq, pais, grupo, prefijo, confederacion] #Guarda en el dataframe
    df.to_excel("data/equipos.xlsx", index=False) #Guarda en el excel sin indice

def ver_equipos():
    df=calcular_stats()
    df=df.sort_values(
        by=["puntos", "dg", "gf", "prefijo"],
        ascending=[False, False, False, False]
    )
    return df    #devuelve el dataframe en orden




def ingresar_partido(fecha, hora, lugar, equipo1, equipo2, goles1, goles2, penales1, penales2, fase):
    df = pd.read_excel("data/partidos.xlsx")
    df.loc[len(df)] = [fecha, hora, lugar, equipo1, equipo2, goles1, goles2, penales1, penales2, fase]
    df.to_excel("data/partidos.xlsx", index=False)

def ver_partidos():
    df = pd.read_excel("data/partidos.xlsx")
    return df



#Dataframes de informes
def informe_partidos_por_fecha(fecha): #Informe 1
     df=pd.read_excel("data/partidos.xlsx")
     df["fecha"]=df["fecha"].astype(str)  #se connvierte a cadena para comparar sin problemas
     fechas=df[df["fecha"] == fecha]  #Filtra las fechas que coincidan con el parametro
     return fechas



def informe_tabla_grupo(grupo):   #Informe 2
    df=calcular_stats()
    df=df[df["grupo"]==grupo.upper()]
    
    if len(df)==0:
        return None #devuelve None si el grupo no existe
    
    df=df.sort_values(     #Ordena el dataframe
        by=["puntos", "dg", "gf", "prefijo"],
        ascending=[False, False, False, False]
    )
    return df