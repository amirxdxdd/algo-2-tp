import pandas as pd
import os
from datetime import datetime
def calcular_stats():   
    equipos=pd.read_excel("data/equipos.xlsx")
    partidos=pd.read_excel("data/partidos.xlsx")
    stats = equipos.copy()  #copiamos la tabla de equipos

    stats["pj"]=0     #estas columnas son solamente auxiliares
    stats["gf"]=0
    stats["gc"]=0
    stats["puntos"]=0

    for eid in equipos["id"]:  #recorre todos los equipos

        local=partidos[partidos["equipo1"]==eid]    #con local y visitante me refiero a los partidos
        visitante=partidos[partidos["equipo2"]==eid]    #en donde el equipo fue el equipo 1 o el 2

        pj=len(partidos[((partidos["equipo1"]==eid) | (partidos["equipo2"]==eid)) & (partidos["jugado"]==1)])   #cuenta la cantidad de partidos jugados, revisando en eq1 0 eq2, y jugado
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
    df=pd.read_excel("data/equipos.xlsx") #Lee el dataframe
    df.loc[len(df)]=[id_eq, pais, grupo, prefijo, confederacion] #Guarda en el dataframe
    df.to_excel("data/equipos.xlsx", index=False) #Guarda en el excel sin indice

def ver_equipos():
    df=calcular_stats()
    df=df.sort_values(
        by=["puntos", "dg", "gf", "prefijo"],
        ascending=[False, False, False, False]
    )
    return df    #devuelve el dataframe en orden



def ids_disponibles(fase):   #busca los ids de los partidos aun no registrados en el calendario
    df=pd.read_excel("data/partidos.xlsx")
    
    ids_por_fase={
        "Dieciseisavos": ["M73","M74","M75","M76","M77","M78","M79","M80","M81","M82","M83","M84","M85","M86","M87","M88"],
        "Octavos": ["M89","M90","M91","M92","M93","M94","M95","M96"],
        "Cuartos": ["M97","M98","M99","M100"],
        "Semifinal": ["M101","M102"],
        "Final": ["M104"],
        "Tercer Puesto": ["M103"]
    }

    if fase not in ids_por_fase:
        return []

    ids_cargados=list(df[df["fase"]==fase]["id_partido"].astype(str))   #filtramos los que ya fueron cargados

    ids_libres=[]

    for id in ids_por_fase[fase]:  #busca en la fase seleccionada
        if id not in ids_cargados:
            ids_libres.append(id)   #los que aun no fueron cargados se agregan a la lista

    return ids_libres


def ingresar_partido(fecha, hora, lugar, equipo1, equipo2, fase, id_partido=""):
    df=pd.read_excel("data/partidos.xlsx")
    df.loc[len(df)]=[fecha, hora, lugar, equipo1, equipo2, 0, 0, 0, 0, fase, 0, id_partido]
    df.to_excel("data/partidos.xlsx", index=False)




def ver_partidos():
    df=pd.read_excel("data/partidos.xlsx")
    df["fecha"] = df["fecha"].dt.strftime("%d/%m/%Y")
    return df



def fase_actual():    #Simplemente retorna la fase actual del toreno
    if not grupos_completos():
        return "Grupos"
    if not ronda_completa("Dieciseisavos"):
        return "Dieciseisavos"
    if not ronda_completa("Octavos"):
        return "Octavos"
    if not ronda_completa("Cuartos"):
        return "Cuartos"
    if not ronda_completa("Semifinal"):
        return "Semifinal"
    if not ronda_completa("Final") or not ronda_completa("Tercer Puesto"):   #tercer lugar y final se generan juntos
        return "Final y Tercer Puesto"
    return "Torneo finalizado"


