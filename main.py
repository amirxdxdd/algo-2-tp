import customtkinter as ctk
from datetime import datetime
from logica import *


def actualizar_hora():
    ahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S") #Convierte a str la fecha y hora actual y guarda en ahora
    label_hora.configure(text=ahora)  #Cambia la etiqueta a lo que hay en ahora  
    ventana.after(1000, actualizar_hora)  #Actualiza 1 segundo despues



#Funciones para configuracion del torneo
def abrir_ingresar_equipo():   #Todo igual a las otras ventanas
    ventana_equipo = ctk.CTkToplevel(ventana)   
    ventana_equipo.title("Ingresar Equipo")
    ventana_equipo.geometry("420x580")   #Esto debe tener este tamaño minimo para que aparezca el boton de guardar
    ventana_equipo.resizable(False, False)  #No se puede cambiar la resolucion
    

    header_equipo = ctk.CTkFrame(ventana_equipo, corner_radius=0, fg_color="#1a1a2e")
    header_equipo.pack(fill="x")

    ctk.CTkLabel(
        header_equipo,
        text="Ingresar Equipo",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

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
        ).pack(fill="x", pady=(8, 2))

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
    ).pack(pady=4)

    ctk.CTkButton(     #Boton para cancelar o regresar
        ventana_equipo,
        text="Volver",
        width=200,
        fg_color="transparent",     
        border_width=1,             
        command=ventana_equipo.destroy
    ).pack(pady=4)

    ventana_equipo.grab_set()  #No se puede usar la ventana anterior, tengo que ponerlo aca por problemas de linux hyperland



