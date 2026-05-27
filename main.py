import customtkinter as ctk
from datetime import datetime

def actualizar_hora():
    ahora = datetime.now().strftime("%d/%m/%Y  %H:%M:%S") #Convierte a str la fecha y hora actual y guarda en ahora
    label_hora.configure(text=ahora)  #Cambia la etiqueta a lo que hay en ahora  
    ventana.after(1000, actualizar_hora)  #Actualiza 1 segundo despues



#Funciones para configuracion del torneo
def abrir_ingresar_equipo():
    print("Ingresar equipo")

def abrir_ingresar_partido():
    print("Ingresar partido")

def abrir_ver_equipos():
    print("Ver equipos")

def abrir_ver_partidos():
    print("Ver partidos")





def abrir_configuracion():
    ventana_config = ctk.CTkToplevel(ventana) #crea una ventana secundaria encima de la principal
    ventana_config.title("Configuración del Torneo")
    ventana_config.geometry("600x460")
    ventana_config.resizable(False, False)  #se me bugea en linux cambiar la resolucion de esta ventana, bloqueo para evitar
    ventana_config.grab_set()  #bloquea la ventana principal mientras esta abierto configuracion

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
        ("Ingresar Equipo",   abrir_ingresar_equipo),
        ("Ingresar Partido",  abrir_ingresar_partido),
        ("Ver Equipos",       abrir_ver_equipos),
        ("Ver Partidos",      abrir_ver_partidos),
        ("Volver",            ventana_config.destroy),  #destroy cierra solo esta ventana
    ]

    for texto, comando in opciones_config:
        ctk.CTkButton(
            frame_config,
            text=texto,
            width=300,
            height=44,
            font=ctk.CTkFont(size=13),
            command=comando
        ).pack(pady=7)



def abrir_resultados():
    print("Resultados")

def abrir_informes():
    print("Informes")



ctk.set_appearance_mode("dark") #Modo oscuro
ctk.set_default_color_theme("blue") #Botones azules

ventana = ctk.CTk() #Crea la ventana
ventana.title("Copa Mundial FIFA 2026")
ventana.geometry("700x500")

header = ctk.CTkFrame(ventana, corner_radius=0, fg_color="#1a1a2e")
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





#Menus, botones, etc
frame_menu = ctk.CTkFrame(ventana, fg_color="transparent")
frame_menu.pack(expand=True)

ctk.CTkLabel(
    frame_menu,
    text="MENÚ PRINCIPAL",
    font=ctk.CTkFont(size=14, weight="bold"),
    text_color="#cccccc"
).pack(pady=(0, 20))  #20 de px de espacio abajo, para separarlo de los botones

# Lista de tuplas, cada tupla tiene el texto del boton y la funcion que ejecuta
opciones = [
    ("Configuración del Torneo",  abrir_configuracion),
    ("Registro de Resultados",     abrir_resultados),
    ("Emisión de Informes",        abrir_informes),
    ("Salir",                      ventana.quit),
]

for texto, comando in opciones:
    ctk.CTkButton(
        frame_menu,
        text=texto,
        width=320, #ancho del boton en pixeles
        height=48, #alto del boton en pixeles
        font=ctk.CTkFont(size=14),
        command=comando  # funcion que se ejecuta al hacer click
    ).pack(pady=8)  # 8px de espacio entre cada boton



ventana.mainloop()