# Sombras en la UNMSM
## Infiltración Táctica Nocturna en la Ciudad Universitaria

**Estudiantes:** 
Tapia Acosta Sandro Estanislao - 21140098
Pariguana Angulo Carlos - 21140100
Ibañez Sanchez Marlon - 19140098
**Institución:** Universidad Nacional Mayor de San Marcos - Fac. Ciencias Matemáticas  
**Año:** 2026

---

# Sombras en la UNMSM

**Sombras en la UNMSM** es un juego de infiltración táctica nocturna ambientado en el campus de la Universidad Nacional Mayor de San Marcos. El objetivo es escapar por las diferentes zonas del campus (como la Facultad de Matemáticas, el Estadio, la Plaza Cívica y la Puerta 7) mientras evitas ser detectado por guardias y drones de vigilancia.

---

## Instalación y Ejecución (Step-by-Step)

Sigue estos pasos para instalar y ejecutar el juego en tu computadora local.

**Paso 1: Requisitos previos**
Asegúrate de tener instalado [Python 3.8 o superior](https://www.python.org/downloads/) y `pip` en tu sistema.

**Paso 2: Descargar el proyecto**
Clona el repositorio o descarga el código fuente y entra al directorio del proyecto:

    git clone <https://github.com/seta6942/Proyecto_Videojuegos_Grupal>
    cd <Sombras>

**Paso 3: Crear un entorno virtual (Recomendado)**
Crea un entorno aislado para gestionar las dependencias del proyecto.

* **En Windows:**

    python -m venv venv
    .\venv\Scripts\activate

* **En macOS/Linux:**

    python3 -m venv venv
    source venv/bin/activate

**Paso 4: Instalar las dependencias**
Con el entorno virtual activado, instala las librerías necesarias ejecutando:

    pip install -r requirements.txt

**Paso 5: Ejecutar el juego**
Inicia el juego ejecutando el archivo principal:

    python main.py

---

## Características Principales

* **Mecánicas de Sigilo y Estamina:** Controla a Melvin mediante movimientos cautelosos en sigilo, camina normalmente, o gasta tu estamina con el sprint. El ruido que generas varía según tu velocidad y la superficie que pisas. 
* **Ocultación Dinámica:** Utiliza la vegetación (arbustos y árboles grandes) como cobertura para ocultarte de los enemigos.
* **IA Avanzada (Máquina de Estados):** Los guardias cuentan con conos de visión dinámicos y estados de comportamiento: Patrullar, Sospechar, Perseguir y Soporte (donde avisan a otros guardias cercanos). El campo visual respeta las paredes mediante raycasting inteligente.
* **Drones de Vigilancia:** Enemigos aéreos que patrullan zonas específicas y elevan el nivel de alerta global si te detectan.
* **Entorno Interactivo:** Lanza piedras (con inventario y cooldown visual) o hackea las alarmas de los autos aparcados para distraer a las patrullas enemigas y despejar tu ruta.
* **Iluminación Nocturna:** Un sistema de luces dinámicas con faroles parpadeantes y una luz cálida centrada en el jugador.
* **Minimapa en Tiempo Real:** Interfaz HUD que muestra un minimapa de vista superior del campus, detectores de estamina, nivel de alerta, contador de FPS y zona actual.
* **Generación Procedural y TMX:** Los niveles se pueden generar programáticamente con `ProceduralMap` o cargarse a través de archivos diseñados en Tiled (`.tmx`) mediante la librería `pytmx`.
* **Audio de Tensión:** Efectos de sonido dinámicos para los pasos y un motor de audio que eleva el volumen de la música de tensión conforme sube el porcentaje de alerta global.

## Controles

* **W, A, S, D o Flechas:** Moverse por el escenario.
* **SHIFT:** Activar modo Sigilo (caminar lento sin hacer ruido).
* **CTRL:** Sprint (correr más rápido, consume estamina y genera mucho ruido).
* **ESPACIO:** Ocultarse (Solo disponible sobre vegetación o zonas de cobertura).
* **CLIC DERECHO:** Lanzar una piedra hacia la posición del mouse.
* **TECLA Q:** Activar la alarma del auto más cercano dentro de tu rango.
* **ESC:** Pausar el juego o volver a la pantalla anterior en los menús.
* **R:** Reiniciar el juego desde las pantallas de Game Over o Pausa.

## Arquitectura del Proyecto (`src/`)

* **game.py:** Clase principal del juego que administra el Game Loop, los estados de la partida y la instancia de subsistemas.
* **player.py:** Lógica del jugador, físicas de movimiento, hitbox, y control del sistema de estamina y ocultación.
* **guard.py:** Inteligencia artificial, comportamiento *swarming* y dibujo del cono de visión semitransparente tricolor.
* **hud.py:** Interfaz de usuario gráfica, notificaciones dinámicas, minimapa top-down y menú principal.
* **lighting.py:** Sistema de renderizado de iluminación por gradientes y oscurecimiento del ambiente según la alerta.
* **map_generator.py:** Generador de los 4 niveles temáticos modelados para ser reconocibles como la UNMSM.
* **tilemap.py:** Motor de lectura TMX para soporte de mapas y rutas dinámicas.
* **audio.py:** Motor para el control de canales de sonido (pasos, impactos, alarmas) y música *BGM*.
* **sprites.py:** Generador procedural de *pixel art* y cargador robusto de recursos gráficos.
* **camera.py:** Motor de interpolación lineal (*lerp*) para la cámara con seguimiento suave.
* **settings.py:** Archivo global de configuraciones, variables, rutas y paletas de colores.

## Arquitectura

game/
├── main.py           # Punto de entrada
├── requirements.txt
└── src/
    ├── settings.py   # Constantes y configuración global
    ├── game.py       # Loop principal y coordinación
    ├── player.py     # Jugador (Melvin)
    ├── guard.py      # IA de guardias (FSM 3 estados)
    ├── camera.py     # Cámara con seguimiento suave
    ├── tilemap.py    # Carga de TMX (pytmx)
    ├── map_generator.py  # Mapa procedimental del campus UNMSM
    ├── lighting.py   # Iluminación nocturna
    ├── hud.py        # HUD y UI
    └── sprites.py    # Generador de sprites pixel art
