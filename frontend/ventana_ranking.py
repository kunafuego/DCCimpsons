from PyQt5 import uic
from PyQt5.QtGui import QPixmap

import parametros as p
import sys

window_name_main, base_class_main = uic.loadUiType(p.VENTANA_RANKING)


class VentanaRanking(window_name_main, base_class_main):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.foto_ranking.setPixmap(QPixmap(p.FOTO_RANKING))
        self.foto_ranking.setScaledContents(True)
        self.boton_volver.clicked.connect(self.volver)
        self.boton_salir.clicked.connect(self.salir)

    def mostrar_ranking(self):
        self.setear_ranking()
        self.show()

    def volver(self):
        self.hide()

    def salir(self):
        self.hide()
        sys.exit()
    
    def actualizar_archivo_ranking(self, diccionario_ranking):
        with open("ranking.txt", "a") as archivo:
            print(diccionario_ranking["usuario"] + ","+ str(diccionario_ranking["puntaje"]) + "\n", 
                    file=archivo, end="")
            archivo.close()

    def obtener_ranking(self):
        try:
            with open("ranking.txt", "r") as archivo:
                puntajes = {}
                lineas = archivo.readlines()
                for linea in lineas:
                    lista_linea = linea.strip().split(",")
                    puntajes[lista_linea[0]] = int(lista_linea[1])
                archivo.close()
            puntajes_ordenado = [(u,p) for u, p in sorted(puntajes.items(), 
                                 key=lambda item: item[1], reverse=True)]
            if len(puntajes_ordenado) > 5:
                puntajes_ordenado = [(u,p) for u,p in puntajes_ordenado[:5]]
            return puntajes_ordenado
        except FileNotFoundError:
            with open("ranking.txt", "w") as archivo_nuevo:
                archivo_nuevo.close()
        
    def setear_ranking(self):
        ranking = self.obtener_ranking()
        try:
            self.primero_ranking.setText("1: " + ranking[0][0] + " " + str(ranking[0][1]))
            self.segundo_ranking.setText("2: " + ranking[1][0] + " " + str(ranking[1][1]))
            self.tercero_ranking.setText("3: " + ranking[2][0] + " " + str(ranking[2][1]))
            self.cuarto_ranking.setText("4: " + ranking[3][0] + " " + str(ranking[3][1]))
            self.quinto_ranking.setText("5: " + ranking[4][0] + " " + str(ranking[4][1]))
        except IndexError:
            pass
        except TypeError:
            pass


