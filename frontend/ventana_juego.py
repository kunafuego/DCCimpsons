from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import parametros as p
import sys
from random import randint

window_name_main, base_class_main = uic.loadUiType(p.VENTANA_JUEGO)

class VentanaJuego(window_name_main, base_class_main):

    senal_teclas = pyqtSignal(dict)
    senal_coord_iniciales = pyqtSignal(dict)
    senal_data_inicial = pyqtSignal(dict)
    senal_pausar_juego = pyqtSignal(str)
    senal_cheatcode_vida = pyqtSignal()
    senal_cheatcode_ronda = pyqtSignal()
    senal_coordenandas_iniciales_enemigo = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap(p.LOGO_INICIO))
        self.logo.setScaledContents(True)
        self.label_pausado.setVisible(False)
        self.label_pausado.setStyleSheet("background-color: red")
        self.obstaculo_1 = QLabel(self)
        self.obstaculo_2 = QLabel(self)
        self.obstaculo_3 = QLabel(self)
        self.label_objeto = QLabel(self)
        self.label_personaje = QLabel(self)
        self.label_enemigo = QLabel(self)
        self.teclas_apretadas = []
        self.labels_objetos = {}
        self.boton_pausa.clicked.connect(self.pausar_juego)
        self.boton_salir.clicked.connect(self.salir_juego)
        self.pausado = False
    
    def pausar_juego(self):
        if self.pausado:
            self.senal_pausar_juego.emit("despausar")
            self.label_pausado.setVisible(False)
            self.pausado = False
        else:
            self.senal_pausar_juego.emit("pausar")
            self.label_pausado.setVisible(True)
            self.pausado = True
    
    def esconder_ventana_juego(self, diccionario):
        self.hide()

    def salir_juego(self):
        self.hide()
        sys.exit()

    def bajar_un_sec(self):            
        self.tiempo.display(self.tiempo.value() - 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.senal_teclas.emit({'direccion': 'up'})
        if event.key() == Qt.Key_D:
            self.senal_teclas.emit({'direccion': 'right'})
        if event.key() == Qt.Key_A:
            self.senal_teclas.emit({'direccion': 'left'})
        if event.key() == Qt.Key_S:
            self.senal_teclas.emit({'direccion': 'down'})
        if event.key() == Qt.Key_P:
            self.pausar_juego()
        self.teclas_apretadas.append(event.key())
        try:
            if self.teclas_apretadas[-1] == Qt.Key_D and self.teclas_apretadas[-2] == Qt.Key_I and \
            self.teclas_apretadas[-3] == Qt.Key_V:
                self.senal_cheatcode_vida.emit()
            if self.teclas_apretadas[-1] == Qt.Key_V and self.teclas_apretadas[-2] == Qt.Key_I and \
            self.teclas_apretadas[-3] == Qt.Key_N:
                self.senal_cheatcode_ronda.emit()
        except IndexError:
            pass

    def desaparecer_objeto(self, rut_objeto):
        """
        Hace desaparecer al primer objeto que entró a la lista de objetos
        """
        objeto_a_desaparecer = self.labels_objetos[rut_objeto]
        objeto_a_desaparecer.setVisible(False)
        self.labels_objetos.pop(rut_objeto)

    def mostrar_objeto(self, di_obj):
        rut_objeto = di_obj["rut objeto"]
        tipo_objeto = di_obj["tipo objeto"]
        pos_objeto = di_obj["posicion objeto"]
        personaje = di_obj["personaje"]
        self.label_objeto = QLabel(self)
        if tipo_objeto == "objeto_bueno2":
            self.label_objeto.setPixmap(QPixmap(p.CORAZON))
        elif tipo_objeto == "objeto_peligroso":
            self.label_objeto.setPixmap(QPixmap(p.VENENO))
        if personaje == "homero":
            if tipo_objeto == "objeto_normal":
                self.label_objeto.setPixmap(QPixmap(p.DONA))
            elif tipo_objeto == "objeto_bueno1":
                self.label_objeto.setPixmap(QPixmap(p.DONAX2))
        if personaje == "lisa":
            if tipo_objeto == "objeto_normal":
                self.label_objeto.setPixmap(QPixmap(p.SAXO))
            elif tipo_objeto == "objeto_bueno1":
                self.label_objeto.setPixmap(QPixmap(p.SAXOX2))
        self.label_objeto.setScaledContents(True)
        self.label_objeto.setGeometry(pos_objeto[0], pos_objeto[1], 100, 30)
        self.label_objeto.show()
        self.labels_objetos[rut_objeto] = self.label_objeto

    def mostrar_obstaculos (self, di_ob):
        width = self.label_personaje.width()
        height = self.label_personaje.height()
        if di_ob["personaje"] == "homero":
            self.obstaculo_1.setPixmap(QPixmap(p.P_N_OBSTACULO_1))
            self.obstaculo_2.setPixmap(QPixmap(p.P_N_OBSTACULO_2))
            self.obstaculo_3.setPixmap(QPixmap(p.P_N_OBSTACULO_3))
        elif di_ob["personaje"] == "lisa":
            self.obstaculo_1.setPixmap(QPixmap(p.PR_OBSTACULO_1))
            self.obstaculo_2.setPixmap(QPixmap(p.PR_OBSTACULO_2))
            self.obstaculo_3.setPixmap(QPixmap(p.PR_OBSTACULO_3)) 
        self.obstaculo_1.setScaledContents(True)
        self.obstaculo_2.setScaledContents(True)
        self.obstaculo_3.setScaledContents(True)
        self.obstaculo_1.setGeometry(di_ob["obstaculo1"][0], di_ob["obstaculo1"][1], width, height)
        self.obstaculo_2.setGeometry(di_ob["obstaculo2"][0], di_ob["obstaculo2"][1], width, height)
        self.obstaculo_3.setGeometry(di_ob["obstaculo3"][0], di_ob["obstaculo3"][1], width, height)
    
    def cambiar_pyf(self, diccionario):
        #Cambiamos la posicion y la foto según lo que dictó el BE
        pos_x, pos_y = diccionario["nueva posicion"]
        personaje = diccionario["personaje"]
        width = self.label_personaje.width()
        height = self.label_personaje.height()
        foto = diccionario["foto"]
        if personaje == 'homero':
            if foto == 'ABAJO_1':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_ABAJO_1))
            elif foto == 'ABAJO_2':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_ABAJO_2))
            elif foto == 'ABAJO_3':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_ABAJO_3))
            elif foto == 'DERECHA_1':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_DERECHA_1))
            elif foto == 'DERECHA_2':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_DERECHA_2))
            elif foto == 'DERECHA_3':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_DERECHA_3))
            elif foto == 'IZQUIERDA_1':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_IZQUIERDA_1))
            elif foto == 'IZQUIERDA_2':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_IZQUIERDA_2))
            elif foto == 'IZQUIERDA_3':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_IZQUIERDA_3))   
            elif foto == 'ARRIBA_1':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_ARRIBA_1))
            elif foto == 'ARRIBA_2':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_ARRIBA_2))
            elif foto == 'ARRIBA_3':
                self.label_personaje.setPixmap(QPixmap(p.HOMERO_ARRIBA_3)) 
        elif personaje == 'lisa':
            if foto == 'ABAJO_1':
                self.label_personaje.setPixmap(QPixmap(p.LISA_ABAJO_1))
            elif foto == 'ABAJO_2':
                self.label_personaje.setPixmap(QPixmap(p.LISA_ABAJO_2))
            elif foto == 'ABAJO_3':
                self.label_personaje.setPixmap(QPixmap(p.LISA_ABAJO_3))
            elif foto == 'DERECHA_1':
                self.label_personaje.setPixmap(QPixmap(p.LISA_DERECHA_1))
            elif foto == 'DERECHA_2':
                self.label_personaje.setPixmap(QPixmap(p.LISA_DERECHA_2))
            elif foto == 'DERECHA_3':
                self.label_personaje.setPixmap(QPixmap(p.LISA_DERECHA_3))
            elif foto == 'IZQUIERDA_1':
                self.label_personaje.setPixmap(QPixmap(p.LISA_IZQUIERDA_1))
            elif foto == 'IZQUIERDA_2':
                self.label_personaje.setPixmap(QPixmap(p.LISA_IZQUIERDA_2))
            elif foto == 'IZQUIERDA_3':
                self.label_personaje.setPixmap(QPixmap(p.LISA_IZQUIERDA_3))   
            elif foto == 'ARRIBA_1':
                self.label_personaje.setPixmap(QPixmap(p.LISA_ARRIBA_1))
            elif foto == 'ARRIBA_2':
                self.label_personaje.setPixmap(QPixmap(p.LISA_ARRIBA_2))
            elif foto == 'ARRIBA_3':
                self.label_personaje.setPixmap(QPixmap(p.LISA_ARRIBA_3)) 
        self.label_personaje.setScaledContents(True)
        self.label_personaje.setGeometry(pos_x, pos_y, width, height)

    def mostrar_juego(self, diccionario):
        #Ocupamos el diccionario de info para setar los labels de la ronda
        self.label_puntaje.setText(str(diccionario["puntaje"]))
        self.label_ronda.setText(str(diccionario["numero rondas"] + 1))
        self.barra_vida.setValue(int(float(diccionario["vida"] * 100)))
        self.label_items_buenos.setText(str(diccionario["objetos buenos"]))
        self.label_items_malos.setText(str(diccionario["objetos malos"]))
        dificultad = diccionario['dificultad']
        #Seteamos cuánto durará la ronda
        if dificultad == 'intro':
            self.tiempo.display(p.DURACION_INTRO)
            diccionario["tiempo"] = p.DURACION_INTRO
        elif dificultad == 'avanzada':
            self.tiempo.display(p.DURACION_AVANZADA)
            diccionario["tiempo"] = p.DURACION_AVANZADA
        self.posicionar_personajes(diccionario)
        self.show()
    
    def actualizar_data_FE(self, diccionario):
        self.label_puntaje.setText(str(diccionario["puntaje"]))
        nueva_vida = float(diccionario["vida"]) * 100 
        self.barra_vida.setValue(int(nueva_vida))
        if nueva_vida < 50:
            self.barra_vida.setStyleSheet("background-color: red")
        self.label_items_buenos.setText(str(diccionario["items buenos"]))
        self.label_items_malos.setText(str(diccionario["items malos"]))        
    
    def posicionar_personajes(self, diccionario):
        personaje = diccionario["personaje"]
        pos_x_jugador = randint(p.BORDE_VERTICAL_IZQ_J, p.BORDE_VERTICAL_DER_J)
        pos_y_jugador = randint(p.BORDE_HORIZONTAL_UP_J, p.BORDE_HORIZONTAL_DOWN_J)
        if personaje == 'homero':
            self.fondo.setPixmap(QPixmap(p.MAPA_PLANTA_NUCLEAR))
            self.fondo_arriba.setPixmap(QPixmap(p.MAPA_PLANTA_NUCLEAR_ARRIBA))
            self.label_personaje.setPixmap(QPixmap(p.HOMERO_ABAJO_1))
            self.label_personaje.move(pos_x_jugador, pos_y_jugador)
        elif personaje == 'lisa':
            self.fondo.setPixmap(QPixmap(p.MAPA_PRIMARIA))
            self.fondo_arriba.setPixmap(QPixmap(p.MAPA_PRIMARIA_ARRIBA))
            self.label_personaje.setPixmap(QPixmap(p.LISA_ABAJO_1))
            self.label_personaje.move(pos_x_jugador, pos_y_jugador)
        self.label_personaje.setScaledContents(True)
        self.fondo.setScaledContents(True)
        self.fondo_arriba.setScaledContents(True)
        diccionario["posicion x"] = pos_x_jugador
        diccionario["posicion y"] = pos_y_jugador
        self.senal_data_inicial.emit(diccionario)
        #Ahora posicionamos y escondemos al enemigo
        pos_x_enemigo = pos_x_jugador
        pos_y_enemigo = pos_y_jugador
        self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ABAJO_1))
        self.label_enemigo.setScaledContents(True)
        self.label_enemigo.move(pos_x_enemigo, pos_y_enemigo)
        self.senal_coordenandas_iniciales_enemigo.emit((pos_x_enemigo, pos_y_enemigo))
        self.label_enemigo.hide()

    def cambiar_pyf_enemigo(self, diccionario_mover_enemigo):
        #Cambiamos la posicion y la foto según lo que dictó el BE
        self.label_enemigo.show()
        pos_x_enemigo, pos_y_enemigo = diccionario_mover_enemigo["nueva posicion"]
        width = self.label_personaje.width()
        height = self.label_personaje.height()
        foto = diccionario_mover_enemigo["foto"]
        if foto == 'ABAJO_1':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ABAJO_1))
        elif foto == 'ABAJO_2':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ABAJO_2))
        elif foto == 'ABAJO_3':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ABAJO_3))
        elif foto == 'DERECHA_1':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_DERECHA_1))
        elif foto == 'DERECHA_2':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_DERECHA_2))
        elif foto == 'DERECHA_3':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_DERECHA_3))
        elif foto == 'IZQUIERDA_1':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_IZQUIERDA_1))
        elif foto == 'IZQUIERDA_2':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_IZQUIERDA_2))
        elif foto == 'IZQUIERDA_3':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_IZQUIERDA_3))   
        elif foto == 'ARRIBA_1':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ARRIBA_1))
        elif foto == 'ARRIBA_2':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ARRIBA_2))
        elif foto == 'ARRIBA_3':
            self.label_enemigo.setPixmap(QPixmap(p.ENEMIGO_ARRIBA_3)) 
        self.label_enemigo.setScaledContents(True)
        self.label_enemigo.setGeometry(pos_x_enemigo, pos_y_enemigo, width, height)
