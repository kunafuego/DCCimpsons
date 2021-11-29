from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtMultimedia
import parametros as p

class VentanaInicioBackend(QObject):

    senal_empezar_juego = pyqtSignal(str)
    senal_mensaje_error = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.musica = Musica(p.RUTA_CANCION)
        self.comenzar_musica()

    def comenzar_musica(self):
        self.musica.comenzar()
    
    def verificar_usuario(self, usuario):
        if usuario.isalnum():
            self.senal_empezar_juego.emit(usuario)
        else:
            self.senal_mensaje_error.emit()
        pass

class Musica(QObject):
    # NO MODIFICAR ESTA CLASE

    def __init__(self, ruta_cancion):
        super().__init__()
        self.ruta_cancion = ruta_cancion

    def comenzar(self):
        self.cancion = QtMultimedia.QSound(self.ruta_cancion)
        self.cancion.Loop()
        self.cancion.play()
