from PyQt5.QtCore import QObject, QThread, pyqtSignal
from time import time
import parametros as p
from random import randint, random


class ThreadDesaparecerObjetos(QThread):

    def __init__(self, senal_desaparecer_objeto_intra, dificultad, tipo_objeto, 
                rut_objeto, personaje, *args, **kwargs):
        # Podemos usar *args y **kwargs para pasar argumentos a Thread
        super().__init__(*args, **kwargs)
        self.senal_desaparecer_objeto_intra = senal_desaparecer_objeto_intra
        self.tipo_objeto = tipo_objeto
        self.dificultad = dificultad
        self.rut_objeto = rut_objeto
        self.personaje = personaje

    def run(self):
        tiempo = time()
        if self.dificultad == "intro":
            tiempo_a_sumar = p.TIEMPO_OBJETO_INTRO
        elif self.dificultad == "avanzada":
            tiempo_a_sumar = p.TIEMPO_OBJETO_AVANZADA
        if self.personaje == "lisa" and self.tipo_objeto == "objeto_normal":
            tiempo_a_sumar += p.PONDERADOR_TIEMPO_LISA
        while True:
            if time() > tiempo + tiempo_a_sumar:
                diccionario_desaparicion = {"tipo objeto": self.tipo_objeto, "rut objeto": self.rut_objeto}
                self.senal_desaparecer_objeto_intra.emit(diccionario_desaparicion)
                break
            else:
                continue

