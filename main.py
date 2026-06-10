import customtkinter as ctk
from datetime import datetime
from logica import *


def construir_header(ventana_padre, titulo):   #en todas las ventanas tiene que estar el titulo de la materia, hora, etc
    header=ctk.CTkFrame(ventana_padre, corner_radius=0, fg_color="#1a1a2e")
    header.pack(fill="x")  #estira el frame de izquierda a derecha

    ctk.CTkLabel(
        header,
        text="COPA MUNDIAL FIFA 2026",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#e94560"
    ).pack(pady=(10, 0)) #10 px de espacio arriba y 0 abajo

    ctk.CTkLabel(
        header,
        text="Algoritmos y Estructuras de Datos II",
        font=ctk.CTkFont(size=10),
        text_color="#aaaaaa"
    ).pack()

    label_h=ctk.CTkLabel(header, text="", font=ctk.CTkFont(size=10), text_color="#aaaaaa")  #aca se va a poner la hora
    label_h.pack(pady=(0, 4))

    def actualizar():   #datetime.now() es el objeto hora actual del tipo datetime, strftime lo coniverte a str
        label_h.configure(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S")) #.configure() cambia el widget despues de haber sido creado, entonces la hora va a ser modificada
        ventana_padre.after(1000, actualizar) #cada 1000ms (1 segundo) se vuelve a ejecutar la funcioon

    actualizar() 

    ctk.CTkLabel(
        header,
        text=titulo,   #el titulo de la ventana
        font=ctk.CTkFont(size=16, weight="bold"),
        text_color="#ffffff"
    ).pack(pady=(4, 10))


#Funciones para configuracion del torneo
def abrir_ingresar_equipo():   #Todo igual a las otras ventanas
    ventana_equipo = ctk.CTkToplevel(ventana)   
    ventana_equipo.title("Ingresar Equipo")
    ventana_equipo.geometry("420x600")   #Esto debe tener este tamaño minimo para que aparezca el boton de guardar
    ventana_equipo.resizable(False, False)  #No se puede cambiar la resolucion
    

    construir_header(ventana_equipo, "Ingresar equipo")

    #Aca pongo los campos del formulario
    frame_form = ctk.CTkFrame(ventana_equipo, fg_color="transparent")
    frame_form.pack(padx=40, pady=20, fill="x")

    #los campos del formulario
    campos=["ID (ej: A1)", "Pais", "Grupo (ej: A)", "Prefijo telefonico", "Confederacion"]
    entradas={}  #uso un diccionario para guardar cada campo y acceder a su valor despues

    for campo in campos:
        ctk.CTkLabel(
            frame_form,
            text=campo,
            anchor="w" #anchor="w" alinea el texto a la izquierda, west es oeste en ingles
        ).pack(fill="x", pady=(5, 1))

        entrada=ctk.CTkEntry(frame_form, width=340)   #Crea un cuadro para ingresar datos
        entrada.pack()
        entradas[campo] = entrada   #se guarda la entrada en el diccionario con el nombre del campo como clave

    #Label para mostrar mensajes de error o exito
    label_mensaje = ctk.CTkLabel(ventana_equipo, text="", text_color="#aaaaaa")
    label_mensaje.pack(pady=(10, 4))

    def guardar():
        id_eq=entradas["ID (ej: A1)"].get().strip().upper()         #.get() obtiene texto escrito por el usuario 
        pais=entradas["Pais"].get().strip()                         #.strip() quita los espacios que estan de mas
        grupo=entradas["Grupo (ej: A)"].get().strip().upper()       #.upper() pone en mayuscula
        prefijo=entradas["Prefijo telefonico"].get().strip()
        confederacion=entradas["Confederacion"].get().strip()

        #verificar que no hayan campos vacios
        if id_eq == "" or pais == "" or grupo == "" or prefijo == "" or confederacion == "":
            label_mensaje.configure(text="Completa todos los campos.", text_color="#e94560")
            return

        if not prefijo.isdigit():
            label_mensaje.configure(text="El prefijo debe ser un numero.", text_color="#e94560")
            return

        ingresar_equipo(id_eq, pais, grupo, int(prefijo), confederacion)   #Lo guarda en excel, el prefijo hay que ponerlo como entero por el excel
        label_mensaje.configure(text="Equipo guardado correctamente.", text_color="#44bb77")

        

    ctk.CTkButton(    #Boton para guardar equipo
        ventana_equipo,
        text="Guardar Equipo",
        width=200,
        command=guardar
    ).pack(pady=2)

    ctk.CTkButton(     #Boton para cancelar o regresar
        ventana_equipo,
        text="Volver",
        width=200,
        fg_color="transparent",     
        border_width=1,             
        command=ventana_equipo.destroy
    ).pack(pady=2)

    ventana_equipo.grab_set()  #No se puede usar la ventana anterior, tengo que ponerlo aca por problemas de linux hyperland



def abrir_ingresar_partido():
    ventana_tipo=ctk.CTkToplevel(ventana)   #Igual al anterior
    ventana_tipo.title("Ingresar Partido")
    ventana_tipo.geometry("500x400")
    ventana_tipo.resizable(False, False)

    construir_header(ventana_tipo, "Ingresar partido")

    frame=ctk.CTkFrame(ventana_tipo, fg_color="transparent")
    frame.pack(expand=True)

    ctk.CTkLabel(frame, text="Seleccionar fase del partido", font=ctk.CTkFont(size=13)).pack(pady=(0, 20))

    ctk.CTkButton(frame, text="Fase de Grupos", width=300, height=44,    #dar la opcion de elegir si el partido es de fase eliminatoria o de grupos
        command=abrir_ingresar_partido_grupos).pack(pady=8)
    
    ctk.CTkButton(frame, text="Fase Eliminatoria", width=300, height=44,
        command=abrir_ingresar_partido_eliminatorio).pack(pady=8)
      
    ctk.CTkButton(frame, text="Volver", width=300, height=44,
        fg_color="transparent", border_width=1,
        command=ventana_tipo.destroy).pack(pady=8)

    ventana_tipo.grab_set()


def abrir_ingresar_partido_grupos():
    ventana_partido=ctk.CTkToplevel(ventana)
    ventana_partido.title("Ingresar Partido - Grupos")
    ventana_partido.geometry("700x600")
    ventana_partido.resizable(False, False)

    construir_header(ventana_partido, "Ingresar Partido - Grupos")

    frame_form=ctk.CTkFrame(ventana_partido, fg_color="transparent")
    frame_form.pack(padx=40, pady=20, fill="x")

    campos=["Fecha (DD/MM/AAAA)", "Hora (HH:MM)", "Lugar", "Equipo 1", "Equipo 2"]
    entradas={}

    for campo in campos:
        ctk.CTkLabel(frame_form, text=campo, anchor="w").pack(fill="x", pady=(2, 2))
        entrada=ctk.CTkEntry(frame_form, width=340)
        entrada.pack()
        entradas[campo]=entrada

    label_mensaje=ctk.CTkLabel(ventana_partido, text="", text_color="#aaaaaa")
    label_mensaje.pack(pady=(1, 1))

    def guardar():
        fecha=entradas["Fecha (DD/MM/AAAA)"].get().strip()
        hora=entradas["Hora (HH:MM)"].get().strip()
        lugar=entradas["Lugar"].get().strip()
        pais1=entradas["Equipo 1"].get().strip()
        pais2=entradas["Equipo 2"].get().strip()

        if fecha=="" or hora=="" or lugar=="" or pais1=="" or pais2=="":
            label_mensaje.configure(text="Completa todos los campos.", text_color="#e94560")
            return

        equipos=pd.read_excel("data/equipos.xlsx")
        eq1=equipos[equipos["pais"].str.upper() == pais1.upper()]
        eq2=equipos[equipos["pais"].str.upper() == pais2.upper()]

        if len(eq1)==0 or len(eq2)==0:
            label_mensaje.configure(text="Uno de los equipos no existe.", text_color="#e94560")
            return

        id_eq1=eq1.iloc[0]["id"]
        id_eq2=eq2.iloc[0]["id"]
        ingresar_partido(fecha, hora, lugar, id_eq1, id_eq2, "Grupos") 
        label_mensaje.configure(text="Partido guardado correctamente.", text_color="#44bb77")

    ctk.CTkButton(ventana_partido, text="Guardar Partido", width=200, command=guardar).pack(pady=2)
    ctk.CTkButton(ventana_partido, text="Volver", width=200, fg_color="transparent",
        border_width=1, command=ventana_partido.destroy).pack(pady=2)

    ventana_partido.grab_set()



def abrir_ingresar_partido_eliminatorio():
    ventana_elim=ctk.CTkToplevel(ventana)
    ventana_elim.title("Ingresar Partido - Eliminatorio")
    ventana_elim.geometry("500x600")
    ventana_elim.resizable(False, False)

    construir_header(ventana_elim, "Ingresar Partido - Eliminatorio")

    frame_form=ctk.CTkFrame(ventana_elim, fg_color="transparent")
    frame_form.pack(padx=40, pady=20, fill="x")


    partidos_disponibles_ids=[None]   #uso listas porque funcionan como variable global para que se guarde al modificarlo en las funciones

    def actualizar_ids(fase):  #al seleccionar una fase, actualiza la lista de ids
        ids=ids_disponibles(fase) 
        partidos_disponibles_ids[0]=ids
        if len(ids)==0:
            selector_id.configure(values=["No hay partidos disponibles"])   #si no hay, pone eso como una opcion
            selector_id.set("No hay partidos disponibles")   #selecciona esa unica opcion
        else:
            selector_id.configure(values=ids)  #si hay, muestra todos los que hay
            selector_id.set(ids[0])   #selecciona la primera

    def al_cambiar_fase(fase):   #cada vez que se cambia de fase se actualiza la lista de ids
        actualizar_ids(fase)


    #selector de fase
    ctk.CTkLabel(frame_form, text="Fase", anchor="w").pack(fill="x", pady=(4, 2))
    selector_fase=ctk.CTkOptionMenu(   #un pequeño menu que se abrira para seleccionar fase
        frame_form,
        values=["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final", "Tercer Puesto"],
        width=340,
        command=al_cambiar_fase
    )
    selector_fase.pack()

    ctk.CTkLabel(frame_form, text="ID del partido", anchor="w").pack(fill="x", pady=(8,2))   #aca ira el otro minimenu donde estaran los ids disponibles para la fase seleccionada
    selector_id=ctk.CTkOptionMenu(frame_form, values=[""], width=340)
    selector_id.pack()

    campos=["Fecha (DD/MM/AAAA)", "Hora (HH:MM)", "Lugar"]
    entradas={}

    for campo in campos:
        ctk.CTkLabel(frame_form, text=campo, anchor="w").pack(fill="x", pady=(4, 2))
        entrada=ctk.CTkEntry(frame_form, width=340)
        entrada.pack()
        entradas[campo]=entrada

    label_mensaje=ctk.CTkLabel(ventana_elim, text="", text_color="#aaaaaa")
    label_mensaje.pack(pady=(6, 2))

    def guardar():
        fase=selector_fase.get()
        id_partido=selector_id.get()
        fecha=entradas["Fecha (DD/MM/AAAA)"].get().strip()
        hora=entradas["Hora (HH:MM)"].get().strip()
        lugar=entradas["Lugar"].get().strip()

        if id_partido=="No hay partidos disponibles":
            label_mensaje.configure(text="No hay partidos para esa fase")
            return

        if fecha=="" or hora=="" or lugar=="":
            label_mensaje.configure(text="Completa todos los campos.", text_color="#e94560")
            return

        #equipos vacios, se asignaran al generar la fase
        ingresar_partido(fecha, hora, lugar, "", "", fase, id_partido)
        label_mensaje.configure(text="Partido guardado correctamente.", text_color="#44bb77")
        actualizar_ids(fase)   #para que una vez ingresado, ya no este disponible

    ctk.CTkButton(ventana_elim, text="Guardar Partido", width=200, command=guardar).pack(pady=1)
    ctk.CTkButton(ventana_elim, text="Volver", width=200, fg_color="transparent",
        border_width=1, command=ventana_elim.destroy).pack(pady=4)

    actualizar_ids(generar_dieciseisavos)   #al abrir la ventana, automaticamente la lista se refresca, por defecto en diesiceisavos
    ventana_elim.grab_set()    




def abrir_ver_equipos():
    ventana_equipos = ctk.CTkToplevel(ventana)  #Igual que todas las ventanas
    ventana_equipos.title("Ver Equipos")
    ventana_equipos.geometry("700x700")
    ventana_equipos.resizable(False, False)

    construir_header(ventana_equipos, "Ver equipos")

    #ctktextbox crea un cuadro de texto para mostrar datos
    textbox=ctk.CTkTextbox(ventana_equipos, width=660, height=500, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=20)

    df=ver_equipos()  #guardo el contenido del excel en el dataframe df
    textbox.insert("end", df.to_string(index=False))  #el contenido se inserta en el cuadro    
    textbox.configure(state="disabled") #si no se desactiva el usuario puede modificar el cuadro

    ctk.CTkButton(
        ventana_equipos,
        text="Volver",
        width=200,
        fg_color="transparent",
        border_width=1,
        command=ventana_equipos.destroy
    ).pack()

    ventana_equipos.grab_set()





def abrir_ver_partidos():
    ventana_partidos = ctk.CTkToplevel(ventana)   #Igual que todas las ventanas
    ventana_partidos.title("Ver Partidos")
    ventana_partidos.geometry("900x800")
    ventana_partidos.resizable(False, False)

    construir_header(ventana_partidos, "Ver partidos")

    textbox=ctk.CTkTextbox(ventana_partidos, width=860, height=600, font=ctk.CTkFont(family="Courier", size=12))   #Courier queda lindo
    textbox.pack(pady=20)

    df=ver_partidos()  #Guarda el contenido del excel en el df
    textbox.insert("end", df.to_string(index=False))   #Inserta en el final sin indices
    textbox.configure(state="disabled") #Sin esto el usuario puede modificar

    ctk.CTkButton(
        ventana_partidos,
        text="Volver",
        width=200,
        fg_color="transparent",
        border_width=1,
        command=ventana_partidos.destroy
    ).pack()

    ventana_partidos.grab_set()





def abrir_configuracion():
    ventana_config=ctk.CTkToplevel(ventana) #crea una ventana secundaria encima de la principal
    ventana_config.title("Configuración del Torneo")
    ventana_config.geometry("600x520")
    ventana_config.resizable(False, False)  #cambiar la resolucion se me bugea desde linux
    
    construir_header(ventana_config, "Configuración del Torneo")

    #marco para botones
    frame_config = ctk.CTkFrame(ventana_config, fg_color="transparent")
    frame_config.pack(expand=True)

    cerrada=configuracion_cerrada()  #verifica si la configuracion esta cerrada o no

    if cerrada:    #dependiendo si esta o no cerrada, los botones de configuracion se habilitan o deshabilitan
        estado="disabled"
    else:
        estado="normal"


    opciones_config=[
        ("Ingresar Equipo", abrir_ingresar_equipo),   #cada tupla tiene el nombre y la funcion que ejecuta
        ("Ingresar Partido", abrir_ingresar_partido),
        ("Ver Equipos", abrir_ver_equipos),
        ("Ver Partidos", abrir_ver_partidos)  
    ]
    #El boton volver lo puse aparte porque cuando cierre la configuracion desabilitare todos los botones

    for texto, comando in opciones_config:    #Esto es solo para crear los botones
        ctk.CTkButton(
            frame_config,
            text=texto,
            width=300,
            height=44,
            font=ctk.CTkFont(size=13),
            command=comando,   #para darle click y ejecutar la funcion
            state=estado  #si esta cerrada la config no funcionaran los botones
        ).pack(pady=7)

    ctk.CTkButton(
        frame_config,
        text="Volver",
        width=300,
        height=44,
        font=ctk.CTkFont(size=13),
        fg_color="transparent",
        border_width=1,
        command=ventana_config.destroy   #boton volver, destroy cierra solo esta ventana
    ).pack(pady=7)

    if not cerrada:
        def cerrar():
            cerrar_configuracion()   #cambio el txt a cerrado
            ventana_config.destroy()  #estas 2 lineas refrescan la ventana (la reinician), actualiando el estado
            abrir_configuracion()
        
        ctk.CTkButton(
            frame_config,
            text="Cerrar Configuración",  #el boton solo aparece si no se cerro
            width=300,
            height=44,
            font=ctk.CTkFont(size=13),
            fg_color="#e94560",
            command=cerrar
        ).pack(pady=7)
    else:
        ctk.CTkLabel(   #si ce cerro la config aparece este mensaje al reiniciarse automaticamente la ventana
            frame_config,
            text="La configuracion esta cerrada, no se pueden realizar cambios",
            text_color="#e94560",
            font=ctk.CTkFont(size=12)
        ).pack(pady=7)

        ctk.CTkLabel(   #Y tambien este mensaje
        frame_config,
        text="Reinicie la aplicacion para habilitar Registro de Resultados",
        text_color="#04ea23",
        font=ctk.CTkFont(size=11)
    ).pack()

    

    ventana_config.grab_set()  #bloquea la ventana principal mientras esta abierto configuracion





def abrir_resultados():
    ventana_res=ctk.CTkToplevel(ventana)
    ventana_res.title("Registro de Resultados")
    ventana_res.geometry("600x700")
    ventana_res.resizable(False, False)

    construir_header(ventana_res, "Registrar resultados")

    frame_form=ctk.CTkFrame(ventana_res, fg_color="transparent")
    frame_form.pack(padx=40, pady=20, fill="x")

    partidos_disponibles=[None]   #la lista funciona como una variable global, puede ser modificada por las funciones

    def actualizar_lista():
        fase=fase_actual()
        df=partidos_sin_resultado(fase)
        partidos_disponibles[0]=df

        if len(df)==0:
            selector_partido.configure(values=["No hay partidos disponibles"])  #hace que sea la unica opcion disponible en el mini menu
            selector_partido.set("No hay partidos disponibles")   #selecciona esa opcion
            return
        
        opciones=[]   #aca se guardaran los str departidos disponibles
        for i in range(len(df)):
            fila=df.iloc[i]
            pais1=obtener_pais(fila["equipo1"])
            pais2=obtener_pais(fila["equipo2"])
            opciones.append(f"{fila['fecha']} {fila['hora']} - {pais1} vs {pais2}")

        selector_partido.configure(values=opciones)
        selector_partido.set(opciones[0])  #selecciona el primer partido automaticamente
    
    fase=fase_actual()

    if fase=="Torneo finalizado":
        ctk.CTkLabel(frame_form, text="El torneo ha finalizado",
                     text_color="#44bb77", font=ctk.CTkFont(size=13)).pack(pady=10)
    else:   #Muestra la fase actual y el selector de partidos disponibles
        ctk.CTkLabel(frame_form, text=f"Fase actual: {fase}", text_color="#ffffff", font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(0,10))
        
        ctk.CTkLabel(frame_form, text="Partido", anchor="w").pack(fill="x", pady=(4, 2))
        selector_partido=ctk.CTkOptionMenu(frame_form, values=[""], width=340)
        selector_partido.pack()
    

    #campos de goles, deshabilitado hasta encontrar el partido 
    campos_goles=["Goles Equipo 1", "Goles Equipo 2", "Penales Equipo 1", "Penales Equipo 2"]
    entradas={}

    for campo in campos_goles:
        ctk.CTkLabel(frame_form, text=campo, anchor="w").pack(fill="x", pady=(4,2))
        entrada=ctk.CTkEntry(frame_form, width=340)
        entrada.pack()
        entradas[campo]=entrada


    label_mensaje=ctk.CTkLabel(ventana_res, text="", text_color="#aaaaaa")
    label_mensaje.pack(pady=(6,2))  #mensaje donde avisara si hubo error o si se registro correctamente


    def guardar():
        df=partidos_disponibles[0]
        
        if df is None or len(df)==0:  
            label_mensaje.configure(text="No hay partidos disponibles para esta fase", text_color="#e94560")
            return

        #parece kilombo pero es chill

        seleccion=selector_partido.get()  #obtiene el partido selecionado en el mini menu
        opciones=selector_partido.cget("values")   #cget obtiene una tupla con todas las opciones del minimenu
        indice_seleccion=list(opciones).index(seleccion)   #convierte la tupla a lista para usar index, obteniendo su indice en el mini menu
        fila=df.iloc[indice_seleccion]   #con el indice, puede acceder a la fila del dataframe del partido
        indice=fila.name    #y finalmente con name, obtiene el indice real, el que esta en el excel, para poder modificarlo


        g1=entradas["Goles Equipo 1"].get().strip()
        g2=entradas["Goles Equipo 2"].get().strip()
        pen1=entradas["Penales Equipo 1"].get().strip()
        pen2=entradas["Penales Equipo 2"].get().strip()

        if g1=="" or g2=="" or pen1=="" or pen2=="":
            label_mensaje.configure(text="Completa todos los campos", text_color="#e94560")
            return

        if not g1.isdigit() or not g2.isdigit() or not pen1.isdigit() or not pen2.isdigit():
            label_mensaje.configure(text="Deben ser numeros los goles y penales", text_color="#e94560")
            return

        registrar_resultado(indice, int(g1), int(g2), int(pen1), int(pen2))
        label_mensaje.configure(text="Resultado registrado correctamente.", text_color="#44bb77")

        for entry in entradas.values():
            entry.delete(0, "end")

        actualizar_lista()   #quita el partido que se acaba de ingresar de la lista de partidos disponibles
        refrescar_botones()   #si ya se ingresaron todos los de la fase, se habilita el boton para la siguiente fase


    ctk.CTkButton(
        ventana_res,
        text="Guardar Resultado",
        width=200,
        command=guardar
    ).pack(pady=2)

    ctk.CTkButton(
        ventana_res,
        text="Volver",
        width=200,
        fg_color="transparent",
        border_width=1,
        command=ventana_res.destroy
    ).pack(pady=4)
    
    actualizar_lista()  #para que al abrir la ventana ya aparezcan los partidos disponibles

    frame_botones=ctk.CTkFrame(ventana_res, fg_color="transparent")
    frame_botones.pack()
    

    def refrescar_botones():
        for widget in frame_botones.winfo_children():   #winfo_children devuelve una lista con todos los widgets, en este caso botones, que estan en ese frame
            widget.destroy()   #elimina los botones para que no se acumulen

        print(f"grupos_completos: {grupos_completos()}")
        print(f"hay_partidos_de_fase Dieciseisavos: {hay_partidos_de_fase('Dieciseisavos')}")

        if grupos_completos() and not hay_partidos_de_fase("Dieciseisavos"):
            ctk.CTkButton(frame_botones, text="Asignar equipos - Dieciseisavos", width=200,
                fg_color="#44bb77", command=gen_dieciseisavos).pack(pady=1)

        if ronda_completa("Dieciseisavos") and not hay_partidos_de_fase("Octavos"):
            ctk.CTkButton(frame_botones, text="Asignar equipos - Octavos", width=200,
                fg_color="#44bb77", command=gen_octavos).pack(pady=1)

        if ronda_completa("Octavos") and not hay_partidos_de_fase("Cuartos"):
            ctk.CTkButton(frame_botones, text="Asignar equipos - Cuartos", width=200,
                fg_color="#44bb77", command=gen_cuartos).pack(pady=1)

        if ronda_completa("Cuartos") and not hay_partidos_de_fase("Semifinal"):
            ctk.CTkButton(frame_botones, text="Asignar equipos - Semifinal", width=200,
                fg_color="#44bb77", command=gen_semifinal).pack(pady=1)

        if ronda_completa("Semifinal") and not hay_partidos_de_fase("Final"):
            ctk.CTkButton(frame_botones, text="Asignar equipos - Final y Tercer Puesto", width=200,
                fg_color="#44bb77", command=gen_final).pack(pady=1)



    def ejecutar_y_refrescar(funcion):   #ejecuta la funcion y refresca las opciones de botones y la lista de partidos
        funcion()
        refrescar_botones()
        actualizar_lista()  #para que se actualice la lista de partidos disponibles una vez que cambia de fase

    #cada funcion asigna los encuentros de los equipos para esa fase y actualiza la ventana
    def gen_dieciseisavos():
        ejecutar_y_refrescar(generar_dieciseisavos)

    def gen_octavos():
        ejecutar_y_refrescar(generar_octavos)

    def gen_cuartos():
        ejecutar_y_refrescar(generar_cuartos)

    def gen_semifinal():
        ejecutar_y_refrescar(generar_semifinal)

    def gen_final():
        ejecutar_y_refrescar(generar_final)

    
    refrescar_botones()  #esto es para que al abrir la ventana aparezcan los botones correspondientes        
    ventana_res.grab_set()


    



def abrir_informes():
    ventana_informes=ctk.CTkToplevel(ventana)   #Igual que abrir configuracion
    ventana_informes.title("Emision de Informes")
    ventana_informes.geometry("600x600")
    ventana_informes.resizable(False, False)

    construir_header(ventana_informes, "Emision de informes")

    frame_informes = ctk.CTkFrame(ventana_informes, fg_color="transparent")
    frame_informes.pack(expand=True)

    opciones_informes = [
        ("Partidos por fecha", abrir_informe1),
        ("Tabla de posiciones por grupo", abrir_informe2),
        ("Resultados por equipo", abrir_informe3),
        ("Proximo partido por equipo", abrir_informe4),
        ("Tabla de todos los grupos",abrir_informe5)
    ]

    for texto, comando in opciones_informes:
        ctk.CTkButton(
            frame_informes,
            text=texto,
            width=320,
            height=44,
            font=ctk.CTkFont(size=13),
            command=comando
        ).pack(pady=7)


    if fase_actual()=="Torneo finalizado":   #lo pongo aparte para que aparezca solo si el torneo termino
        ctk.CTkButton(
            frame_informes,
            text="Resumen del Torneo",
            width=320,
            height=44,
            font=ctk.CTkFont(size=13),
            command=abrir_resumen
        ).pack(pady=7)


    ctk.CTkButton(
        ventana_informes,
        text="Volver",
        width=150,
        fg_color="transparent",
        border_width=1,
        command=ventana_informes.destroy
    ).pack(pady=7)

    ventana_informes.grab_set()




def abrir_informe1():
    ventana_inf1=ctk.CTkToplevel(ventana)
    ventana_inf1.title("Partidos por fecha")
    ventana_inf1.geometry("600x600")
    ventana_inf1.resizable(False, False)

    construir_header(ventana_inf1,"Partidos por fecha")

    frame_input=ctk.CTkFrame(ventana_inf1, fg_color="transparent")
    frame_input.pack(pady=20)

    ctk.CTkLabel(
        frame_input,
        text="Fecha (DD/MM/AAAA):",
    ).pack(side="left", padx=(0, 10))  #side="left" pone la etiqueta a la izquierda del cuadro entry

    entrada_fecha=ctk.CTkEntry(frame_input, width=150)
    entrada_fecha.pack(side="left")  #el entry queda a la derecha del label

    #cuadro donde se muestran los resultados
    textbox=ctk.CTkTextbox(ventana_inf1, width=540, height=280, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=(0, 10))
    textbox.configure(state="disabled") #Para que el usuario no toque nada

    def buscar():
        fecha=entrada_fecha.get().strip()  #Lee lo que se escribe en el cuadro
        if fecha=="":
            return

        df=informe_partidos_por_fecha(fecha)   #guarda el dataframe donde aparecen los partidos en esa fecha

        textbox.configure(state="normal")   #habilitamos para poder escribir, esto dura milisegundos, el usuario no puede hacer nada en ese tiempo
        textbox.delete("1.0", "end")        #borramos el contenido anterior

        if len(df)==0:
            textbox.insert("end", f"No hay partidos para la fecha {fecha}")
        else:
            textbox.insert("end", f"Partidos del {fecha}\n")   
            textbox.insert("end", "─" * 50 + "\n\n")

            for i in range(len(df)):
                fila=df.iloc[i]   #Va recorriendo el df por filas
                pais1=obtener_pais(fila['equipo1'])   #busca el pais que tiene el id del equipo
                pais2=obtener_pais(fila['equipo2'])
                textbox.insert("end", f"{fila['hora']} hs — {fila['lugar']}\n") #Inserta dentro del cuadro de texto (Imprime)
                
                textbox.insert("end", f"  {pais1}  {int(fila['goles1'])} : {int(fila['goles2'])}  {pais2}\n")
                textbox.insert("end", f"  Fase: {fila['fase']}\n\n")

        textbox.configure(state="disabled")  #deshabilitamos para que no se pueda editar por el usuario

    ctk.CTkButton(
        ventana_inf1,
        text="Buscar",
        width=150,
        command=buscar
    ).pack(pady=(0, 8))

    ctk.CTkButton(
        ventana_inf1,
        text="Volver",
        width=150,
        fg_color="transparent",
        border_width=1,
        command=ventana_inf1.destroy
    ).pack()

    ventana_inf1.grab_set()



def abrir_informe2():
    ventana_inf2 = ctk.CTkToplevel(ventana)
    ventana_inf2.title("Tabla de posiciones por grupo")
    ventana_inf2.geometry("600x600")
    ventana_inf2.resizable(False, False)

    construir_header(ventana_inf2, "Tabla de posiciones por grupo")

    frame_input=ctk.CTkFrame(ventana_inf2, fg_color="transparent")
    frame_input.pack(pady=20)

    ctk.CTkLabel(
        frame_input,
        text="Grupo (ej: A):",
    ).pack(side="left", padx=(0, 10))

    entrada_grupo=ctk.CTkEntry(frame_input, width=80)
    entrada_grupo.pack(side="left")

    textbox=ctk.CTkTextbox(ventana_inf2, width=540, height=280, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=(0, 10))
    textbox.configure(state="disabled")

    def buscar():
        grupo=entrada_grupo.get().strip()

        if grupo=="":
            return

        df=informe_tabla_grupo(grupo)

        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        if df is None:
            textbox.insert("end", f"No existe el grupo {grupo.upper()}")
        else:
            textbox.insert("end", f"Grupo {grupo.upper()}\n")
            textbox.insert("end", "─" * 55 + "\n")
            textbox.insert("end", f"{'POS':<5} {'PAIS':<20} {'PJ':<5} {'GF':<5} {'GC':<5} {'DG':<5} {'PTS':<5}\n")
            textbox.insert("end", "─" * 55 + "\n")

            for i in range(len(df)):
                fila = df.iloc[i]
                textbox.insert("end", f"{i+1:<5} {str(fila['pais']):<20} {int(fila['pj']):<5} {int(fila['gf']):<5} {int(fila['gc']):<5} {int(fila['dg']):<5} {int(fila['puntos']):<5}\n")

        textbox.configure(state="disabled")

    ctk.CTkButton(
        ventana_inf2,
        text="Buscar",
        width=150,
        command=buscar
    ).pack(pady=(0, 8))

    ctk.CTkButton(
        ventana_inf2,
        text="Volver",
        width=150,
        fg_color="transparent",
        border_width=1,
        command=ventana_inf2.destroy
    ).pack()

    ventana_inf2.grab_set()





def abrir_informe3():
    ventana_inf3=ctk.CTkToplevel(ventana)
    ventana_inf3.title("Resultados por equipo")
    ventana_inf3.geometry("600x600")
    ventana_inf3.resizable(False, False)

    construir_header(ventana_inf3, "Resultados por equipo")

    frame_input=ctk.CTkFrame(ventana_inf3, fg_color="transparent")
    frame_input.pack(pady=20)

    ctk.CTkLabel(
        frame_input,
        text="Pais:",
    ).pack(side="left", padx=(0, 10))

    entrada_pais=ctk.CTkEntry(frame_input, width=150)
    entrada_pais.pack(side="left")

    textbox=ctk.CTkTextbox(ventana_inf3, width=540, height=280, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=(0, 10))
    textbox.configure(state="disabled")

    def buscar():
        pais_buscado=entrada_pais.get().strip()

        if pais_buscado=="":
            return

        df,avance=informe_resultados_equipo(pais_buscado)

        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        if df is None:
            textbox.insert("end", f"No existe el equipo {pais_buscado}")
        elif len(df)==0:
            textbox.insert("end", f"{pais_buscado.upper()} no tiene partidos registrados")
        else:
            textbox.insert("end", f"Resultados de {pais_buscado.upper()}\n")
            textbox.insert("end", "─"*50 + "\n\n")

            for i in range(len(df)):   #similar al informe 1
                fila=df.iloc[i]
                pais1=obtener_pais(fila["equipo1"])
                pais2=obtener_pais(fila["equipo2"])
                textbox.insert("end", f"{fila['fecha']} — {fila['fase']}\n")
                textbox.insert("end", f"  {pais1}  {int(fila['goles1'])} : {int(fila['goles2'])}  {pais2}\n")
                textbox.insert("end", f"  {fila['lugar']}\n\n")
            
            if avance=="Campeon":
                textbox.insert("end", "Campeon del Mundial\n")
            elif avance=="Vicecampeon":
                textbox.insert("end", "Vicecampeon del Mundial\n")
            elif avance=="Fase de Grupos":
                textbox.insert("end", "Maximo avance: Fase de Grupos\n")
            else:
                textbox.insert("end", f"Clasificado a {avance}\n")

        textbox.configure(state="disabled")

    ctk.CTkButton(
        ventana_inf3,
        text="Buscar",
        width=150,
        command=buscar
    ).pack(pady=(0, 8))

    ctk.CTkButton(
        ventana_inf3,
        text="Volver",
        width=150,
        fg_color="transparent",
        border_width=1,
        command=ventana_inf3.destroy
    ).pack()

    ventana_inf3.grab_set()




def abrir_informe4():
    ventana_inf4 = ctk.CTkToplevel(ventana)
    ventana_inf4.title("Proximo partido")
    ventana_inf4.geometry("600x600")
    ventana_inf4.resizable(False, False)

    construir_header(ventana_inf4, "Proximo partido")

    frame_input = ctk.CTkFrame(ventana_inf4, fg_color="transparent")
    frame_input.pack(pady=20)

    #pide el pais
    ctk.CTkLabel(frame_input, text="Pais:").grid(row=0, column=0, padx=(0, 10), pady=6)
    entrada_pais = ctk.CTkEntry(frame_input, width=150)         #grid es similar a pack pero maneja filas y columnas
    entrada_pais.grid(row=0, column=1)

    #pide la fecha
    ctk.CTkLabel(frame_input, text="Fecha (DD/MM/AAAA):").grid(row=1, column=0, padx=(0, 10), pady=6)
    entrada_fecha = ctk.CTkEntry(frame_input, width=150)
    entrada_fecha.grid(row=1, column=1)

    textbox = ctk.CTkTextbox(ventana_inf4, width=540, height=240, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=(0, 10))
    textbox.configure(state="disabled")

    def buscar():
        pais_buscado  = entrada_pais.get().strip()
        fecha_buscada = entrada_fecha.get().strip()

        if pais_buscado == "" or fecha_buscada == "":
            return

        resultado=informe_proximo_partido(pais_buscado, fecha_buscada)

        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        if resultado is None:
            textbox.insert("end", f"No existe el equipo {pais_buscado}")

        else:
            pais1 = obtener_pais(resultado["equipo1"])
            pais2 = obtener_pais(resultado["equipo2"])
            textbox.insert("end", f"Próximo partido de {pais_buscado.upper()}\n")
            textbox.insert("end", "─" * 50 + "\n\n")
            textbox.insert("end", f"Fecha:  {resultado['fecha']}\n")
            textbox.insert("end", f"Hora:   {resultado['hora']}\n")
            textbox.insert("end", f"Lugar:  {resultado['lugar']}\n")
            textbox.insert("end", f"Fase:   {resultado['fase']}\n\n")
            textbox.insert("end", f"  {pais1}  vs  {pais2}\n\n")

        textbox.configure(state="disabled")

    ctk.CTkButton(
        ventana_inf4,
        text="Buscar",
        width=150,
        command=buscar
    ).pack(pady=(0, 8))

    ctk.CTkButton(
        ventana_inf4,
        text="Volver",
        width=150,
        fg_color="transparent",
        border_width=1,
        command=ventana_inf4.destroy
    ).pack()

    ventana_inf4.grab_set()






def abrir_informe5():
    ventana_inf5=ctk.CTkToplevel(ventana)
    ventana_inf5.title("Todos los grupos")
    ventana_inf5.geometry("600x600")
    ventana_inf5.resizable(False, False)

    construir_header(ventana_inf5, "Todos los grupos")

    textbox=ctk.CTkTextbox(ventana_inf5, width=540, height=360, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=20)

    grupos=informe_todos_los_grupos()

    encabezado=f"{'POS':<5} {'PAIS':<20} {'PJ':<5} {'GF':<5} {'GC':<5} {'DG':<5} {'PTS':<5}\n"

    for grupo in grupos:
        df=grupos[grupo]
        textbox.insert("end", f"Grupo {grupo}\n")
        textbox.insert("end", "─" * 57 + "\n")
        textbox.insert("end", encabezado)
        textbox.insert("end", "─" * 57 + "\n")

        for i in range(len(df)):
            fila = df.iloc[i]
            textbox.insert("end", f"{i+1:<5} {str(fila['pais']):<20} {int(fila['pj']):<5} {int(fila['gf']):<5} {int(fila['gc']):<5} {int(fila['dg']):<5} {int(fila['puntos']):<5}\n")

        textbox.insert("end", "\n")  #espacio entre grupos

    textbox.configure(state="disabled")

    ctk.CTkButton(
        ventana_inf5,
        text="Volver",
        width=150,
        fg_color="transparent",
        border_width=1,
        command=ventana_inf5.destroy
    ).pack()

    ventana_inf5.grab_set()



def abrir_resumen():
    ventana_res2=ctk.CTkToplevel(ventana)
    ventana_res2.title("Resumen del Torneo")
    ventana_res2.geometry("600x600")
    ventana_res2.resizable(False, False)

    construir_header(ventana_res2, "Resumen del Torneo")
    
    textbox=ctk.CTkTextbox(ventana_res2, width=540, height=400, font=ctk.CTkFont(family="Courier", size=12))
    textbox.pack(pady=20)    #la funete courier es linda

    textbox.insert("end", generar_resumen())
    textbox.configure(state="disabled")

    ctk.CTkButton(ventana_res2, text="Volver", width=150, fg_color="transparent",
        border_width=1, command=ventana_res2.destroy).pack()

    ventana_res2.grab_set()






#Configuracion global de ctk para el programa
ctk.set_appearance_mode("dark") #Modo oscuro
ctk.set_default_color_theme("blue") #Botones azules


#La primera ventana que contendra al menu principal
ventana=ctk.CTk() #Crea la ventana
ventana.title("Copa Mundial FIFA 2026")
ventana.geometry("700x500")

construir_header(ventana, "MENU PRINCIPAL")


#Menu principal
frame_menu = ctk.CTkFrame(ventana, fg_color="transparent")
frame_menu.pack(expand=True)


cerrada=configuracion_cerrada()   #retorna true o false si esta o no cerrada la configuracion

#cada tupla tiene el texto del boton y la funcion que ejecuta
opciones=[
    ("Configuracion del Torneo", abrir_configuracion, "normal"),
    ("Registro de Resultados", abrir_resultados, "normal" if cerrada else "disabled"),
    ("Emision de Informes", abrir_informes, "normal"),
    ("Salir", ventana.quit, "normal"),
]

for texto, comando, estado in opciones:   #Se crean los botones
    ctk.CTkButton(
        frame_menu,
        text=texto,
        width=320, #ancho del boton en pixeles
        height=48, #alto del boton en pixeles
        font=ctk.CTkFont(size=14),
        command=comando,  #funcion que se ejecuta al hacer click
        state=estado
    ).pack(pady=8)  #8px de espacio entre cada boton



ventana.mainloop()