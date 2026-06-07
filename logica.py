import pandas as pd
import os
def calcular_stats():   #Para la fase de grupos, devuelve una tabla similar a la de equipos, pero con la informacion necesaria para hacer calculos
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

        pj=len(local)+len(visitante)
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




def ingresar_partido(fecha, hora, lugar, equipo1, equipo2, goles1, goles2, penales1, penales2, fase):
    df=pd.read_excel("data/partidos.xlsx")
    df.loc[len(df)]=[fecha, hora, lugar, equipo1, equipo2, goles1, goles2, penales1, penales2, fase]
    df.to_excel("data/partidos.xlsx", index=False)

def ver_partidos():
    df = pd.read_excel("data/partidos.xlsx")
    return df





def registrar_resultado(fecha, pais1, pais2, goles1, goles2, penales1, penales2):
    df=pd.read_excel("data/partidos.xlsx")
    equipos=pd.read_excel("data/equipos.xlsx")

    #buscar los equipos
    eq1=equipos[equipos["pais"].str.upper() == pais1.upper()]
    eq2=equipos[equipos["pais"].str.upper() == pais2.upper()]

    if len(eq1)==0 or len(eq2)==0:
        return "equipo_no_existe"

    id_eq1=eq1.iloc[0]["id"]  #obtener los ids
    id_eq2=eq2.iloc[0]["id"]

    #buscamos el partido en el calendario
    df["fecha"]=df["fecha"].astype(str)
    partido=df[
        (df["fecha"]==fecha) & (df["equipo1"]==id_eq1) & (df["equipo2"]==id_eq2)]   #Busca el partido con esa fecha, ese eq1 y ese eq2

    if len(partido)==0:
        return "partido_no_existe"

    #actualizamos los goles en la fila correspondiente
    indice=partido.index[0]   #el df partido guardo el indice que tenia en el excel partidos
    df.loc[indice, "goles1"]=goles1
    df.loc[indice, "goles2"]=goles2
    df.loc[indice, "penales1"]=penales1
    df.loc[indice, "penales2"]=penales2
    df.loc[indice, "jugado"]=1 

    df.to_excel("data/partidos.xlsx", index=False)
    return "ok"   #con esto se registra el resultado



