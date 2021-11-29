from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

import parametros as p
import sys

window_name_main, base_class_main = uic.loadUiType(p.VENTANA_INICIO)
window_name_error, base_class_error = uic.loadUiType(p.VENTANA_ERROR)


class VentanaInicio(window_name_main, base_class_main):

    senal_verificar_usuario = pyqtSignal(str)
    senal_ver_ranking = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logo.setPixmap(QPixmap(p.LOGO_INICIO))
        self.logo.setScaledContents(True)
        self.boton_iniciar_partida.clicked.connect(self.verificar_usuario)
        self.boton_salir.clicked.connect(self.salir_juego)
        self.boton_rankings.clicked.connect(self.rankings) 
        
    def mostrar_inicio(self):
        self.show()

    def rankings(self):
        self.senal_ver_ranking.emit()

    def verificar_usuario(self):
        self.senal_verificar_usuario.emit(self.ingresar_nombre.text())
        pass

    def esconder_inicio(self):
        self.hide()

    def salir_juego(self):
        self.hide()
        sys.exit()

class VentanaError(window_name_error, base_class_error):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_volver.clicked.connect(self.esconder)
        self.logo_error.setPixmap(QPixmap(p.LOGO_ERROR))
        self.logo_error.setScaledContents(True)
        self.boton_salir.clicked.connect(self.salir)

    def salir(self):
        self.esconder()
        sys.exit()

    def mostrar_error(self):
        self.show()

    def esconder(self):
        self.hide()
