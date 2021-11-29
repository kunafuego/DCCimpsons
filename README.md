# Tarea 2: DCCimpsons:


¡Holaa! Intentaré hacer el mejor Readme posible para ayudar en la corrección. La verdad podría escribir 100 páginas sobre como fue hacer la tarea jaja, pero intentaré
ser lo más conciso posible y escribir solo lo necesario. 

## Consideraciones generales :octocat:

La tarea creo que en general me quedó muy bien. Seguí la misma lógica que en las actividades del curso, de crear una carpeta de frontend y otra de backend, además de un main
donde uno los archivos de ambas carpetas mediante señales. La idea era hacer un archivo de frontend y otro de backend para cada ventana, pero para la ventana de juego fue necesario
hacer dos backends para no sobrepasar el límite de las 400 líneas. Para cada archivo del backend cree una clase principal que tenía las funciones más importantes para el backend
de la ventana, y en caso de que hubieran personajes que se movían creaba también otra clase para este personaje. En el caso de la ventana de juego una clase para el enemigo y otra para
el character del usuario. 

Cree todos los objetos, obstáculos y personajes del mismo porte. Este porte es el que viene por default al crear un QLabel, 100 x 30 pixeles.

En muchas partes del código debía posicionar un objeto o obstáculo en posiciones donde no hubieran objetos, obstaculos o personajes. Para hacer esto creaba un set con todas las tuplas que no se podían ocupar,
luego creaba un while True en el que elegía una tupla al azar, y solo ocurría el break si es que esa tupla elegida al azar no estaba entre las que no podía ocupar.
Pero ahora, ¿Cómo generaba ese set de tuplas? Tenía atributos para guardar todas las posiciones de obstáculos, objetos y del personaje. Luego, para cada posición de cada uno de esos generaba las tuplas con el siguiente código:
```Código cuando se generan los obstáculos. Se ocupa el range con -+200 y -+60 porque no pueden haber dos obstáculos pegados.```
posx_prohibidas = [x for x in range(self.pos_personaje_x - 200, self.pos_personaje_x + 200)], se creaban todas las posiciones x prohibidas para ese obstáculo
posy_prohibidas = [y for y in range(self.pos_personaje_y - 60, self.pos_personaje_y + 60)], se creaban todas las posiciones y prohibidas para ese obstáculo
pos_prohibidas1 = set([(x,y) for x in posx_prohibidas for y in posy_prohibidas]), se creaban todas las tuplas prohibidas para ese obstáculo, y se añadían a las tuplas prohibidas anteriores.

En el caso de los obstáculos, dado que no varían nunca de posición, cree otro atributo con las tuplas prohibidas por ellos. Como no varían, esto hacía que el código no tuviera que crear
los mismos sets con tuplas prohibidas por obstáculos siempre.

Podría llamarle la atención de que los atributos con las posiciones de los objetos son diccionarios, ¿Por qué hice esto? Bueno, esto se me ocurrió porque introduje un nuevo concepto, el ***rut del objeto***.
Este rut del objeto me fue super útil, porque así a la hora de tener que hacer desaparecer un objeto en el frontend, yo con solo enviarle el rut, este ya sabía que objeto debía hacer desaparecer. Así, los atributos
con las posiciones de los objeto son diccionarios de la forma {rut_objeto: posicion_objeto}. Así, cuando el personaje colisiona con un objeto, busco cual es el rut del objeto en la posición de la colisión, y le envío
este rut al frontend. El rut es generado con un número aleatorio entre el 0 y el 1000000, por lo que la probabilidad de que dos objetos que están en la pantalla al mismo tiempo tengan el mismo rut es casi 0.

En cada archivo del backend se tiene una función que recibe un diccionario con información. Esto hace que cada ventana pueda ser llamada varias veces, y se le puede pasar información distinta cada vez que es llamada.

Dejaré acá algunos temas que creo que son importantes:

