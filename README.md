Pokemona 2.0

Esta es la versión 2 del primer juego de pokemona, solucionando las fallas, creando la clase padre pokemona y las hijas, que son las especies, agregando el clear en el mapa, y definiendo cada aspecto del juego en clases diferentes, como juego, mapa, pokemonas etc.

Características principales

Mapa de 10x10 donde el jugador se mueve con las teclas `W`, `A`, `S`, `D`.
Representación visual simple del mapa con:
  - "P" → Jugador.
  - "E" → Enemigos.
  - "." → Espacios vacíos.
- Menú de estados para consultar salud, energía y estadísticas de Pokemona.
- Sistema de combate contra enemigos.
- Guardado y carga de partida.

Estructura del código

El programa está dividido en varias clases, cada una con una responsabilidad específica:

1. Mapa
   - Representa el tablero del juego.  
   - Contiene el grid de 10x10, la posición del jugador y de los enemigos.  
   - Métodos principales: `crear_mapa`, `mostrar_mapa`, `mover_jugador`.  
   - Aquí se maneja la **colocación y eliminación de enemigos**.

2. Juego
   - Clase que controla el flujo principal del juego.  
   - Métodos: jugar, menu_estados, menu_combate, guardar_partida, etc.  
   - Representa la lógica de interacción entre el jugador, el mapa y los combates.

3. Pokemona (y sus derivados / enemigos)  
   - Clase que representa al personaje principal y sus atributos (salud, energía, ataques, etc.).  
   - Los enemigos también derivan de esta clase, demostrando el uso de herencia.

Conceptos de POO aplicados

Este proyecto está diseñado para poner en práctica los fundamentos de la Programación Orientada a Objetos:

1. Clases
   - Mapa, Juego, Pokemona, Enemigo, etc.  
   - Cada clase organiza datos y comportamientos relacionados en un solo lugar.

2. Objetos
   - Cuando se crea al jugador (self.pokemona_jugador = Pokemona(...)), se instancia un objeto.  
   - Los enemigos (enemigos_seleccionados[idx]()) también son objetos creados a partir de clases hijas.

3. Instancias
   - Cada vez que se crea un enemigo o un Pokemona, se obtiene una instancia única con su propio estado.

4. Atributos y métodos  
   - Ejemplo: self.salud, self.energia, mover_jugador(), mostrar_estado().  
   - Definen las propiedades y acciones de cada objeto.

5. Herencia  
   - Los enemigos heredan de la clase base Pokemona.  
   - Esto permite reutilizar código y compartir atributos comunes (como salud o energía) entre clases.

6. Polimorfismo
   - Cada enemigo puede redefinir su ataque especial sobrescribiendo métodos heredados.  
   - Al invocar el mismo método (atacar), cada clase puede ejecutar un comportamiento distinto.

7. Encapsulamiento
   - Los datos del mapa y de los enemigos están contenidos dentro de sus clases, evitando que se manipulen directamente desde fuera.  
   - Se accede a ellos únicamente mediante métodos (mover_jugador, eliminar_enemigo, etc.).