class ThreadAparecerObjetos(QThread):

    def __init__(self, diccionario_aparecer_o, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.senal_aparecer_objeto_intra = diccionario_aparecer_o["senal"]
        self.pos_personaje_x = diccionario_aparecer_o["posicion personaje x"]
        self.pos_personaje_y = diccionario_aparecer_o["posicion personaje y"]
        self.personaje = diccionario_aparecer_o["personaje"]
        self.posi_o_normales = diccionario_aparecer_o["posiciones normales"]
        self.posi_obstaculos = diccionario_aparecer_o["posiciones obstaculos"]
        self.posi_o_buenos_cora = diccionario_aparecer_o["posiciones corazones"]
        self.posi_o_buenos_X2 = diccionario_aparecer_o["posiciones x2"]
        self.posi_peligrosos = diccionario_aparecer_o["posiciones peligrosos"]
    
    def generar_tuplas_objetos_obstaculos(self):
        lista_tuplas = []
        for posicion in self.posi_o_normales.values():
            pos_x_o_normales = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_o_normales = [y for y in range(posicion[1], posicion[1] + 30)]
            tuplas = [(x,y) for x in pos_x_o_normales for y in pos_y_o_normales]
            lista_tuplas += tuplas
        for posicion in self.posi_o_buenos_cora.values():
            pos_x_corazones = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_corazones = [y for y in range(posicion[1], posicion[1] + 30)]
            tuplas = [(x,y) for x in pos_x_corazones for y in pos_y_corazones]
            lista_tuplas += tuplas
        for posicion in self.posi_o_buenos_X2.values():
            pos_x_X2 = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_X2 = [y for y in range(posicion[1], posicion[1] + 30)]
            tuplas = [(x,y) for x in pos_x_X2 for y in pos_y_X2]
            lista_tuplas += tuplas
        for posicion in self.posi_peligrosos.values():
            pos_x_peligrosos = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_peligrosos = [y for y in range(posicion[1], posicion[1] + 30)]
            tuplas = [(x,y) for x in pos_x_peligrosos for y in pos_y_peligrosos]
            lista_tuplas += tuplas
        for posicion in self.posi_obstaculos:
            pos_x_obstaculos = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_obstaculos = [y for y in range(posicion[1], posicion[1] + 30)]
            tuplas = [(x,y) for x in pos_x_obstaculos for y in pos_y_obstaculos]
            lista_tuplas += tuplas
        return lista_tuplas

    def run(self):
        posx_prohibidas = [x for x in range(self.pos_personaje_x, self.pos_personaje_x + 100)]
        posy_prohibidas = [y for y in range(self.pos_personaje_y, self.pos_personaje_y + 30)]
        tuplas_prohibidas_per = [(x,y) for x in posx_prohibidas for y in posy_prohibidas]
        resto_tuplas = self.generar_tuplas_objetos_obstaculos()
        pos_prohibidas = set(tuplas_prohibidas_per + resto_tuplas)
        while True:
            posx_o = randint(0, p.BORDE_VERTICAL_DER_J)
            posy_o = randint(p.BORDE_HORIZONTAL_UP_J, p.BORDE_HORIZONTAL_DOWN_J)
            vertices = [(posx_o, posy_o), (posx_o + 100, posy_o), (posx_o, posy_o + 30),
                (posx_o + 100, posy_o + 30)]
            if any(vertice in pos_prohibidas for vertice in vertices):
                continue
            else:
                pos_objeto = (posx_o, posy_o)
                break
        numero_azar = random()
        if numero_azar <= p.PROB_NORMAL:
            objeto = "objeto_normal"
            rut_objeto = "0"
        elif numero_azar > p.PROB_NORMAL and numero_azar <= p.PROB_BUENO + p.PROB_NORMAL:
            numero_azar_objeto_bueno = random()
            if numero_azar_objeto_bueno <= 0.5:
                objeto = "objeto_bueno1"
                rut_objeto = "1"
            else:
                objeto = "objeto_bueno2"
                rut_objeto = "2" 
        else:
            objeto = "objeto_peligroso"
            rut_objeto = "3"
        rut_objeto += str(randint(0,1000000))
        dic_obj = {"posicion objeto": pos_objeto, "tipo objeto": objeto, 
                   "personaje": self.personaje, "rut objeto": rut_objeto}
        self.senal_aparecer_objeto_intra.emit(dic_obj)

class PersonajeJuego(QObject):

    senal_chequear_cambio = pyqtSignal(dict)
    senal_revisar_local = pyqtSignal()
    senal_local_correcto = pyqtSignal(dict)
    senal_local_incorrecto = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.pos_x = 0
        self.pos_y = 0
        self.foto = 'ABAJO_1'
        self.personaje = None
        self.velocidad = 0

    def moverse(self, diccionario):
        direccion = diccionario["direccion"]
        posicion_inicial = (self.pos_x, self.pos_y)
        #Primero setea la foto que necesita y la posible posicion
        if direccion == 'left':
            if "IZQUIERDA" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'IZQUIERDA_1'
                else:
                    self.foto = 'IZQUIERDA_'+str(ultimo_digito + 1)
            else:
                self.foto = 'IZQUIERDA_1'
            self.pos_x -= self.velocidad
        if direccion == 'up':
            if "ARRIBA" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'ARRIBA_1'
                else:
                    self.foto = 'ARRIBA_'+str(ultimo_digito + 1)
            else:
                self.foto = 'ARRIBA_1'
            self.pos_y -= self.velocidad
        if direccion == 'right':
            if "DERECHA" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'DERECHA_1'
                else:
                    self.foto = 'DERECHA_'+str(ultimo_digito + 1)
            else:
                self.foto = 'DERECHA_1'
            self.pos_x += self.velocidad
        if direccion == 'down':
            if "ABAJO" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'ABAJO_1'
                else:
                    self.foto = 'ABAJO_'+str(ultimo_digito + 1)
            else:
                self.foto = 'ABAJO_1'
            self.pos_y += self.velocidad
        #Revisa si choca con algun borde
        if self.pos_x < p.BORDE_VERTICAL_IZQ_J:
            self.pos_x = p.BORDE_VERTICAL_IZQ_J
        if self.pos_x > p.BORDE_VERTICAL_DER_J:
            self.pos_x = p.BORDE_VERTICAL_DER_J
        if self.pos_y > p.BORDE_HORIZONTAL_DOWN_J:
            self.pos_y = p.BORDE_HORIZONTAL_DOWN_J
        if self.pos_y < p.BORDE_HORIZONTAL_UP_J:
            self.pos_y = p.BORDE_HORIZONTAL_UP_J
        #Envía señal a logica_juego para chequar si pasa algo en esa posicion
        diccionario_chequear_cambios = {"posible posicion": (self.pos_x, self.pos_y), 
        "foto": self.foto, "personaje": self.personaje, "antigua posicion": posicion_inicial}
        self.senal_chequear_cambio.emit(diccionario_chequear_cambios)

    def coordenadas_iniciales_personaje(self, diccionario):
        self.pos_x = diccionario["posicion x"]
        self.pos_y = diccionario['posicion y']
        self.personaje = diccionario["personaje"]
        if self.personaje == 'homero':
            self.velocidad = p.VELOCIDAD_HOMERO
        elif self.personaje == 'lisa':
            self.velocidad = p.VELOCIDAD_LISA
    
    def chocando_obstaculos(self, diccionario):
        pos_x, pos_y = diccionario["nueva posicion"]
        self.pos_x = pos_x
        self.pos_y = pos_y

class EnemigoJuego(QObject):

    senal_mover_enemigo_FE = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.pos_x = 0
        self.pos_y = 0
        self.foto = 'ABAJO_1'

    def mover_enemigo(self, siguiente_posicion):
        nueva_pos_x, nueva_pos_y = siguiente_posicion
        if nueva_pos_x > self.pos_x:
            direccion = "right"
        elif nueva_pos_x < self.pos_x:
            direccion = "left"
        elif nueva_pos_y > self.pos_y:
            direccion = "down"
        elif nueva_pos_y < self.pos_y:
            direccion = "up"
        if direccion == 'left':
            if "IZQUIERDA" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'IZQUIERDA_1'
                else:
                    self.foto = 'IZQUIERDA_'+str(ultimo_digito + 1)
            else:
                self.foto = 'IZQUIERDA_1'
        elif direccion == 'up':
            if "ARRIBA" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'ARRIBA_1'
                else:
                    self.foto = 'ARRIBA_'+str(ultimo_digito + 1)
            else:
                self.foto = 'ARRIBA_1'
        elif direccion == 'right':
            if "DERECHA" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'DERECHA_1'
                else:
                    self.foto = 'DERECHA_'+str(ultimo_digito + 1)
            else:
                self.foto = 'DERECHA_1'
        elif direccion == 'down':
            if "ABAJO" in self.foto:
                ultimo_digito = int(self.foto[-1])
                if ultimo_digito == 3: 
                    self.foto = 'ABAJO_1'
                else:
                    self.foto = 'ABAJO_'+str(ultimo_digito + 1)
            else:
                self.foto = 'ABAJO_1'
        self.pos_x = nueva_pos_x
        self.pos_y = nueva_pos_y
        diccionario_mover_enemigo = {"foto": self.foto, "nueva posicion": siguiente_posicion}
        self.senal_mover_enemigo_FE.emit(diccionario_mover_enemigo)
   
    def coordenadas_iniciales(self, coordenadas_iniciales_enemigo):
        self.pos_x, self.pos_y = coordenadas_iniciales_enemigo