def partidos_sin_resultado(fase):   #la funcion busca entre todos los partidos de una fase que no hayan sido jugados
    df=pd.read_excel("data/partidos.xlsx")
    df["equipo1"]=df["equipo1"].fillna("")   #las columnas nulas, no son "" para pandas, hay que reemplazarlo para trabajar con ellas
    if fase=="Final y Tercer Puesto":   #cuando fase_actual() devuelve esto, no se encontrara en el excel de esa forma porque estan separados
        partidos=df[
            ((df["fase"]=="Final") | (df["fase"]=="Tercer Puesto")) &    #hay que buscarlos por separados
            (df["jugado"]==0) & (df["equipo1"]!="")   #los partidos que se muestran no tienen que estar sin equipos
        ]
    else:
        partidos=df[(df["fase"]==fase) & (df["jugado"]==0) & (df["equipo1"]!= "")]

    partidos["fecha"]=partidos["fecha"].dt.strftime('%d/%m/%Y')  #para mostrar bien la hora
    return partidos


def registrar_resultado(indice, goles1, goles2, penales1, penales2):  #asigna un resultado a un partido
    df=pd.read_excel("data/partidos.xlsx")
    df.loc[indice, "goles1"]=goles1
    df.loc[indice, "goles2"]=goles2
    df.loc[indice, "penales1"]=penales1
    df.loc[indice, "penales2"]=penales2
    df.loc[indice, "jugado"]=1   #marcar el partido como jugado
    df.to_excel("data/partidos.xlsx", index=False)


#funciones para informes
def avance_maximo(id_eq):   #maximo avance de un equipo, para el informe 3
    df=pd.read_excel("data/partidos.xlsx")

    #orden de fases de menor a mayor
    fases=["Grupos", "Dieciseisavos", "Octavos", "Cuartos", "Semifinal"]

    #verificamos si el equipo jugo en cada fase
    ultimo_avance="Fase de Grupos"

    for fase in fases:
        partidos_fase=df[
            ((df["equipo1"]==id_eq) | (df["equipo2"]==id_eq)) &   #filtrar para que sea eq1 o 2, la fase y que ya se haya jugado
            (df["fase"]==fase)]
        
        if len(partidos_fase)>0:
            ultimo_avance=fase

    #si llego a la final, verificamos si gano o perdio (campeon o vicecampeon)
    final=df[(df["fase"]=="Final") ]
    if len(final)>0:
        fila_final=final.iloc[0]
        if ganador_partido(fila_final)==id_eq:  #si gano
            return "Campeon"
        elif fila_final["equipo1"]==id_eq or fila_final["equipo2"]==id_eq:  #si perdio
            return "Vicecampeon"
        
    #si llego a tercer puesto, verificamos si gano o perdio (tercer o cuarto puesto)
    tercero = df[(df["fase"]=="Tercer Puesto") & (df["jugado"]==1)]
    if len(tercero)>0:
        fila_tercero=tercero.iloc[0]
        if ganador_partido(fila_tercero)==id_eq:   #si gano
            return "Tercer Puesto"
        elif fila_tercero["equipo1"]==id_eq or fila_tercero["equipo2"]==id_eq:   #si perdio
            return "Cuarto Puesto"

    return ultimo_avance   #si no llego ni a tercer puesto retorna su ultimo avandce de la lista de fases



#Dataframes de informes
def informe_partidos_por_fecha(fecha): #Informe 1
     df=pd.read_excel("data/partidos.xlsx")
     fecha=datetime.strptime(fecha, "%d/%m/%Y")
     df["fecha"]=pd.to_datetime(df["fecha"], dayfirst=True)  #se connvierte a datetime ambos para comparar sin problemas
     fechas=df[df["fecha"]==fecha]  #Filtra las fechas que coincidan con el parametro
     return fechas



