from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

import parametros as p
import sys

window_name_main, base_class_main = uic.loadUiType(p.VENTANA_POSTRONDA)


class VentanaPostronda(window_name_main, base_class_main):

    senal_volver_ventana_presentacion = pyqtSignal(dict)
    senal_volver_ventana_inicio = pyqtSignal()
    senal_actualizar_ranking = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.foto.setPixmap(QPixmap(p.FOTO_POSTRONDA))
        self.foto.setScaledContents(True)
        #Estos dos atributos los defino para actualizar el ranking en caso que sea necesario
        self.diccionario_ranking = {}
        self.diccionario = {}
    
    def mostrar_ventana_postronda(self, diccionario_postronda):
        vida = diccionario_postronda["vida"]
        self.diccionario_ranking["usuario"] = diccionario_postronda["usuario"]
        self.diccionario_ranking["puntaje"] = diccionario_postronda["puntaje"]
        self.diccionario = diccionario_postronda
        self.label_puntaje.setText(str(diccionario_postronda["puntaje"]))
        self.label_puntaje.setAlignment(Qt.AlignCenter)
        self.label_vida.setText(str(int(vida * 100)))
        self.label_vida.setAlignment(Qt.AlignCenter)
        self.label_mensaje.setAlignment(Qt.AlignCenter)
        self.label_items_buenos.setText(str(diccionario_postronda["items buenos"]))
        self.label_items_buenos.setAlignment(Qt.AlignCenter)
        self.label_items_malos.setText(str(diccionario_postronda["items malos"]))
        self.label_items_malos.setAlignment(Qt.AlignCenter)
        self.boton_inicio.clicked.connect(self.volver_al_inicio)
        if vida > 0:
            self.label_mensaje.setStyleSheet("background-color: green")
            self.label_mensaje.setText("PUEDES SEGUIR JUGANDO")
            self.boton_seguir_jugando.setEnabled(True)
            self.boton_seguir_jugando.clicked.connect(self.volver_ventana_preparacion)
        else:
            self.label_mensaje.setStyleSheet("background-color: red")
            self.label_mensaje.setText("NO PUEDES SEGUIR JUGANDO")
            self.boton_seguir_jugando.setEnabled(False)
        self.boton_salir.clicked.connect(self.salir)
        self.show()

    def salir(self):
        self.senal_actualizar_ranking.emit(self.diccionario_ranking)
        self.hide()
        sys.exit()

    def volver_al_inicio(self):
        self.hide()
        self.senal_volver_ventana_inicio.emit()
        self.senal_actualizar_ranking.emit(self.diccionario_ranking)
        pass

    def volver_ventana_preparacion(self):
        self.hide()
        self.senal_volver_ventana_presentacion.emit(self.diccionario)
        pass
