from PyQt5.QtCore import QObject, pyqtSignal
import parametros as p


class Preparacion(QObject):

    senal_mandar_data = pyqtSignal(dict)
    senal_comenzar_ronda = pyqtSignal(dict)
    senal_revisar_local = pyqtSignal(str)
    senal_info_ronda = pyqtSignal(dict)
    senal_local_incorrecto = pyqtSignal()
    senal_actualizar_vida_en_FE = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.pos_x = 0
        self.pos_y = 0
        self.personaje = None
        self.usuario = None
        self.rondas = 0
        self.puntaje = 0
        self.objetos_buenos = 0
        self.objetos_malos = 0
        self.vida = 1
        self.posicion_local = 0
        posiciones_locales = [range(355, 376), range(775, 795), range(590, 620), range(145, 186)]
        self.posiciones_locales = []
        for lista in posiciones_locales:
            for i in lista:
                self.posiciones_locales.append(i)
        self.senal_revisar_local.connect(self.revisar_local)
        self.senal_info_ronda.connect(self.data_ronda)

    def mandar_data_preparacion(self, usuario):
        self.usuario = usuario
        diccionario = {"vida": self.vida,
                       "Rondas" : self.rondas,
                       "Puntaje": self.puntaje,
                       "Objetos Buenos": self.objetos_buenos,
                       "Objetos Malos": self.objetos_malos}
        self.senal_mandar_data.emit(diccionario)

    def actualizar_data(self, diccionario_presentacion):
        self.rondas = diccionario_presentacion["numero rondas"]
        self.puntaje = diccionario_presentacion["puntaje"]
        self.objetos_buenos = diccionario_presentacion["items buenos"]
        self.objetos_malos = diccionario_presentacion["items malos"]
        self.vida = diccionario_presentacion["vida"]
        pass

    def data_ronda(self, diccionario_ronda):
        diccionario_ronda['numero rondas'] = self.rondas
        diccionario_ronda['vida'] = self.vida
        diccionario_ronda['puntaje'] = self.puntaje
        diccionario_ronda['objetos malos'] = self.objetos_malos
        diccionario_ronda['objetos buenos'] = self.objetos_buenos
        diccionario_ronda['usuario'] = self.usuario
        self.senal_comenzar_ronda.emit(diccionario_ronda)

    def revisar_local(self, dificultad):
        if self.pos_x in self.posicion_local:
            diccionario_juego = {"personaje": self.personaje, "dificultad": dificultad}
            self.senal_info_ronda.emit(diccionario_juego)
        else:
            self.senal_local_incorrecto.emit()

    def cheatcode_vida(self):
        if self.vida + (p.VIDA_TRAMPA / 100) < 1:
            self.vida += (p.VIDA_TRAMPA / 100)
        else:
            self.vida = 1
        self.senal_actualizar_vida_en_FE.emit(self.vida)

    def data_inicial_personaje_pre(self, diccionario):
        self.pos_x = diccionario["posicion x"]
        self.pos_y = diccionario['posicion y']
        self.personaje = diccionario["personaje"]
        if self.personaje == 'homero':
            self.posicion_local = range(145,186)
        elif self.personaje == 'lisa':
            self.posicion_local = range(355,376)

    def cambiar_posicion(self, diccionario):
        pos_x, pos_y = diccionario["n_posicion"]
        self.pos_x = pos_x
        self.pos_y = pos_y
        
class PersonajePreparacion(QObject):

    senal_mandar_cambio = pyqtSignal(dict)
    senal_revisar_local = pyqtSignal(str)
    senal_info_ronda = pyqtSignal(dict)
    senal_local_incorrecto = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.pos_x = 0
        self.pos_y = 0
        self.foto = 'ABAJO_1'
        self.personaje = None
        self.velocidad = 0
        self.posicion_local = 0
        posiciones_locales = [range(355,376), range(770,795), range(585,610), range(145,186)]
        self.posiciones_locales = []
        for lista in posiciones_locales:
            for i in lista:
                self.posiciones_locales.append(i)

    def mover_personaje_pre(self, diccionario):
        direccion = diccionario["direccion"]
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
        if self.pos_x < p.BORDE_VERTICAL_IZQ_P:
            self.pos_x = p.BORDE_VERTICAL_IZQ_P
        if self.pos_x > p.BORDE_VERTICAL_DER_P:
            self.pos_x = p.BORDE_VERTICAL_DER_P
        if self.pos_y > p.BORDE_HORIZONTAL_DOWN_P:
            self.pos_y = p.BORDE_HORIZONTAL_DOWN_P
        if self.pos_y < p.BORDE_HORIZONTAL_UP_P and self.pos_x not in self.posiciones_locales:
            self.pos_y = p.BORDE_HORIZONTAL_UP_P
        elif self.pos_y < p.BORDE_HORIZONTAL_UP_P and self.pos_x in self.posiciones_locales:
            self.senal_revisar_local.emit(diccionario["dificultad"])
            if self.pos_y < p.BORDE_HORIZONTAL_UP_P - 30:
                self.pos_y = p.BORDE_HORIZONTAL_UP_P - 30
        self.senal_mandar_cambio.emit({"n_posicion": (self.pos_x, self.pos_y), "foto": self.foto})

    def coordenadas_iniciales(self, diccionario):
        self.pos_x = diccionario["posicion x"]
        self.pos_y = diccionario['posicion y']
        self.personaje = diccionario["personaje"]
        if self.personaje == 'homero':
            self.velocidad = p.VELOCIDAD_HOMERO
            self.posicion_local = range(145,186)
        elif self.personaje == 'lisa':
            self.velocidad = p.VELOCIDAD_LISA
            self.posicion_local = range(355,376)