def informe_tabla_grupo(grupo, fecha):   #Informe 2
    partidos=pd.read_excel("data/partidos.xlsx")
    equipos=pd.read_excel("data/equipos.xlsx")

    partidos["fecha"]=pd.to_datetime(partidos["fecha"], dayfirst=True)
    fecha_dt=pd.to_datetime(fecha, dayfirst=True)
    partidos=partidos[partidos["fecha"]<=fecha_dt]   #se queda solo con los partidos que estan antes de la fecha ingresada

    stats=equipos.copy()
    stats["pj"]=0
    stats["gf"]=0
    stats["gc"]=0
    stats["puntos"]=0    #hay que calcular las estadisticas al igual que con la funcion

    for eid in equipos["id"]:
        local=partidos[partidos["equipo1"]==eid]   #busca los partidos en donde fue eq1
        visitante=partidos[partidos["equipo2"]==eid]   #busca los partidos en donde fue eq2

        pj=len(local)+len(visitante)
        gf=int(local["goles1"].sum())+int(visitante["goles2"].sum())   #la cantidad de goles a favor, ya sea como eq1 o 2
        gc= int(local["goles2"].sum())+int(visitante["goles1"].sum())   #los goles en contra

        puntos=int((local["goles1"]>local["goles2"]).sum())*3
        puntos+=int((local["goles1"]==local["goles2"]).sum())*1
        puntos+=int((visitante["goles2"]>visitante["goles1"]).sum())*3
        puntos+=int((visitante["goles2"]==visitante["goles1"]).sum())*1

        stats.loc[stats["id"]==eid, "pj"]=pj
        stats.loc[stats["id"]==eid, "gf"]=gf
        stats.loc[stats["id"]==eid, "gc"]=gc
        stats.loc[stats["id"]==eid, "puntos"]=puntos

    stats["dg"]=stats["gf"]-stats["gc"]    #se crea la columna entera dg

    df=stats[stats["grupo"]==grupo.upper()]   #agarra solo el grupo ingresado


    if len(df)==0:
        return None #devuelve None si el grupo no existe
    
    df=df.sort_values(     #Ordena el dataframe
        by=["puntos", "dg", "gf", "prefijo"],
        ascending=[False, False, False, False]
    )
    return df



def informe_resultados_equipo(pais_buscado):  #Informe 3
    partidos=pd.read_excel("data/partidos.xlsx")
    equipos=pd.read_excel("data/equipos.xlsx")

    eq=equipos[equipos["pais"].str.upper()==pais_buscado.upper()]  #Obtiene la fila del equipo
    
    if len(eq)==0:
        return None, None  #por si el pais no existe

    id_eq=eq.iloc[0]["id"]

    todos=partidos[(partidos["equipo1"] == id_eq) | (partidos["equipo2"] == id_eq)]  #El | es el or logico, como en c
    todos=todos.sort_values(by="fecha")  #para que se muestre ordenado
    avance=avance_maximo(id_eq)

    return todos, avance   #retorno la tupla con todos los partidos y el ultimo avance



def informe_proximo_partido(pais_buscado, fecha_buscada):   #Informe 4
    partidos=pd.read_excel("data/partidos.xlsx")
    equipos=pd.read_excel("data/equipos.xlsx")

    eq=equipos[equipos["pais"].str.upper()==pais_buscado.upper()]

    if len(eq)==0:
        return None  #por si el pais no existe

    id_eq=eq.iloc[0]["id"]

    #buscamos todos los partidos donde jugó este equipo, como equipo 1 o 2 (local o visitante)
    todos=partidos[(partidos["equipo1"]==id_eq) | (partidos["equipo2"]==id_eq)]

    #convertimos las fechas a formato datetime para poder comparar
    todos=todos.copy()
    todos["fecha"]=pd.to_datetime(todos["fecha"], dayfirst=True)
    fecha_buscada_dt=pd.to_datetime(fecha_buscada, dayfirst=True)

    #filtramos los partidos que sean en la fecha buscada o despues
    proximos=todos[todos["fecha"]>=fecha_buscada_dt]

    if len(proximos)==0:
        return None  #Si no hay ningun partido proximo

    #ordenamos y tomamos el primero
    proximos=proximos.sort_values(by="fecha")
    proximo=proximos.iloc[0].copy()

    #convertimos la fecha de vuelta a texto para mostrarla
    proximo["fecha"]=proximo["fecha"].strftime("%d/%m/%Y")

    return proximo