def abrir_ingresar_partido():
    ventana_partido=ctk.CTkToplevel(ventana)   #Igual al anterior
    ventana_partido.title("Ingresar Partido")
    ventana_partido.geometry("700x760")
    ventana_partido.resizable(False, False)

    header_partido=ctk.CTkFrame(ventana_partido, corner_radius=0, fg_color="#1a1a2e")
    header_partido.pack(fill="x")

    ctk.CTkLabel(
        header_partido,
        text="Ingresar Partido",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

    frame_form=ctk.CTkFrame(ventana_partido, fg_color="transparent")
    frame_form.pack(padx=40, pady=20, fill="x")

    campos = ["Fecha (DD/MM/AAAA)", "Hora (HH:MM)", "Lugar", "Equipo 1", "Equipo 2", "Goles Equipo 1", "Goles Equipo 2", "Penales Equipo 1", "Penales Equipo 2", "Fase"]
    entradas = {}

    for campo in campos:
        ctk.CTkLabel(
            frame_form,
            text=campo,
            anchor="w"
        ).pack(fill="x", pady=(1, 1))

        entrada = ctk.CTkEntry(frame_form, width=340)   #Cuadro para ingresar datos
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
        g1=entradas["Goles Equipo 1"].get().strip()
        g2=entradas["Goles Equipo 2"].get().strip()
        pen1=entradas["Penales Equipo 1"].get().strip()
        pen2=entradas["Penales Equipo 2"].get().strip()
        fase=entradas["Fase"].get().strip()

        #verificar que no hayan campos vacios
        if fecha=="" or hora=="" or lugar=="" or pais1=="" or pais2=="" or g1=="" or g2=="" or pen1=="" or pen2=="" or fase=="":
            label_mensaje.configure(text="Completa todos los campos.", text_color="#e94560")
            return

        #verificar que goles y penales sean numeros
        if not g1.isdigit() or not g2.isdigit() or not pen1.isdigit() or not pen2.isdigit():
            label_mensaje.configure(text="Goles y penales deben ser numeros.", text_color="#e94560")
            return

        #buscar el ID rapidin (No quiero hacer una funcion porque no volvere a usar esto)
        equipos=pd.read_excel("data/equipos.xlsx")
        eq1=equipos[equipos["pais"].str.upper()==pais1.upper()]
        eq2=equipos[equipos["pais"].str.upper()==pais2.upper()]

        if len(eq1)==0 or len(eq2)==0:
            label_mensaje.configure(text="Uno de los equipos no existe.", text_color="#e94560")
            return

        id_eq1=eq1.iloc[0]["id"]
        id_eq2=eq2.iloc[0]["id"]

        ingresar_partido(fecha, hora, lugar, id_eq1, id_eq2, int(g1), int(g2), int(pen1), int(pen2), fase)
        label_mensaje.configure(text="Partido guardado correctamente.", text_color="#44bb77")


    ctk.CTkButton(
        ventana_partido,
        text="Guardar Partido",
        width=200,
        command=guardar
    ).pack(pady=1)

    ctk.CTkButton(
        ventana_partido,
        text="Volver",
        width=200,
        fg_color="transparent",
        border_width=1,
        command=ventana_partido.destroy
    ).pack(pady=1)

    ventana_partido.grab_set()





def abrir_ver_equipos():
    ventana_equipos = ctk.CTkToplevel(ventana)  #Igual que todas las ventanas
    ventana_equipos.title("Ver Equipos")
    ventana_equipos.geometry("700x500")
    ventana_equipos.resizable(False, False)

    header_equipos = ctk.CTkFrame(ventana_equipos, corner_radius=0, fg_color="#1a1a2e")
    header_equipos.pack(fill="x")

    ctk.CTkLabel(
        header_equipos,
        text="Equipos",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

    #ctktextbox crea un cuadro de texto para guardar datos
    textbox = ctk.CTkTextbox(ventana_equipos, width=660, height=360, font=ctk.CTkFont(family="Courier", size=12))
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
    ventana_partidos.geometry("900x500")
    ventana_partidos.resizable(False, False)

    header_partidos=ctk.CTkFrame(ventana_partidos, corner_radius=0, fg_color="#1a1a2e")
    header_partidos.pack(fill="x")

    ctk.CTkLabel(
        header_partidos,
        text="Partidos",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

    textbox=ctk.CTkTextbox(ventana_partidos, width=860, height=360, font=ctk.CTkFont(family="Courier", size=12))   #Courier queda lindo
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
    ventana_config = ctk.CTkToplevel(ventana) #crea una ventana secundaria encima de la principal
    ventana_config.title("Configuración del Torneo")
    ventana_config.geometry("600x460")
    ventana_config.resizable(False, False)  #se me bugea en linux cambiar la resolucion de esta ventana, bloqueo para evitar
    
    
    #nuevo header, igual al menu principal
    header_config = ctk.CTkFrame(ventana_config, corner_radius=0, fg_color="#1a1a2e")
    header_config.pack(fill="x")

    ctk.CTkLabel(
        header_config,
        text="Configuración del Torneo",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

    #marco para botones
    frame_config = ctk.CTkFrame(ventana_config, fg_color="transparent")
    frame_config.pack(expand=True)

    opciones_config = [
        ("Ingresar Equipo", abrir_ingresar_equipo),   #cada tupla tiene el nombre y la funcion que ejecuta
        ("Ingresar Partido", abrir_ingresar_partido),
        ("Ver Equipos", abrir_ver_equipos),
        ("Ver Partidos", abrir_ver_partidos),
        ("Volver", ventana_config.destroy),  #destroy cierra solo esta ventana
    ]

    for texto, comando in opciones_config:    #Esto es solo para crear los botones
        ctk.CTkButton(
            frame_config,
            text=texto,
            width=300,
            height=44,
            font=ctk.CTkFont(size=13),
            command=comando   #para darle click y ejecutar la funcion
        ).pack(pady=7)

    ventana_config.grab_set()  #bloquea la ventana principal mientras esta abierto configuracion





def abrir_resultados():
    print("Resultados")






def abrir_informes():
    ventana_informes = ctk.CTkToplevel(ventana)   #Igual que abrir configuracion
    ventana_informes.title("Emisión de Informes")
    ventana_informes.geometry("600x460")
    ventana_informes.resizable(False, False)

    header_informes = ctk.CTkFrame(ventana_informes, corner_radius=0, fg_color="#1a1a2e")
    header_informes.pack(fill="x")

    ctk.CTkLabel(
        header_informes,
        text="Emisión de Informes",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

    frame_informes = ctk.CTkFrame(ventana_informes, fg_color="transparent")
    frame_informes.pack(expand=True)

    opciones_informes = [
        ("Partidos por fecha", abrir_informe1),
        ("Tabla de posiciones por grupo", abrir_informe2),
        ("Resultados por equipo", abrir_informe3),
        ("Proximo partido por equipo", abrir_informe4),
        ("Tabla de todos los grupos",abrir_informe5),
        ("Volver", ventana_informes.destroy),
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

    ventana_informes.grab_set()




def abrir_informe1():
    ventana_inf1=ctk.CTkToplevel(ventana)
    ventana_inf1.title("Partidos por fecha")
    ventana_inf1.geometry("600x500")
    ventana_inf1.resizable(False, False)

    header_inf1 = ctk.CTkFrame(ventana_inf1, corner_radius=0, fg_color="#1a1a2e")
    header_inf1.pack(fill="x")

    ctk.CTkLabel(
        header_inf1,
        text="Partidos por Fecha",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

    frame_input=ctk.CTkFrame(ventana_inf1, fg_color="transparent")
    frame_input.pack(pady=20)

    ctk.CTkLabel(
        frame_input,
        text="Fecha (DD/MM/AAAA):",
    ).pack(side="left", padx=(0, 10))  #side="left" pone la etiqueta a la izquierda del cuadro entry

    entrada_fecha = ctk.CTkEntry(frame_input, width=150)
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
                pais1 = obtener_pais(fila['equipo1'])   #busca el pais que tiene el id del equipo
                pais2 = obtener_pais(fila['equipo2'])

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
    ventana_inf2.geometry("600x500")
    ventana_inf2.resizable(False, False)

    header_inf2=ctk.CTkFrame(ventana_inf2, corner_radius=0, fg_color="#1a1a2e")
    header_inf2.pack(fill="x")

    ctk.CTkLabel(
        header_inf2,
        text="Tabla de Posiciones por Grupo",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

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
    ventana_inf3.geometry("600x500")
    ventana_inf3.resizable(False, False)

    header_inf3=ctk.CTkFrame(ventana_inf3, corner_radius=0, fg_color="#1a1a2e")
    header_inf3.pack(fill="x")

    ctk.CTkLabel(
        header_inf3,
        text="Resultados por Equipo",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

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

        df=informe_resultados_equipo(pais_buscado)

        textbox.configure(state="normal")
        textbox.delete("1.0", "end")

        if df is None:
            textbox.insert("end", f"No existe el equipo {pais_buscado}")
        elif len(df) == 0:
            textbox.insert("end", f"{pais_buscado.upper()} no tiene partidos registrados")
        else:
            textbox.insert("end", f"Resultados de {pais_buscado.upper()}\n")
            textbox.insert("end", "─"*50 + "\n\n")

            for i in range(len(df)):   #Igualito al informe 1
                fila=df.iloc[i]
                pais1=obtener_pais(fila["equipo1"])
                pais2=obtener_pais(fila["equipo2"])
                textbox.insert("end", f"{fila['fecha']} — {fila['fase']}\n")
                textbox.insert("end", f"  {pais1}  {int(fila['goles1'])} : {int(fila['goles2'])}  {pais2}\n")
                textbox.insert("end", f"  {fila['lugar']}\n\n")

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
    ventana_inf4.geometry("600x500")
    ventana_inf4.resizable(False, False)

    header_inf4 = ctk.CTkFrame(ventana_inf4, corner_radius=0, fg_color="#1a1a2e")
    header_inf4.pack(fill="x")

    ctk.CTkLabel(
        header_inf4,
        text="Proximo Partido por Equipo",
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="#e94560"
    ).pack(pady=14)

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
    print("Informe 5")







#Configuracion global de ctk para el programa
ctk.set_appearance_mode("dark") #Modo oscuro
ctk.set_default_color_theme("blue") #Botones azules


#La primera ventana que contendra al menu principal
ventana=ctk.CTk() #Crea la ventana
ventana.title("Copa Mundial FIFA 2026")
ventana.geometry("700x500")

header=ctk.CTkFrame(ventana, corner_radius=0, fg_color="#1a1a2e")
header.pack(fill="x")



#Titulos, fecha, materia, etc
ctk.CTkLabel(
    header,
    text="COPA MUNDIAL FIFA 2026",
    font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
    text_color="#e94560"
).pack(pady=(18, 2))

ctk.CTkLabel(
    header,
    text="Algoritmos y Estructuras de Datos II",
    font=ctk.CTkFont(size=11),
    text_color="#aaaaaa"
).pack(pady=(0, 2))

label_hora = ctk.CTkLabel(
    header,
    text="",
    font=ctk.CTkFont(size=11),
    text_color="#aaaaaa"
)
label_hora.pack(pady=(0, 14))
actualizar_hora()





#Menu principal
frame_menu = ctk.CTkFrame(ventana, fg_color="transparent")
frame_menu.pack(expand=True)

ctk.CTkLabel(
    frame_menu,
    text="MENU PRINCIPAL",
    font=ctk.CTkFont(size=14, weight="bold"),
    text_color="#cccccc"
).pack(pady=(0, 20))  #20 de px de espacio abajo, para separarlo de los botones

#cada tupla tiene el texto del boton y la funcion que ejecuta
opciones = [
    ("Configuracion del Torneo", abrir_configuracion),
    ("Registro de Resultados", abrir_resultados),
    ("Emision de Informes", abrir_informes),
    ("Salir", ventana.quit),
]

for texto, comando in opciones:   #Se crean los botones
    ctk.CTkButton(
        frame_menu,
        text=texto,
        width=320, #ancho del boton en pixeles
        height=48, #alto del boton en pixeles
        font=ctk.CTkFont(size=14),
        command=comando  #funcion que se ejecuta al hacer click
    ).pack(pady=8)  #8px de espacio entre cada boton



ventana.mainloop()