from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

import parametros as p
from random import randint

window_name_main, base_class_main = uic.loadUiType(p.VENTANA_PREPARACION)


class VentanaPreparacion(window_name_main, base_class_main):

    senal_crear_personaje = pyqtSignal(dict)
    senal_pedir_data = pyqtSignal(str)
    senal_teclas = pyqtSignal(dict)
    senal_comenzar_ronda = pyqtSignal(dict)
    senal_cheatcode_vida = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.foto_homero.setPixmap(QPixmap(p.FOTO_HOMERO))
        self.foto_homero.setScaledContents(True)
        self.foto_lisa.setPixmap(QPixmap(p.FOTO_LISA))
        self.foto_lisa.setScaledContents(True)
        self.mapa_preparacion.setPixmap(QPixmap(p.MAPA_PREPARACION))
        self.mapa_preparacion.setScaledContents(True)    
        self.barra_vida.setValue(100)
        self.label_local_incorrecto.setVisible(False)
        self.label_local_incorrecto.setStyleSheet("background-color: red")
        self.label_selecciona_dificultad.setVisible(False)
        self.label_selecciona_dificultad.setStyleSheet("background-color: red")
        self.check_intro.clicked.connect(self.checked)
        self.check_avanzada.clicked.connect(self.checked)
        self.boton_homero.clicked.connect(self.homero_clickeado)
        self.boton_lisa.clicked.connect(self.lisa_clickeado)
        self.teclas_apretadas = []
        self.senal_comenzar_ronda.connect(self.esconder)
        self.jugador_homero = QLabel(self)
        self.jugador_lisa = QLabel(self)
        self.dificultad_juego = None
        self.homero_mostrado = False
        self.lisa_mostrado = False
        self.personaje = None

    def homero_clickeado(self):
        if not self.homero_mostrado:
            if self.lisa_mostrado:
                self.jugador_lisa.hide()    
                self.lisa_mostrado = False           
            self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ABAJO_1))
            self.jugador_homero.setScaledContents(True)
            pos_x = randint(p.BORDE_VERTICAL_IZQ_P, p.BORDE_VERTICAL_DER_P)
            pos_y = randint(p.BORDE_HORIZONTAL_UP_P, p.BORDE_HORIZONTAL_DOWN_P)
            self.jugador_homero.move(pos_x, pos_y)
            dic_senal = {"posicion x": pos_x, "posicion y": pos_y, "personaje": 'homero'}
            self.senal_crear_personaje.emit(dic_senal)
            self.homero_mostrado = True
            self.personaje = 'homero'
            self.jugador_homero.show()
               
    def lisa_clickeado(self):
        if not self.lisa_mostrado:
            if self.homero_mostrado:
                self.jugador_homero.hide()
                self.homero_mostrado = False               
            self.jugador_lisa.setPixmap(QPixmap(p.LISA_ABAJO_1))
            self.jugador_lisa.setScaledContents(True)
            pos_x = randint(p.BORDE_VERTICAL_IZQ_P, p.BORDE_VERTICAL_DER_P)
            pos_y = randint(p.BORDE_HORIZONTAL_UP_P, p.BORDE_HORIZONTAL_DOWN_P)
            self.jugador_lisa.move(pos_x, pos_y)
            dic_senal = {"posicion x": pos_x, "posicion y": pos_y, "personaje": 'lisa'}
            self.senal_crear_personaje.emit(dic_senal)
            self.lisa_mostrado = True
            self.personaje = 'lisa'
            self.jugador_lisa.show()
            
    def keyPressEvent(self, event):
        if not self.homero_mostrado and not self.lisa_mostrado:
            return
        if event.key() == Qt.Key_W:
            self.senal_teclas.emit({'direccion': 'up', "dificultad": self.dificultad_juego})
        if event.key() == Qt.Key_D:
            self.senal_teclas.emit({'direccion': 'right',"dificultad": self.dificultad_juego})
        if event.key() == Qt.Key_A:
            self.senal_teclas.emit({'direccion': 'left',"dificultad": self.dificultad_juego})
        if event.key() == Qt.Key_S:
            self.senal_teclas.emit({'direccion': 'down',"dificultad": self.dificultad_juego})
        self.teclas_apretadas.append(event.key())
        try:
            if self.teclas_apretadas[-1] == Qt.Key_D and self.teclas_apretadas[-2] == Qt.Key_I and \
            self.teclas_apretadas[-3] == Qt.Key_V:
                self.senal_cheatcode_vida.emit()
        except IndexError:
            pass

    def actualizar_VID(self, vida):
        self.barra_vida.setValue(int(vida * 100))

    def cambiar_pyf(self, diccionario):
        pos_x, pos_y = diccionario["n_posicion"]
        if self.personaje == 'homero':
            width = self.jugador_homero.width()
            height = self.jugador_homero.height()
            foto = diccionario["foto"]
            if foto == 'ABAJO_1':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ABAJO_1))
            elif foto == 'ABAJO_2':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ABAJO_2))
            elif foto == 'ABAJO_3':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ABAJO_3))
            elif foto == 'DERECHA_1':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_DERECHA_1))
            elif foto == 'DERECHA_2':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_DERECHA_2))
            elif foto == 'DERECHA_3':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_DERECHA_3))
            elif foto == 'IZQUIERDA_1':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_IZQUIERDA_1))
            elif foto == 'IZQUIERDA_2':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_IZQUIERDA_2))
            elif foto == 'IZQUIERDA_3':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_IZQUIERDA_3))   
            elif foto == 'ARRIBA_1':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ARRIBA_1))
            elif foto == 'ARRIBA_2':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ARRIBA_2))
            elif foto == 'ARRIBA_3':
                self.jugador_homero.setPixmap(QPixmap(p.HOMERO_ARRIBA_3)) 
            self.jugador_homero.setScaledContents(True)
            self.jugador_homero.setGeometry(pos_x, pos_y, width, height)
        elif self.personaje == 'lisa':
            width = self.jugador_lisa.width()
            height = self.jugador_lisa.height()
            foto = diccionario["foto"]
            if foto == 'ABAJO_1':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_ABAJO_1))
            elif foto == 'ABAJO_2':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_ABAJO_2))
            elif foto == 'ABAJO_3':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_ABAJO_3))
            elif foto == 'DERECHA_1':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_DERECHA_1))
            elif foto == 'DERECHA_2':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_DERECHA_2))
            elif foto == 'DERECHA_3':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_DERECHA_3))
            elif foto == 'IZQUIERDA_1':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_IZQUIERDA_1))
            elif foto == 'IZQUIERDA_2':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_IZQUIERDA_2))
            elif foto == 'IZQUIERDA_3':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_IZQUIERDA_3))   
            elif foto == 'ARRIBA_1':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_ARRIBA_1))
            elif foto == 'ARRIBA_2':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_ARRIBA_2))
            elif foto == 'ARRIBA_3':
                self.jugador_lisa.setPixmap(QPixmap(p.LISA_ARRIBA_3)) 
            self.jugador_lisa.setScaledContents(True)
            self.jugador_lisa.setGeometry(pos_x, pos_y, width, height)
        if pos_y >= p.BORDE_HORIZONTAL_UP_P:
            self.label_selecciona_dificultad.setVisible(False)
            self.label_local_incorrecto.setVisible(False)

    def checked(self):
        checkbox_clickeado = self.sender()
        if checkbox_clickeado == self.check_intro:
            self.dificultad_juego = 'intro'
            self.check_avanzada.setChecked(False)
            self.check_intro.setChecked(True)
            self.check_avanzada.setEnabled(True)
            self.check_intro.setEnabled(False)
        else:
            self.dificultad_juego = 'avanzada'
            self.check_intro.setChecked(False)
            self.check_avanzada.setChecked(True)
            self.check_intro.setEnabled(True)
            self.check_avanzada.setEnabled(False)

    def empezar_preparacion(self, usuario):
        self.senal_pedir_data.emit(usuario)
        self.check_intro.setChecked(False)
        self.check_avanzada.setChecked(False)
        self.check_intro.setEnabled(True)
        self.check_avanzada.setEnabled(True)
        self.mostrar_ventana_preparacion()

    def empezar_preparacion_denuevo(self, diccionario_preparacion):
        self.label_local_incorrecto.setVisible(False)
        self.label_selecciona_dificultad.setVisible(False)
        usuario = diccionario_preparacion["usuario"]
        self.senal_pedir_data.emit(usuario)
        self.mostrar_ventana_preparacion()

    def mostrar_ventana_preparacion(self):
        self.show()

    def recibir_data_preparacion(self, diccionario):
        self.barra_vida.setValue(int(float(diccionario["vida"]) * 100))
        self.label_ronda.setText('Rondas: '+str(diccionario["Rondas"]))
        self.label_puntaje.setText('Puntaje: '+str(diccionario["Puntaje"]))
        self.label_items_malos.setText('Objetos Malos: '+str(diccionario["Objetos Malos"]))
        self.label_items_buenos.setText('Objetos Buenos: '+str(diccionario["Objetos Buenos"]))

    def esconder(self):
        self.lisa_mostrado = False
        self.homero_mostrado = False
        self.personaje = None
        self.jugador_homero.hide()
        self.jugador_lisa.hide()
        self.hide()
    
    def local_incorrecto(self):
        """
Viene para mostrar el label con el mensaje del local incorrecto
        """
        self.label_local_incorrecto.setVisible(True)
        pass
    
    def local_correcto(self, diccionario_ronda):
        """
Viene para revisar que este checkeado el botón de dificultad y luego 
enviar señal para partir juego
Debe seguir rellenando el diccionario para la señal de comenzar juego
        """
        if self.dificultad_juego == None:
            self.label_selecciona_dificultad.setVisible(True)
        else:
            self.senal_comenzar_ronda.emit(diccionario_ronda)