def informe_todos_los_grupos():  #Informe 5
    df=calcular_stats()
    cols = ["dg", "gf", "prefijo"]
    df[cols] = df[cols].astype(int)

    grupos=sorted(df["grupo"].unique())  #obtiene los grupos sin repetir en orden
    resultado={}

    for grupo in grupos:   #Ordena los equipos en los grupos
        df_grupo = df[df["grupo"]==grupo].sort_values(
            by=["puntos", "dg", "gf", "prefijo"],
            ascending=[False, False, False, False]
        )
        resultado[grupo]=df_grupo  #guardamos cada grupo en el diccionario

    return resultado   #Retorna entonces un diccionario de dfs de grupos ordenado por grupo, con cada grupo ordenado



#Despues de la fase de grupos

def cerrar_configuracion():
    archivo=open("data/config.txt", "w")   #abrir en modo write crea el archivo si no existe
    archivo.write("cerrada")
    archivo.close()

def configuracion_cerrada():  #retorna si esta o no cerrada la config
    if not os.path.exists("data/config.txt"):    
        return False
    archivo=open("data/config.txt", "r")  
    contenido=archivo.read()
    archivo.close()
    return contenido=="cerrada"  


def grupos_completos():  #con esta funcion verifico si ya fueron jugados los partidos de la fase de grupo para comenzar con la fase eliminatoria
    df=pd.read_excel("data/partidos.xlsx")
    partidos_grupos=df[df["fase"] == "Grupos"]   #df con los partidos de la fase de grupos
    if len(partidos_grupos)==0:
        return False  #si no hay partidos cargados
    
    #si ya se jugaron todos, retorna true
    return int(partidos_grupos["jugado"].sum())==len(partidos_grupos)   #sirve para saber si mostrar o no el boton de la siguiente fase



#fase eliminatoria


def hay_partidos_de_fase(fase):
    df = pd.read_excel("data/partidos.xlsx")
    df["equipo1"] = df["equipo1"].fillna("")  #reemplaza nan por string vacio
    return len(df[(df["fase"]==fase) & (df["equipo1"]!="")]) > 0

def ronda_completa(fase):
    df=pd.read_excel("data/partidos.xlsx")
    partidos_fase=df[df["fase"]==fase]
    if len(partidos_fase)==0:
        return False
    return int(partidos_fase["jugado"].sum())==len(partidos_fase)   #True o false si ya se jugaron todos los partidos de cierta fase, para saber si habilitar o no el boton de la siguiente ronda



def ganador_partido(fila):   #ganador de un partido, recibe la fila completa del partido, retorna su id de equipo
    if fila["goles1"]>fila["goles2"]:
        return fila["equipo1"]
    elif fila["goles2"]>fila["goles1"]:
        return fila["equipo2"]
    else:
        if fila["penales1"]>fila["penales2"]:
            return fila["equipo1"]
        else:
            return fila["equipo2"]



def ganador_partido_por_id(id_partido):   #recibe el id del partido y utiliza la anterior funcion para darme el ganador de ese partido (su id de equipo)
    df = pd.read_excel("data/partidos.xlsx")
    fila = df[df["id_partido"] == id_partido].iloc[0]
    return ganador_partido(fila)



def calcular_clasificados():
    df=calcular_stats()   #calcular stats me da la informacion necesaria para ordenar
    grupos=sorted(df["grupo"].unique())  #grupos ordenadamente

    primeros=[]   #se van a guardar las filas completas de todos los primeros, segundos y terceros
    segundos=[]
    terceros=[]

    for grupo in grupos:
        df_grupo=df[df["grupo"]==grupo].sort_values(     #filas ordenadas que contiene los equipos de cada grupo
            by=["puntos", "dg", "gf", "prefijo"],
            ascending=[False, False, False, False]
        )

        primeros.append(df_grupo.iloc[0])   #el primero del grupo
        segundos.append(df_grupo.iloc[1])   #el segundo del grupo
        terceros.append(df_grupo.iloc[2])   #el tercero del grupo

    #convertimos las listas a dataframes
    df_primeros=pd.DataFrame(primeros).reset_index(drop=True)
    df_segundos=pd.DataFrame(segundos).reset_index(drop=True)
    df_terceros=pd.DataFrame(terceros).reset_index(drop=True)

    #ordenamos los terceros por los 4 criterios y tomamos los 8 mejores
    df_terceros=df_terceros.sort_values(
        by=["puntos", "dg", "gf", "prefijo"],
        ascending=[False, False, False, False]
    )
    df_terceros=df_terceros[:8]  #los 8 mejores terceros
    df_terceros=df_terceros.reset_index(drop=True)   #cuando se los devuelve al df, los indices se resetean

    return {
        "primeros": df_primeros,
        "segundos": df_segundos,
        "terceros":df_terceros
    }


