from PyQt5.QtCore import QObject, QTimer, pyqtSignal
import parametros as p
from random import randint
from .BE_ventana_juego2 import ThreadDesaparecerObjetos, ThreadAparecerObjetos

class Juego(QObject):

    senal_pos_todo_bien = pyqtSignal(dict)
    senal_bajar_un_sec = pyqtSignal()
    senal_enviar_obstaculos = pyqtSignal(dict)
    senal_aparecer_objeto = pyqtSignal(dict)
    senal_aparecer_objeto_intra = pyqtSignal(dict)
    senal_desaparecer_objeto_intra = pyqtSignal(dict)
    senal_desaparecer_objeto = pyqtSignal(str)
    senal_chocando_obstaculo = pyqtSignal(dict)
    senal_actualizar_data_FE = pyqtSignal(dict)
    senal_ventana_post_ronda = pyqtSignal(dict)
    senal_mover_enemigo = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.personaje = None
        self.dificultad = None
        self.usuario = None
        self.puntaje = 0
        self.items_buenos = 0
        self.items_malos = 0
        self.tiempo = 0
        self.vida = 1
        self.n_rondas = 0
        self.pos_personaje_x = 0
        self.pos_personaje_y = 0
        #estas listas/diccionarios contienen las posiciones de los objetos
        self.posi_o_normales = {}
        self.cantidad_donas_normales = 0
        self.posi_o_buenos_cora = {}
        self.posi_o_buenos_X2 = {}
        self.posi_peligrosos = {}
        self.posi_obstaculos = []
        #esta lista/set contiene las tuplas que no se pueden ocupar porque ahí están
        # los obstaculos
        self.tuplas_prohibidas_obstaculos = []
        self.posiciones_jugador = []
        self.cantidad_movimientos_enemigo = 0
        self.threads_desaparecer = {}
        self.threads_aparecer = []
        self.timer_tiempo = None
        self.senal_desaparecer_objeto_intra.connect(self.desaparecer_objeto)
        self.senal_aparecer_objeto_intra.connect(self.aparecer_objeto)

    def crear_timer_enemigo(self):
        self.timer_enemigo = QTimer(self)
        if self.dificultad == "avanzada":
            self.timer_enemigo.setInterval(1000 * p.TIEMPO_DELAY_AVANZADA)
        elif self.dificultad == "intro":
            self.timer_enemigo.setInterval(1000 * p.TIEMPO_DELAY_INTRO)
        self.timer_enemigo.timeout.connect(self.mostrarycomenzar_mover_enemigo)
        self.timer_enemigo.start()

    def mostrarycomenzar_mover_enemigo(self):
        self.timer_mover_enemigo = QTimer(self)
        if self.dificultad == "avanzada":
            self.timer_mover_enemigo.setInterval(p.TIEMPO_MOVIMIENTO_ENEMIGO_AVANZADA)
        elif self.dificultad == "intro":
            self.timer_mover_enemigo.setInterval(p.TIEMPO_MOVIMIENTO_ENEMIGO_INTRO)
        self.timer_mover_enemigo.timeout.connect(self.mover_enemigo)
        self.timer_mover_enemigo.start()
        #Detenemos el primer timer
        self.timer_enemigo.stop()

    def mover_enemigo(self):
        self.cantidad_movimientos_enemigo += 1
        try:
            siguiente_posicion_e = self.posiciones_jugador[self.cantidad_movimientos_enemigo - 1]
            if self.pos_personaje_x in range(siguiente_posicion_e[0] - 100, 
            siguiente_posicion_e[0] + 100) and self.pos_personaje_y in range(siguiente_posicion_e[1] 
                                                                - 30, siguiente_posicion_e[1] + 30):
                self.vida = 0
                self.ventana_post_ronda()
            else:
                self.senal_mover_enemigo.emit(siguiente_posicion_e)
        except IndexError:
            #Genera señal de colision, porque significa que no se ha movido desde que partió
            self.vida = 0
            self.ventana_post_ronda()

    def crear_timer_tiempo(self):
        self.timer_tiempo = QTimer(self)
        self.timer_tiempo.setInterval(1000)
        self.timer_tiempo.timeout.connect(self.bajar_un_sec)
        self.timer_tiempo.start()

    def crear_timer_objetos(self):
        self.timer_objetos = QTimer(self)
        if self.dificultad == "intro":
            self.timer_objetos.setInterval(p.APARICION_INTRO * 1000)
        elif self.dificultad == "avanzada":
            self.timer_objetos.setInterval(p.APARICION_AVANZADA * 1000)
        self.timer_objetos.timeout.connect(self.thread_aparecer_objeto)
        self.timer_objetos.start()

    def pausar_timers(self, accion):
        if accion == "pausar":
            self.timer_objetos.stop()
            self.timer_tiempo.stop()
            self.timer_mover_enemigo.stop()
            self.timer_enemigo.stop()
            for thread in self.threads_desaparecer.values():
                if thread.isRunning():
                    thread.exit()
        elif accion == "despausar":
            self.timer_objetos.start()
            self.timer_tiempo.start()
            self.timer_enemigo.start()
            self.timer_mover_enemigo.start()
            for thread in self.threads_desaparecer.items():
                if thread[0] in self.posi_o_buenos_cora or thread[0] in self.posi_o_buenos_X2 \
                or thread[0] in self.posi_o_normales or thread[0] in self.posi_peligrosos:
                    thread[1].start()

    def cheatcode_vida(self):
        if self.vida + (p.VIDA_TRAMPA / 100) < 1:
            self.vida += (p.VIDA_TRAMPA / 100)
        else:
            self.vida = 1
        self.actualizar_data_en_FE()

    def thread_aparecer_objeto(self):
        diccionario_thread = {"senal": self.senal_aparecer_objeto_intra, 
"posicion personaje x": self.pos_personaje_x, "posicion personaje y": self.pos_personaje_y,
"personaje": self.personaje, "posiciones obstaculos": self.posi_obstaculos, 
"posiciones normales": self.posi_o_normales, "posiciones corazones": self.posi_o_buenos_cora,
"posiciones x2": self.posi_o_buenos_X2, "posiciones peligrosos": self.posi_peligrosos}
        thread_aparecer_objeto = ThreadAparecerObjetos(diccionario_thread)
        thread_aparecer_objeto.start()
        self.threads_aparecer.append(thread_aparecer_objeto)
        pass

    def aparecer_objeto(self, dic_objeto):
        rut_objeto = dic_objeto["rut objeto"]
        tipo_objeto = dic_objeto["tipo objeto"]
        pos_objeto = dic_objeto["posicion objeto"]
        if tipo_objeto == "objeto_normal":
            self.posi_o_normales[rut_objeto] = (pos_objeto)
        elif tipo_objeto == "objeto_bueno1":
            self.posi_o_buenos_X2[rut_objeto] = (pos_objeto)
        elif tipo_objeto == "objeto_bueno2":
            self.posi_o_buenos_cora[rut_objeto] = (pos_objeto)
        elif tipo_objeto == "objeto_peligroso":
            self.posi_peligrosos[rut_objeto] = (pos_objeto)
        self.senal_aparecer_objeto.emit(dic_objeto)
        self.crear_thread_desaparecer_objeto(tipo_objeto, rut_objeto)

    def crear_thread_desaparecer_objeto(self, tipo_objeto, rut_objeto):
        thread_desaparecer_objeto = ThreadDesaparecerObjetos(self.senal_desaparecer_objeto_intra,
                                        self.dificultad, tipo_objeto, rut_objeto, self.personaje)
        self.threads_desaparecer[rut_objeto] = thread_desaparecer_objeto
        thread_desaparecer_objeto.start()
        pass

    def desaparecer_objeto(self, dic_objeto):
        tipo_objeto = dic_objeto["tipo objeto"]
        rut_objeto = dic_objeto["rut objeto"]
        try:
            if tipo_objeto == "objeto_normal":
                self.posi_o_normales.pop(rut_objeto)
            elif tipo_objeto == "objeto_bueno1":
                self.posi_o_buenos_X2.pop(rut_objeto)
            elif tipo_objeto == "objeto_bueno2":
                self.posi_o_buenos_cora.pop(rut_objeto)
            elif tipo_objeto == "objeto_peligroso":
                self.posi_peligrosos.pop(rut_objeto)
            self.senal_desaparecer_objeto.emit(rut_objeto)
        except KeyError:
            pass
    
    def ventana_post_ronda(self):
        #método para juntar info y enviar al usuario a la ventana post-ronda
        self.timer_objetos.stop()
        self.timer_tiempo.stop()
        try:
            self.timer_mover_enemigo.stop()
        except AttributeError:
            pass
        self.timer_enemigo.stop()
        dic_info_post_ronda = {"puntaje": self.puntaje, "vida": round(self.vida, 2), 
"numero rondas": self.n_rondas, "items buenos": self.items_buenos, "items malos": self.items_malos,
"usuario": self.usuario}
        self.senal_ventana_post_ronda.emit(dic_info_post_ronda)
        pass
    
    def bajar_un_sec(self):
        if self.tiempo > 0:
            self.tiempo -= 1
            self.senal_bajar_un_sec.emit()
        else:
            self.ventana_post_ronda()
            pass

    def data_inicio_ronda(self, diccionario):
        self.personaje = diccionario["personaje"]
        self.dificultad = diccionario["dificultad"]
        self.puntaje = diccionario["puntaje"]
        self.items_buenos = diccionario["objetos buenos"]
        self.items_malos = diccionario["objetos malos"]
        self.vida = diccionario["vida"]
        self.tiempo = diccionario["tiempo"]
        self.n_rondas = diccionario["numero rondas"] + 1
        self.pos_personaje_x = diccionario["posicion x"]
        self.pos_personaje_y = diccionario["posicion y"]
        self.personaje = diccionario["personaje"]
        self.usuario = diccionario["usuario"]
        self.posi_o_normales = {}
        self.cantidad_donas_normales = 0
        self.posi_o_buenos_cora = {}
        self.posi_o_buenos_X2 = {}
        self.posi_peligrosos = {}
        self.posi_obstaculos = []
        self.cantidad_donas_normales = 0
        self.cantidad_movimientos_enemigo = 0
        self.posiciones_jugador = []
        self.setear_obstaculos()
        self.crear_timer_tiempo()
        self.crear_timer_objetos()
        self.crear_timer_enemigo()
    
    def actualizar_data_en_FE(self):
        diccionario = {"puntaje": self.puntaje, "items buenos": self.items_buenos, "items malos": 
        self.items_malos, "vida": round(self.vida, 2)}
        self.senal_actualizar_data_FE.emit(diccionario)
        pass

    def setear_obstaculos(self):
        """
        La funcion va seteando las posiciones que no se pueden ocupar
        Después elige una al azar, y si es que no está en la lista de las que no se pueden ocupar
        la setea como la posicion del objeto. Si es que sí está en la lista, elige otra
        """
        self.posi_obstaculos = []
        self.tuplas_prohibidas_obstaculos = []
        posx_prohibidas = [x for x in range(self.pos_personaje_x - 200, self.pos_personaje_x + 200)]
        posy_prohibidas = [y for y in range(self.pos_personaje_y - 60, self.pos_personaje_y + 60)]
        pos_prohibidas1 = set([(x,y) for x in posx_prohibidas for y in posy_prohibidas])
        while True:
            posx_o_1 = randint(0, p.BORDE_VERTICAL_DER_J)
            posy_o_1 = randint(p.BORDE_HORIZONTAL_UP_J, p.BORDE_HORIZONTAL_DOWN_J)
            vertices = [(posx_o_1, posy_o_1), (posx_o_1 + 100, posy_o_1), (posx_o_1, posy_o_1 + 30),
                (posx_o_1 + 100, posy_o_1 + 30)]
            if any(vertice in pos_prohibidas1 for vertice in vertices):
                continue
            else:
                pos_o_1 = (posx_o_1, posy_o_1)
                break
        posx_prohibidas = [x for x in range(pos_o_1[0] - 200, pos_o_1[0] + 200)]
        posy_prohibidas = [y for y in range(pos_o_1[1] - 60, pos_o_1[1] + 60)]
        pos_prohibidas2 = set(list(pos_prohibidas1) + [(x,y) for x in posx_prohibidas for 
                                              y in posy_prohibidas])
        while True:
            posx_o_2 = randint(0, p.BORDE_VERTICAL_DER_J)
            posy_o_2 = randint(p.BORDE_HORIZONTAL_UP_J, p.BORDE_HORIZONTAL_DOWN_J)
            vertices = [(posx_o_2, posy_o_2), (posx_o_2 + 100, posy_o_2), (posx_o_2, posy_o_2 + 30),
                (posx_o_2 + 100, posy_o_2 + 30)]
            if any(vertice in pos_prohibidas2 for vertice in vertices):
                continue
            else:
                pos_o_2 = (posx_o_2, posy_o_2)
                break        
        posx_prohibidas = [x for x in range(pos_o_2[0] - 200, pos_o_2[0] + 200)]
        posy_prohibidas = [y for y in range(pos_o_2[1] - 60, pos_o_2[1] + 60)]
        pos_prohibidas3 = set(list(pos_prohibidas2) + [(x,y) for x in posx_prohibidas for y 
                                             in posy_prohibidas])
        while True:
            posx_o_3 = randint(0, p.BORDE_VERTICAL_DER_J)
            posy_o_3 = randint(p.BORDE_HORIZONTAL_UP_J, p.BORDE_HORIZONTAL_DOWN_J)
            vertices = [(posx_o_3, posy_o_3), (posx_o_3 + 100, posy_o_3), (posx_o_3, posy_o_3 + 30),
                (posx_o_3 + 100, posy_o_3 + 30)]
            if any(vertice in pos_prohibidas3 for vertice in vertices):
                continue
            else:
                pos_o_3 = (posx_o_3, posy_o_3)
                break        
        diccionario_obstaculos = {"obstaculo1": pos_o_1, "obstaculo2": pos_o_2, 
                                  "obstaculo3": pos_o_3, "personaje": self.personaje}
        self.posi_obstaculos.append(pos_o_1)
        self.posi_obstaculos.append(pos_o_2)
        self.posi_obstaculos.append(pos_o_3)
        self.crear_tuplas_prohibidas_obstaculos()
        self.senal_enviar_obstaculos.emit(diccionario_obstaculos)
    
    def crear_tuplas_prohibidas_obstaculos(self):
        for posicion in self.posi_obstaculos:
            pos_x_objeto = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_objeto = [y for y in range(posicion[1], posicion[1] + 30)]
            self.tuplas_prohibidas_obstaculos += [(x,y) for x in pos_x_objeto for y in pos_y_objeto]
        self.tuplas_prohibidas_obstaculos = set(self.tuplas_prohibidas_obstaculos)

    def chequear_cambio(self, diccionario):
        pos_x, pos_y = diccionario["posible posicion"]
        vertices = [(pos_x, pos_y), (pos_x + 100, pos_y), (pos_x, pos_y + 30),
        (pos_x + 100, pos_y + 30)]