1. Enemigo:
Hice una pequeña modificación al enemigo porque creo que así cumplirá mejor su rol. El enemigo en mi juego se mueve según un parámetro, que aparece en parametros.py, llamado
TIEMPO_MOVIMIENTO_ENEMIGO_```DIFICULTAD```. Este parametro indica la cantidad de milisegundos que transcurrirán entre cada movimiento del enemigo. Además ocupé dos QTimers,
uno apenas parte la partida que espera hasta que tenga que aparecer el enemigo, y otro para cuando ya haya aparecido para que se mueva según el nuevo parámetro. Estos dos se
encuentran en la clase principal del BE de la ventana juego. Esta clase a su vez tiene dos atributos que ocupará el enemigo: ```self.cantidad_movimientos_enemigo```, que llevará
un int que cuenta cuántas veces se ha movido el enemigo, y ```self.posiciones_jugador```, una lista que guardará todas las posiciones del jugador en forma de tuplas. Así, cada vez
que el segundo Qtimer haga timeout, se el enviará a la clase del enemigo la tupla en self.posiciones_jugadores correspondiente al self.cantidad_movimientos_enemigo que lleva. En 
el primer timeout se le enviará la primera tupla de la lista, en el segundo timeout la segunda tupla, y así sigue. ***Justo antes de enviar la señal para mover al enemigo, se chequeará
que la posición que se le envía a este no sea la misma en la que está el jugador, porque en ese caso se termina la ronda, pues ambos han colisionado.***
Para dejarlo un poco más claro, haré un paso a paso la implementación del enemigo:
	- Cada vez que el jugador cambia de posición, se guarda el nuevo valor en la lista del atributo self.posiciones_jugador.
	- Apenas comienza la partida, se crea el primer QTimer. Este espera TIEMPO_DELAY_```DIFICULTAD``` segundos antes de llamar a la función que crea el segundo QTimer, ese que mueve al enemigo. 
	- Se crea el segundo QTimer y se para el primer QTimer. Este segundo QTimer, que tiene un interval definido por el parámetro arriba mencionado, llama a la función mover_enemigo. Esta función chequea que no colisionen el character con el enemigo, y según esto emite la señal necesaria.

2. Obstáculos:
Apenas se crea la partida, llamo a la función setear_obstaculos, que me genera los obstáculos y los envía al frontend para que los muestre. No aparecerán dos obstáculos en la misma 
posición, porque se ocupa el código explicado más arriba.

3. Aparecer Objetos:
Al iniciar la ronda, se crea el ```self.timer_objetos```. Este tiene intervalo igual a APARICION_```DIFICULTAD```, y su timeout llama a una función que crea un QThread de la clase ThreadAparecerObjetos que se encuentra en BE_ventana_juego2.
Este Thread se encarga de:
	- Crear los sets con tuplas con las posiciones prohibidas.
	- Elegir una posición válida para el objeto mediante el mismo while True que en los objetos.
	- Ocupar random.random() para setear que tipo de objeto será el creado.
	- Crear el rut del objeto creado.
	- Llamar mediante una señal a una función del BE principal, que guarda la posición del objeto y lo envía al frontend para que sea mostrado.

4. Desaparecer Objetos:
A la hora de guardar la posición en el BE principal del juego, se llama a la función crear_thread_desaparecer_objeto, que crea a la vez el Thread que esperará una cantidad de segundos para hacer desaparecer al objeto recién creado.
Este Thread para desaparecer objetos (también en el módulo BE_ventana_juego2), se encarga de:
	- Guardar el tiempo actual.
	- Setear la cantidad de segundos que abrá que esperar.
	- Chequear mediante un while True si el tiempo en ese segundo ya es el tiempo de los dos pasos anteriores, y si lo es manda una señal al backend principal del juego avisando que este objeto debe desaparecer.

Esta señal se conecta a la función desaparecer_objeto, que elimina al objeto(identificado con su rut) de las listas de posición, y le manda la señal al frontend para que lo elimine de la interfaz.
Todo esto lo hace dentro de un try, porque si el character ya había colisionado con el objeto, no habrá que hacer desaparecer a ningún objeto.

5. Ranking:
El ranking será guardado cada vez que, estando en la ventana postronda, el usuario elija volver al menú de inicio o salir del juego. Si se sale del juego cerrando la ventana con la X de la esquina
superior derecha, el puntaje no será guardado. No es necesario tener el archivo creado, pues si no existe ninguno el programa lo creará automáticamente.

6. Pausa:
A la hora de pausar el juego, a nivel de código ocurren dos cosas: 
	- en el main.py se desconectan algunas señales.
	- en el BE principal del juego se pausan los timers.