#cada una de las funciones generar, asigna los equipos a los partidos de cada fase, es decir, genera los cruces

def generar_dieciseisavos():
    clasificados=calcular_clasificados()   #obtiene los primeros, segundos y 8 mejores terceros
    primeros=clasificados["primeros"]
    segundos=clasificados["segundos"]
    terceros=clasificados["terceros"]

    def primero(grupo):
        return primeros[primeros["grupo"]==grupo].iloc[0]["id"]

    def segundo(grupo):
        return segundos[segundos["grupo"]==grupo].iloc[0]["id"]

    terceros_ordenados=terceros.sort_values(by="grupo").reset_index(drop=True)
    t=list(terceros_ordenados["id"])  #list convierte el data frame a lista

    equipos_por_partido={    #los enfrentamientos entre primeros y segundos siguen el articulo 12.6 del reglamento, mientras que los terceros, lo que indica el pdf del tp
        "M73": (segundo("A"), segundo("B")),
        "M74": (primero("E"), t[4]),
        "M75": (primero("F"), segundo("C")),
        "M76": (primero("C"), segundo("F")),
        "M77": (primero("I"), t[2]),
        "M78": (segundo("E"), segundo("I")),
        "M79": (primero("A"), t[7]),
        "M80": (primero("L"), t[0]),
        "M81": (primero("D"), t[5]),
        "M82": (primero("G"), t[3]),
        "M83": (segundo("K"), segundo("L")),
        "M84": (primero("H"), segundo("J")),
        "M85": (primero("B"), t[6]),
        "M86": (primero("J"), segundo("H")),
        "M87": (primero("K"), t[1]),
        "M88": (segundo("D"), segundo("G")),
    }

    df=pd.read_excel("data/partidos.xlsx")

    #buscamos los partidos de dieciseisavos ya cargados y les asignamos los equipos en orden

    for id_partido, (eq1, eq2) in equipos_por_partido.items():   #modificar el df que contiene a los partidos, le asigna los equipos y un id
        indice=df[df["id_partido"]==id_partido].index[0]   #indice es el indice de la fila
        df.loc[indice, "equipo1"]=eq1   #se accede a esa fila en esa columna y se asigna el equipo
        df.loc[indice, "equipo2"]=eq2

    df.to_excel("data/partidos.xlsx", index=False)



def generar_octavos():    
    equipos_por_partido={   #esta tal cual en el articulo 12.7
        "M89": (ganador_partido_por_id("M74"), ganador_partido_por_id("M77")),
        "M90": (ganador_partido_por_id("M73"), ganador_partido_por_id("M75")),
        "M91": (ganador_partido_por_id("M76"), ganador_partido_por_id("M78")),
        "M92": (ganador_partido_por_id("M79"), ganador_partido_por_id("M80")),
        "M93": (ganador_partido_por_id("M83"), ganador_partido_por_id("M84")),
        "M94": (ganador_partido_por_id("M81"), ganador_partido_por_id("M82")),
        "M95": (ganador_partido_por_id("M86"), ganador_partido_por_id("M88")),
        "M96": (ganador_partido_por_id("M85"), ganador_partido_por_id("M87")),
    }

    df=pd.read_excel("data/partidos.xlsx")
    
    for id_partido, (eq1, eq2) in equipos_por_partido.items():   #modificar el df que contiene a los partidos, le asigna los equipos y un id
        indice=df[df["id_partido"]==id_partido].index[0]   #indice es el indice de la fila
        df.loc[indice, "equipo1"]=eq1   #se accede a esa fila en esa columna y se asigna el equipo
        df.loc[indice, "equipo2"]=eq2

    df.to_excel("data/partidos.xlsx", index=False)