#Primero debo crear los sets con tuplas para poder revisar si la posicion coincide con alguna tupla
        pos_objeto_normal = []
        pos_objeto_peligroso = []
        pos_objeto_bueno = []
        tipo_colision = None
        for posicion in self.posi_o_normales.values():
            pos_x_objeto = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_objeto = [y for y in range(posicion[1], posicion[1] + 30)]
            pos_objeto_normal += [(x,y) for x in pos_x_objeto for y in pos_y_objeto]
        for posicion in self.posi_o_buenos_cora.values():
            pos_x_objeto = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_objeto = [y for y in range(posicion[1], posicion[1] + 30)]
            pos_objeto_bueno += [(x,y) for x in pos_x_objeto for y in pos_y_objeto]     
        for posicion in self.posi_o_buenos_X2.values():
            pos_x_objeto = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_objeto = [y for y in range(posicion[1], posicion[1] + 30)]
            pos_objeto_bueno += [(x,y) for x in pos_x_objeto for y in pos_y_objeto]             
        for posicion in self.posi_peligrosos.values():
            pos_x_objeto = [x for x in range(posicion[0], posicion[0] + 100)]
            pos_y_objeto = [y for y in range(posicion[1], posicion[1] + 30)]
            pos_objeto_peligroso += [(x,y) for x in pos_x_objeto for y in pos_y_objeto] 
        if any(vertice in set(pos_objeto_normal) for vertice in vertices):
            self.items_buenos += 1
            self.puntaje += p.PUNTOS_OBJETO_NORMAL
            if self.personaje == "homero":
                self.cantidad_donas_normales += 1
                if self.cantidad_donas_normales == 10:
                    if self.vida + (p.PONDERADOR_VIDA_HOMERO / 100) > 1:
                        self.vida = 1
                    else:
                        self.vida += (p.PONDERADOR_VIDA_HOMERO / 100)
                    self.cantidad_donas_normales = 0
            for posicion in self.posi_o_normales.items():
                if posicion[1][0] - pos_x <= 100 and posicion[1][1] - pos_y <= 30:
                    rut_objeto_colision = posicion[0]
                    self.posi_o_normales.pop(rut_objeto_colision)
                    tipo_colision = "objeto normal"
                    break
        elif any(vertice in self.tuplas_prohibidas_obstaculos for vertice in vertices):
            tipo_colision = "obstaculo"
            posicion_antigua = diccionario["antigua posicion"]
            diccionario["nueva posicion"] = posicion_antigua
            self.senal_chocando_obstaculo.emit(diccionario)
            self.senal_pos_todo_bien.emit(diccionario)
        elif any(vertice in set(pos_objeto_bueno) for vertice in vertices):
            for posicion in self.posi_o_buenos_cora.items():
                if posicion[1][0] - pos_x <= 100 and posicion[1][1] - pos_y <= 30:
                    rut_objeto_colision = posicion[0]
                    self.items_buenos += 1
                    self.posi_o_buenos_cora.pop(rut_objeto_colision)
                    if self.vida + (p.PONDERADOR_CORAZON / 100) < 1:
                        self.vida += p.PONDERADOR_CORAZON / 100
                    else:
                        self.vida = 1
                    tipo_colision = "corazon"
                    break
            for posicion in self.posi_o_buenos_X2.items():
                if posicion[1][0] - pos_x <= 100 and posicion[1][1] - pos_y <= 30:
                    rut_objeto_colision = posicion[0]
                    self.items_buenos += 1
                    self.puntaje += 2 * p.PUNTOS_OBJETO_NORMAL
                    self.posi_o_buenos_X2.pop(rut_objeto_colision)
                    tipo_colision = "X2"
                    break
        elif any(vertice in set(pos_objeto_peligroso) for vertice in vertices):
            self.cantidad_donas_normales = 0
            for posicion in self.posi_peligrosos.items():
                if posicion[1][0] - pos_x <= 100 and posicion[1][1] - pos_y <= 30:
                    self.items_malos += 1
                    rut_objeto_colision = posicion[0]
                    self.posi_peligrosos.pop(rut_objeto_colision)
                    tipo_colision = "peligroso"
                    if self.vida - (p.PONDERADOR_VENENO / 100) > 0:
                        self.vida -= (p.PONDERADOR_VENENO / 100)
                    else:
                        self.vida = 0
                        self.ventana_post_ronda()
                    break
        else:
            diccionario["nueva posicion"] = (pos_x, pos_y)
            self.pos_personaje_x = pos_x
            self.pos_personaje_y = pos_y
            self.senal_pos_todo_bien.emit(diccionario)
        if tipo_colision != None:
            if tipo_colision != "obstaculo":
                self.actualizar_data_en_FE()
                diccionario["nueva posicion"] = (pos_x, pos_y)
                #desaparece el objeto con el que chocasts
                self.senal_desaparecer_objeto.emit(rut_objeto_colision)
                self.pos_personaje_x = pos_x
                self.pos_personaje_y = pos_y
                self.senal_pos_todo_bien.emit(diccionario)
        #Si es que cambia de posicion, agregarlo a la lista por la que se guiará el enemigo
        try:
            if self.posiciones_jugador[-1] != (self.pos_personaje_x, self.pos_personaje_y):
                self.posiciones_jugador.append((self.pos_personaje_x, self.pos_personaje_y))
        except IndexError:
            #Significa que está en el primer movimiento y que no hay nada en self.posiciones_jugador
            self.posiciones_jugador.append((self.pos_personaje_x, self.pos_personaje_y))