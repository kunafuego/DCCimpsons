from PyQt5.QtWidgets import QApplication

import sys

from frontend.ventana_inicio import VentanaInicio, VentanaError
from backend.BE_ventana_inicio import VentanaInicioBackend
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_preparacion import VentanaPreparacion
from backend.BE_ventana_preparacion import PersonajePreparacion, Preparacion
from frontend.ventana_juego import VentanaJuego
from backend.BE_ventana_juego import Juego
from backend.BE_ventana_juego2 import PersonajeJuego, EnemigoJuego
from frontend.ventana_postronda import VentanaPostronda

def pausar_senales_juego(accion):
    if accion == "pausar":
        ventana_juego.senal_teclas.disconnect()
        logica_juego.senal_bajar_un_sec.disconnect()
    elif accion == "despausar":
        ventana_juego.senal_teclas.connect(personaje_juego.moverse)
        logica_juego.senal_bajar_un_sec.connect(ventana_juego.bajar_un_sec)

if __name__ == "__main__":
    app = QApplication([])

    #Ventanas y lógica inicio
    ventana_inicio = VentanaInicio()
    ventana_error = VentanaError()
    logica_inicio = VentanaInicioBackend()
    ventana_ranking = VentanaRanking()

    #Ventana y lógica preparación
    ventana_preparacion = VentanaPreparacion()
    logica_preparacion = Preparacion()
    personaje_preparacion = PersonajePreparacion()

    #Ventanas y lógica juego
    ventana_juego = VentanaJuego()
    personaje_juego = PersonajeJuego()
    enemigo_juego = EnemigoJuego()
    logica_juego = Juego()

    #Ventanas y lógica post ronda
    ventana_postronda = VentanaPostronda()

    #SEÑALES INICIO

    #Mostramos la ventana de inicio
    ventana_inicio.mostrar_inicio()

    #Esta señal verifica si el nombre de usuario está bien
    ventana_inicio.senal_verificar_usuario.connect(logica_inicio.verificar_usuario)
    #Si está bien el nombre, pasa a la siguiente ventana
    logica_inicio.senal_empezar_juego.connect(ventana_preparacion.empezar_preparacion)
    logica_inicio.senal_empezar_juego.connect(ventana_inicio.esconder_inicio)
    #Si está mal el nombre, se muestra la ventana de error
    logica_inicio.senal_mensaje_error.connect(ventana_error.mostrar_error)

    #Si elige ver el ranking, mostramos la ventana de rankings
    ventana_inicio.senal_ver_ranking.connect(ventana_ranking.mostrar_ranking)

    #SEÑALES PREPARACIÓN

    #al principio la ventana debe pedirle la data al backend, que la va a tener desde antes
    ventana_preparacion.senal_pedir_data.connect(logica_preparacion.mandar_data_preparacion)
    #Luego el BE le manda la data a la ventana y esta la muestra
    logica_preparacion.senal_mandar_data.connect(ventana_preparacion.recibir_data_preparacion)

    #Una vez que se clickea un personaje, se manda la senal para que este sea creado en el BE:
    #Primero le mandamos sus coordenadas al BE del jugador
    ventana_preparacion.senal_crear_personaje.connect(personaje_preparacion.coordenadas_iniciales)
    #Luego le mandamos la data al BE principal
    ventana_preparacion.senal_crear_personaje.connect(logica_preparacion.data_inicial_personaje_pre)

    #cada vez que es apretada una tecla, se le manda una señal al BE del jugador 
    #para avisarle que se tiene que mover
    ventana_preparacion.senal_teclas.connect(personaje_preparacion.mover_personaje_pre)
    #Luego de que se mueva el BE del jugador(que revisará que no choque con los bordes) manda 
    #dos señales, una al FE y otra al BE principal para notificar el cambio 
    personaje_preparacion.senal_mandar_cambio.connect(ventana_preparacion.cambiar_pyf)
    personaje_preparacion.senal_mandar_cambio.connect(logica_preparacion.cambiar_posicion)
    #Si la nueva posición es una de los locales, se mandará la señal al BE principal
    #para que se revise si es el local del jugador o no 
    personaje_preparacion.senal_revisar_local.connect(logica_preparacion.revisar_local)
    #Si no está en su local, el BE principal de la preparacion le manda una señal al FE para que
    #le notifique al usuario mediante un label
    logica_preparacion.senal_local_incorrecto.connect(ventana_preparacion.local_incorrecto)
    #Si está en su local, el BE principal envía la data y le dice al frontend que revise si 
    #está marcada la dificultad en la interfaz
    logica_preparacion.senal_comenzar_ronda.connect(ventana_preparacion.local_correcto)
    #El frontend da el visto bueno y se muestra la ventana de juego, con lo que tambien 
    #se mandan las coordenadas iniciales al personaje del backend y al enemigo. Además
    #le manda la info inicial de la partida al BE principal del juego
    ventana_preparacion.senal_comenzar_ronda.connect(ventana_juego.mostrar_juego)
    ventana_juego.senal_coordenandas_iniciales_enemigo.connect(enemigo_juego.coordenadas_iniciales)
    ventana_juego.senal_data_inicial.connect(personaje_juego.coordenadas_iniciales_personaje)
    ventana_juego.senal_data_inicial.connect(logica_juego.data_inicio_ronda)

    #En todo minuto de la preparacion, cuando hago la combinación VID en el teclado se 
    #me suma la vida
    ventana_preparacion.senal_cheatcode_vida.connect(logica_preparacion.cheatcode_vida)
    logica_preparacion.senal_actualizar_vida_en_FE.connect(ventana_preparacion.actualizar_VID)
    
    #SEÑALES JUEGO

    #Cuando hago la combinación VID en el teclado se me suma la vida
    ventana_juego.senal_cheatcode_vida.connect(logica_juego.cheatcode_vida)

    #Cuando hago la combinación NIV en el teclado termina la ronda
    ventana_juego.senal_cheatcode_ronda.connect(logica_juego.ventana_post_ronda)

    #Para comenzar, se envían las posiciones de los obstaculos al FE para que los muestre
    logica_juego.senal_enviar_obstaculos.connect(ventana_juego.mostrar_obstaculos)

    #Cada segundo que pasa, se baja un segundo el reloj
    logica_juego.senal_bajar_un_sec.connect(ventana_juego.bajar_un_sec)

    #Cuando se pausa el juego(mediante el boton o apretando P), se le avisa al BE principal para 
    #que pare los timers, y también se corre una función de main que corta las señales
    ventana_juego.senal_pausar_juego.connect(pausar_senales_juego)
    ventana_juego.senal_pausar_juego.connect(logica_juego.pausar_timers)

    #Cada vez que el timer del BE principal lo indica, este crea un QThread que hace que aparezca
    #un nuevo objeto. Luego el Qthread le avisa al BE principal del juego que el objeto 
    #fue creado, y este manda la señal para que sea mostrado en el FE.
    logica_juego.senal_aparecer_objeto.connect(ventana_juego.mostrar_objeto)
    #Cuando se manda la señal para que se muestre el objeto, se llama a una función que crea el 
    #Thread que hace desaparecer el objeto. Este espera la cantidad de segundos necesaria y le avisa
    #al BE principal, mediante una señal interior, que envíe la señal para desaparecer el objeto
    logica_juego.senal_desaparecer_objeto.connect(ventana_juego.desaparecer_objeto)

    #Cada vez que el Qtimer del enemigo dice que se tiene que mover, se le 
    #mandará una señal al BE del enemigo avisándole que se tiene que mover, y este a su vez 
    #le avisará al FE que debe cambiar su posición
    logica_juego.senal_mover_enemigo.connect(enemigo_juego.mover_enemigo)
    enemigo_juego.senal_mover_enemigo_FE.connect(ventana_juego.cambiar_pyf_enemigo)

    #Ahora, ¿Cómo se mueve el personaje?
    #Cuando apreto tecla el personaje trata de moverse en el BE del personaje
    ventana_juego.senal_teclas.connect(personaje_juego.moverse)
    #El personaje le pregunta al BE principal si está ok su cambio, y este aprovecha de revisar si 
    #hay colisiones
    personaje_juego.senal_chequear_cambio.connect(logica_juego.chequear_cambio)
    #La logica revisa lo que tenga que revisar y lo manda al frontend
    logica_juego.senal_pos_todo_bien.connect(ventana_juego.cambiar_pyf)
    #Si es que la colisión es con un obstáculo, el BE principal del juego le manda una señal al 
    #BE del personaje avisándole que no puede cambiar su posición hacia allá. De todas maneras se 
    #envía la señal al FE para que cambie la foto, pero la posición sigue siendo la misma
    logica_juego.senal_chocando_obstaculo.connect(personaje_juego.chocando_obstaculos)
    
    #Cada vez que se choca con un obstáculo, se debe cambiar la data en el FE
    logica_juego.senal_actualizar_data_FE.connect(ventana_juego.actualizar_data_FE)
    
    #Si se termina el juego por cualquier razón, se debe mostrar la ventana postronda
    #Esta señal a su vez lleva toda la info de la partida
    logica_juego.senal_ventana_post_ronda.connect(ventana_juego.esconder_ventana_juego)
    logica_juego.senal_ventana_post_ronda.connect(ventana_postronda.mostrar_ventana_postronda)

    #SEÑALES POSTRONDA

    #Si se apreta seguir jugando, se actualiza la data de la preparacion, y se muestra la ventana 
    #de presentación nuevamente
    ventana_postronda.senal_volver_ventana_presentacion.connect(logica_preparacion.actualizar_data)
    ventana_postronda.senal_volver_ventana_presentacion.connect\
                                            (ventana_preparacion.empezar_preparacion_denuevo)

    #Si se aprieta volver a ventana inicio, se empieza todo denuevo y se actualiza el ranking. 
    #El ranking también se actualiza si se aprieta el botón salir
    ventana_postronda.senal_volver_ventana_inicio.connect(ventana_inicio.mostrar_inicio)
    ventana_postronda.senal_actualizar_ranking.connect(ventana_ranking.actualizar_archivo_ranking)

    sys.exit(app.exec_())