def generar_cuartos():
    equipos_por_partido={   #tal cual el articulo 12.8
        "M97": (ganador_partido_por_id("M89"), ganador_partido_por_id("M90")),
        "M98": (ganador_partido_por_id("M93"), ganador_partido_por_id("M94")),
        "M99": (ganador_partido_por_id("M91"), ganador_partido_por_id("M92")),
        "M100": (ganador_partido_por_id("M95"), ganador_partido_por_id("M96")),
    }

    df=pd.read_excel("data/partidos.xlsx")
    
    for id_partido, (eq1, eq2) in equipos_por_partido.items():   #modificar el df que contiene a los partidos, le asigna los equipos y un id
        indice=df[df["id_partido"]==id_partido].index[0]   #indice es el indice de la fila
        df.loc[indice, "equipo1"]=eq1   #se accede a esa fila en esa columna y se asigna el equipo
        df.loc[indice, "equipo2"]=eq2

    df.to_excel("data/partidos.xlsx", index=False)



def generar_semifinal():
    equipos_por_partido={     #tal cual el articulo 12.9
        "M101": (ganador_partido_por_id("M97"), ganador_partido_por_id("M98")),
        "M102": (ganador_partido_por_id("M99"), ganador_partido_por_id("M100")),
    }

    df=pd.read_excel("data/partidos.xlsx")

    for id_partido, (eq1, eq2) in equipos_por_partido.items():   #modificar el df que contiene a los partidos, le asigna los equipos y un id
        indice=df[df["id_partido"]==id_partido].index[0]   #indice es el indice de la fila
        df.loc[indice, "equipo1"]=eq1   #se accede a esa fila en esa columna y se asigna el equipo
        df.loc[indice, "equipo2"]=eq2

    df.to_excel("data/partidos.xlsx", index=False)



def generar_final():
    df=pd.read_excel("data/partidos.xlsx")
    #final, tal cual el articulo 12.11
    eq1=ganador_partido_por_id("M101")
    eq2=ganador_partido_por_id("M102")

    #asignar equipos a la final, buscando por el id del partido
    indice_final=df[df["id_partido"]=="M104"].index[0]
    df.loc[indice_final, "equipo1"]=eq1
    df.loc[indice_final, "equipo2"]=eq2


    #tercer puesto, tal cual el articulo 12.10

    semi1=df[df["id_partido"]=="M101"].iloc[0]  #M101 y M102 son los 2 partidos semifinales
    semi2=df[df["id_partido"]=="M102"].iloc[0]

    #como eq1 y eq2 son los ganadores, los otros tienen que ser los perdedores
    if eq1==semi1["equipo1"]:
        eq3=semi1["equipo2"]
    else:
        eq3=semi1["equipo1"]

    if eq2==semi2["equipo1"]:
        eq4=semi2["equipo2"]
    else:
        eq4=semi2["equipo1"]
    
    #asignar equipos al tercer puesto, buscando por el id del partido
    indice_tercero=df[df["id_partido"]=="M103"].index[0]
    df.loc[indice_tercero, "equipo1"]=eq3
    df.loc[indice_tercero, "equipo2"]=eq4
      
    df.to_excel("data/partidos.xlsx", index=False)



#Informe extra, para el final del torneo

