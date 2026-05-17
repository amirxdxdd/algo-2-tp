class Torneo:
    def __init__(self,nombre,fecha_ini,fecha_fin):
        self.nombre=nombre
        self.fecha_ini=fecha_ini
        self.fecha_fin=fecha_fin
class Equipo:
    def __init__(self,identificador,pais,abreviatura,prefifo,confederacion,grupo):
        self.identificador=identificador
        self.pais=pais
        self.abreviatura=abreviatura
        self.prefijo=prefifo
        self.confederacion=confederacion
        self.grupo=grupo
class Partido:
    def __init__(self,fecha,hora,lugar,id1,id2,goles1,goles2,goles_penales1,goles_penales2):
        self.fecha=fecha
        self.hora=hora
        self.lugar=lugar
        self.id1=id1
        self.id2=id2
        self.goles1=goles1
        self.goles2=goles2
        self.goles_penales1=goles_penales1
        self.goles_penales2=goles_penales2