Me acabo de dar cuenta, pasado el tiempo de entrega, que hay dos módulos que cree pero que nunca se utilizan. ***LOS MÓDULOS BE_threads y BE_ventana_postronda NO SON UTILIZADOS EN NINGUNA PARTE DEL PROGRAMA***.

7. Música:
Utilicé la misma idea de música que en la AS2, y lo pude implementar de manera correcta en el backend de la ventana de incio. ***Me acabo de dar cuenta que había que ocupar la canción dada, pero ocupé otra que descargué de internet*** de https://www.talkingwav.com/simpson-song-wav-sounds/.
Tampoco leí que esta debía pausarse, ni que se tenía que reiniciar :disappointed:.

En el archivo main.py ocupé muchos comentarios para explicar cómo funciona el juego. En el resto de los archivos no hice muchos comentarios porque no me dio el tiempo, ¡perdón!. Espero que con lo de las señales + lo señalado acá sea suficiente.


### Cosas implementadas y no implementadas :white_check_mark: :x:
La tarea implementa ***todo*** lo indicado en el enunciado. El único error que tiene el juego es que cuando este se pausa, los threads de desaparecer objetos no se terminan, por lo que 
los objetos que están en la pantalla desaparecerán después de transcurrido el tiempo indicado en parametros.py. Este error lo dejé porque en el discord un ayudante me dijo que terminar
un QThread a la mala era una mala práctica, y pensé que capaz me restaría menos puntaje el error que el ocupar una mala práctica.

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.
Los otros archivos todos contienen clases y parametros que se importan y se crean objetos de estos en main.py.
Además se cargaron muchos archivos .ui, .jpg, .png y .wav a las carpetas del frontend. Las rutas de estas ya están conectadas en parametros.py.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```: Ocupé esta librería que crea las interfaces gráficas en casi todas los módulos de la tarea, y debe instalarse. 
2. ```os```: ```path.join() en parametros.py```
3. ```random```: ```randint() en BE_ventana_juego.py, BE_ventana_juego2.py, ventana_juego.py```
4. ```random```: ```random() en BE_ventana_juego2.py```
5. ```sys```: ```exit()``` siempre que se debía salir del juego.
6. ```random```: ```randint en BE_ventana_juego.py, BE_ventana_juego2.py```
7. ```time```: ```time()``` en BE_ventana_juego2.


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parametros.py```: Contiene todos los parámetros del juego.
2. ```BE_ventana_XXXX```: Contienen las clases con los backends principales de cada ventana. Juego, Preparacion y VentanaInicioBackend.
3. ```BE_ventana_juego2```: Contiene clases utilizadas en la clase principal del backend del juego (Juego). Contiene a las clases ThreadDesaparecerObjetos, ThreadAparecerObjetos, PersonajeJuego y EnemigoJuego.
4. ```ventana_XXXX```: Contienen las clases con los frontends principales de cada ventana. VentanaJuego, VentanaPreparacion, VentanaPostronda, VentanaInicio y VentanaRanking.


## Supuestos y consideraciones adicionales :thinking:
*El enemigo atraviesa los objetos.
*Los cheatcodes deben realizarse presionando las teclas en orden, y no al mismo tiempo. Entre cada una de las letras no se debe presionar ninguna otra.
*La señal del cheatcode V+I+D también podrá ser utilizada en la ventana de preparacion.
*Se debe intentar no programar que aparezcan objetos muy seguidos(>= 3s funciona bien), ya que se laggea un poco el movimiento del jugador.
*El bonus de la música se implementó completo, mientras que los otros dos no.


PD: Se me borró 100% ocupar el linter al final de la tarea :sob:. De todas maneras después lo revisé y tenía muy pocos errores. En los paths no ocupé nunca espacios después de la , porque en las actividades se hacía así.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. AS2: Para crear las ventanas de inicio y error me guié por las de la AS2. Está implementado en el archivo ventana_inicio.py en todas las líneas. Cree mis propios archivos Ui, y copié la idea de pegar las fotos dentro
del código para así evitar errores en la corrección. También me guíe por la AS2 para crear la música en BE_ventana_inicio.py.
2. Ocupé código de https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value en el archivo BE_ventana_ranking, en la línea 10 para obtener una lista con los nombres con mayor puntaje.

Creo que eso sería toodo. ¡¡Muchas gracias por leer y ojalá te guste!!