def generar_resumen():
    df_partidos=pd.read_excel("data/partidos.xlsx")   
    df_equipos=pd.read_excel("data/equipos.xlsx")
    stats=calcular_stats()
    grupos=sorted(df_equipos["grupo"].unique())  #obtiene los grupos ordenados y sin repetir

    resumen="RESUMEN DEL TORNEO\n"
    resumen+="─" * 50 + "\n\n"
    resumen+=f"48 selecciones participaron en el torneo.\n\n"

    #fase de grupos
    resumen+="FASE DE GRUPOS\n"
    resumen+="─" * 50 + "\n"
    for grupo in grupos:   #ordenar cada grupo
        df_grupo=stats[stats["grupo"]==grupo].sort_values(
            by=["puntos", "dg", "gf", "prefijo"],
            ascending=[False, False, False, False]
        )
        primero=df_grupo.iloc[0]["pais"]   #tomar el primero y segundo
        segundo=df_grupo.iloc[1]["pais"]
        pts=int(df_grupo.iloc[0]["puntos"])  #los puntos del primero
        resumen+=f"Grupo {grupo}: {primero} primero con {pts} puntos, {segundo} segundo.\n"

    resumen+="\n"

    #fases eliminatorias
    fases=["Dieciseisavos", "Octavos", "Cuartos", "Semifinal"]
    nombres={
        "Dieciseisavos": "DIECISEISAVOS DE FINAL",
        "Octavos": "OCTAVOS DE FINAL",
        "Cuartos": "CUARTOS DE FINAL",
        "Semifinal": "SEMIFINAL"
    }

    for fase in fases:  
        partidos_fase=df_partidos[df_partidos["fase"]==fase]  #para cada fase, se filtran todos los partidos que sean de esa fase

        if len(partidos_fase)>0:
            resumen+=f"{nombres[fase]}\n"
            resumen+="─"*50 + "\n"

            for i in range(len(partidos_fase)):   #recorrer cada partido de la fase
                fila=partidos_fase.iloc[i]   #leer fila por fila cada partido
                pais1=obtener_pais(fila["equipo1"])
                pais2=obtener_pais(fila["equipo2"])
                g1=int(fila["goles1"])
                g2=int(fila["goles2"])
                ganador=obtener_pais(ganador_partido(fila))   #con el id del equipo se obtiene el pais
                if g1==g2:
                    pen1=int(fila["penales1"])
                    pen2=int(fila["penales2"])            
                    resumen+=f"{ganador} elimino a {pais2 if ganador==pais1 else pais1} ({g1}-{g2}, penales {pen1}-{pen2})\n"     #pais 2 sera el ganador almenos que pais 1 lo sea
                else:
                    if ganador==pais1:
                        eliminado=pais2
                    else:
                        eliminado=pais1
                    resumen+=f"{ganador} elimino a {eliminado} ({g1}-{g2})\n"
                    
            resumen+="\n"

    #tercer puesto
    tercero_partido=df_partidos[df_partidos["fase"]=="Tercer Puesto"]
    if len(tercero_partido)>0:
        fila=tercero_partido.iloc[0]
        pais1=obtener_pais(fila["equipo1"])
        pais2=obtener_pais(fila["equipo2"])
        g1=int(fila["goles1"])
        g2=int(fila["goles2"])
        ganador=obtener_pais(ganador_partido(fila))
        if ganador==pais1:
            perdedor=pais2 
        else:
            perdedor=pais1

        resumen+="TERCER PUESTO\n"
        resumen+="─" * 50 + "\n"
        resumen+=f"{ganador} gano el tercer puesto ante {perdedor} ({g1}-{g2})\n\n"

    #final, igual que las fases eliminatorias, pero al final, para mas placer
    final_partido=df_partidos[df_partidos["fase"]=="Final"]
    if len(final_partido)>0:
        fila=final_partido.iloc[0]
        pais1=obtener_pais(fila["equipo1"])
        pais2=obtener_pais(fila["equipo2"])
        g1=int(fila["goles1"])
        g2=int(fila["goles2"])
        campeon=obtener_pais(ganador_partido(fila))

        if campeon==pais1:
            vice=pais2
        else:
            vice=pais1
        
        resumen+="FINAL\n"
        resumen+="─" * 50 + "\n"
        resumen+=f"La final fue {pais1} vs {pais2}\n"

        if g1==g2:
            pen1=int(fila["penales1"])
            pen2=int(fila["penales2"])
            resumen+=f"{campeon} gano la final por penales ({g1}-{g2}, penales {pen1}-{pen2})\n"
        else:
            resumen+=f"{campeon} gano la final {g1}-{g2}\n"

        resumen+=f"{vice} fue viceampeon\n"

    return resumen