def avance_maximo(id_eq):   #maximo avance de un equipo
    df=pd.read_excel("data/partidos.xlsx")

    #orden de fases de menor a mayor
    fases=["Grupos", "Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final"]

    #verificamos si el equipo jugo en cada fase
    ultimo_avance="Fase de Grupos"

    for fase in fases:
        partidos_fase=df[
            ((df["equipo1"]==id_eq) | (df["equipo2"]==id_eq)) &   #filtrar para que sea eq1 o 2, la fase y que ya se haya jugado
            (df["fase"]==fase) &
            (df["jugado"]==1)
        ]
        if len(partidos_fase)>0:
            ultimo_avance=fase

    #si llego a la final, verificamos si gano o perdio
    final=df[(df["fase"]=="Final") & (df["jugado"]==1)]
    if len(final)>0:
        fila_final=final.iloc[0]
        if ganador_partido(fila_final)==id_eq:
            return "Campeon"
        elif fila_final["equipo1"]==id_eq or fila_final["equipo2"]==id_eq:
            return "Vicecampeon"

    return ultimo_avance



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

    eq=equipos[equipos["pais"].str.upper() == pais_buscado.upper()]
    print(f"Equipo encontrado: {eq}")

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
    df=pd.read_excel("data/partidos.xlsx")
    return len(df[df["fase"]==fase])>0   #retorna true o false si hay o no partidos de cierta fase, para no generar 2 veces los mismos partidos


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
    t=list(terceros_ordenados["id"])

    partidos={    #los enfrentamientos entre primeros y segundos siguen el articulo 12.6 del reglamento, mientras que los terceros, lo que indica el pdf del tp
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
    for id_partido in partidos:
        eq1, eq2=partidos[id_partido]
        df.loc[len(df)]=["", "", "Por definir", eq1, eq2, 0, 0, 0, 0, "Dieciseisavos", 0, id_partido]
    df.to_excel("data/partidos.xlsx", index=False)   #se guardan estos nuevos partidos en partidos.xlsx



def generar_octavos():    
    partidos={   #esta tal cual en el articulo 12.7
        "M89": (ganador_partido_por_id("M74"), ganador_partido_por_id("M77")),
        "M90": (ganador_partido_por_id("M73"), ganador_partido_por_id("M75")),
        "M91": (ganador_partido_por_id("M76"), ganador_partido_por_id("M78")),
        "M92": (ganador_partido_por_id("M79"), ganador_partido_por_id("M80")),
        "M93": (ganador_partido_por_id("M83"), ganador_partido_por_id("M84")),
        "M94": (ganador_partido_por_id("M81"), ganador_partido_por_id("M82")),
        "M95": (ganador_partido_por_id("M86"), ganador_partido_por_id("M88")),
        "M96": (ganador_partido_por_id("M85"), ganador_partido_por_id("M87")),
    }

    df = pd.read_excel("data/partidos.xlsx")
    for id_partido in partidos:
        eq1, eq2=partidos[id_partido]
        df.loc[len(df)]=["", "", "Por definir", eq1, eq2, 0, 0, 0, 0, "Octavos", 0, id_partido]
    df.to_excel("data/partidos.xlsx", index=False)



def generar_cuartos():
    partidos={   #tal cual el articulo 12.8
        "M97": (ganador_partido_por_id("M89"), ganador_partido_por_id("M90")),
        "M98": (ganador_partido_por_id("M93"), ganador_partido_por_id("M94")),
        "M99": (ganador_partido_por_id("M91"), ganador_partido_por_id("M92")),
        "M100": (ganador_partido_por_id("M95"), ganador_partido_por_id("M96")),
    }

    df=pd.read_excel("data/partidos.xlsx")
    for id_partido in partidos:
        eq1, eq2=partidos[id_partido]
        df.loc[len(df)]=["", "", "Por definir", eq1, eq2, 0, 0, 0, 0, "Cuartos", 0, id_partido]
    df.to_excel("data/partidos.xlsx", index=False)



def generar_semifinal():
    partidos={     #tal cual el articulo 12.9
        "M101": (ganador_partido_por_id("M97"), ganador_partido_por_id("M98")),
        "M102": (ganador_partido_por_id("M99"), ganador_partido_por_id("M100")),
    }

    df=pd.read_excel("data/partidos.xlsx")
    for id_partido in partidos:
        eq1, eq2=partidos[id_partido]
        df.loc[len(df)]=["", "", "Por definir", eq1, eq2, 0, 0, 0, 0, "Semifinal", 0, id_partido]
    df.to_excel("data/partidos.xlsx", index=False)



def generar_final():
    df=pd.read_excel("data/partidos.xlsx")
    #final, tal cual el articulo 12.11
    eq1=ganador_partido_por_id("M101")
    eq2=ganador_partido_por_id("M102")
    df.loc[len(df)]=["", "", "Por definir", eq1, eq2, 0, 0, 0, 0, "Final", 0, "M104"]  

    #tercer puesto, tal cual el articulo 12.10
    semi1=df[df["id_partido"]=="M101"].iloc[0]  #M101 y M102 son los 2 partidos semifinales
    semi2=df[df["id_partido"]=="M102"].iloc[0]

    #como se los ganadores, los otros tienen que ser los perdedores
    if eq1==semi1["equipo1"]:
        eq3=semi1["equipo2"]
    else:
        eq3=semi1["equipo1"]

    if eq2==semi2["equipo1"]:
        eq4=semi2["equipo2"]
    else:
        eq4=semi2["equipo1"]
    df.loc[len(df)] = ["", "", "Por definir", eq3, eq4, 0, 0, 0, 0, "Tercer Puesto", 0, "M103"]

    df.to_excel("data/partidos.xlsx", index=False)