# Ciclo euleriano con eventos reales

Implementación C++17 del algoritmo de Hierholzer para grafos no dirigidos, con IDs de aristas, eventos compactos y animación Manim. Arquitectura: **motor C++ → JSON de eventos → animación Manim**.

**Video e informe (Google Drive):** [PEGAR_AQUI_EL_LINK_DEL_DRIVE](PEGAR_AQUI_EL_LINK_DEL_DRIVE)

## Archivos

Las tres trazas del proyecto (`trace.json`, `trace_borde.json`, `trace_retroceso.json`), el video `GrafoEuleriano.mp4` y el informe PDF están versionados en el repositorio. `euler.exe`, la carpeta `media/` de Manim y las pruebas personales (`grafo_mio.txt`, `trace_mio.json`) se generan localmente y están en `.gitignore`.

| Archivo | Contenido |
|---|---|
| `euler.cpp` | Motor: lee el grafo por stdin y escribe el JSON (grafo, grados, `has_circuit`, `circuit`, `edge_order`, `events`). |
| `grafo_ejemplo.txt` → `trace.json` | Dos triángulos que comparten el vértice 0 (sin retrocesos intermedios). |
| `grafo_retroceso.txt` → `trace_retroceso.json` | Dos triángulos unidos por el vértice 1 (con retrocesos intermedios). |
| `grafo_borde.txt` → `trace_borde.json` | Camino 0-1-2: grados impares, sin ciclo. |
| `generar.ps1` | Compila `euler.cpp` y genera las 3 trazas con un solo comando. |
| `animacion.py` | Escena `GrafoEuleriano`: reproduce los eventos del JSON. |
| `validar_euler.py` | Pruebas del ejecutable: casos de borde, entradas inválidas, grafos aleatorios y grafos grandes. |
| `probar_grafo.py` | Probar el algoritmo con un grafo propio (a mano o desde un `.txt`); genera `trace_mio.json` sin tocar las trazas del proyecto. |

## Software requerido

- **g++ con C++17** (MinGW-w64 en Windows; por ejemplo, el que trae CLion, MSYS2 o w64devkit).
- **Python 3.11 o superior** (lo exige Manim 0.22).
- **Manim Community** (`pip install manim`). Las versiones recientes incluyen FFmpeg a través de PyAV, así que no hace falta instalarlo aparte. No se necesita LaTeX porque la escena solo usa `Text`.

## Pasos

### 1. Compilar el motor y generar las trazas

Desde PowerShell, en la carpeta del proyecto:

    .\generar.ps1

El script busca `g++` automáticamente: primero en el PATH y luego en las instalaciones habituales de Windows (el MinGW que trae CLion en cualquier versión, MSYS2, w64devkit, Chocolatey y WinLibs). Si no lo encuentra, indica la ruta a tu `g++.exe`:

    .\generar.ps1 -Cxx "<ruta a tu g++.exe>"

Si Windows bloquea la ejecución de scripts, usa `powershell -ExecutionPolicy Bypass -File .\generar.ps1`.

El script compila con `g++ -std=c++17 -O2 -Wall -Wextra` y luego ejecuta `euler.exe` con cada grafo. Equivale a correr a mano:

    g++ -std=c++17 -O2 -Wall -Wextra euler.cpp -o euler.exe
    cmd /c ".\euler.exe < grafo_ejemplo.txt > trace.json"
    cmd /c ".\euler.exe < grafo_borde.txt > trace_borde.json"
    cmd /c ".\euler.exe < grafo_retroceso.txt > trace_retroceso.json"

Se usa `cmd` para que la redirección no cambie la codificación del JSON (PowerShell 5.1 escribiría UTF-16). En bash basta con `./euler.exe < grafo_ejemplo.txt > trace.json`.

Formato de entrada: `n m` en la primera línea y luego `m` líneas `u v` con vértices entre `0` y `n-1`. Una entrada inválida (vértice fuera de rango, aristas faltantes o `n`/`m` negativos) termina con código 1 y un mensaje en stderr.

### 2. (Opcional) Validar el motor

    python validar_euler.py

### 3. Renderizar la animación

    python -m manim -pql animacion.py GrafoEuleriano

Por defecto se usa `trace.json`. Para elegir otro trace (PowerShell):

    $env:EULER_TRACE="trace_retroceso.json"
    python -m manim -pql animacion.py GrafoEuleriano

    $env:EULER_TRACE="trace_borde.json"
    python -m manim -pql animacion.py GrafoEuleriano

    Remove-Item Env:EULER_TRACE

En bash: `EULER_TRACE=trace_retroceso.json python -m manim -pql animacion.py GrafoEuleriano`.

Para alta resolución, reemplazar `-pql` por `-pqh`. Los videos se guardan en `media/videos/animacion/`, que está en `.gitignore`.

### 4. Probar con un grafo propio

El script `probar_grafo.py` permite ingresar un grafo propio y ver si tiene ciclo euleriano, sin modificar las trazas del proyecto (`trace.json`, `trace_borde.json` y `trace_retroceso.json` se mantienen intactas).

Ingresar el grafo a mano (el programa pide `n`, `m` y luego cada arista):

    python probar_grafo.py

Leer el grafo desde un archivo propio:

    python probar_grafo.py mi_grafo.txt

Agregar `--animar` a cualquiera de los dos para abrir directamente la animación en Manim:

    python probar_grafo.py --animar

El formato es el mismo que usa `euler.cpp`: la primera línea es `n m` (número de vértices y de aristas) y luego una arista `u v` por línea, con vértices numerados de `0` a `n-1`. Ejemplo, un cuadrado:

    4 4
    0 1
    1 2
    2 3
    3 0

Qué hace el script:
- Valida la entrada (enteros, vértices dentro de `0..n-1`) y vuelve a pedir el dato si hay un error.
- En modo manual guarda el grafo en `grafo_mio.txt` para poder reutilizarlo.
- Ejecuta `euler.exe` (si no existe, lo compila con `g++ -std=c++17`; si g++ no está en el PATH, correr antes `.\generar.ps1`) y guarda el resultado en `trace_mio.json`, un archivo aparte.
- Muestra los grados, si existe o no el ciclo y por qué, y el ciclo encontrado.
- Avisa si el grafo tiene lazos, aristas paralelas o más de 10 vértices, porque la animación no los representa bien (el C++ sí los procesa correctamente).

Para animar después un trace propio ya generado (PowerShell):

    $env:EULER_TRACE="trace_mio.json"
    python -m manim -pql animacion.py GrafoEuleriano

Con 5 vértices la animación usa la disposición fija de los ejemplos; con otro número de vértices los coloca en círculo. `grafo_mio.txt` y `trace_mio.json` están en `.gitignore`, así que las pruebas personales no se suben al repositorio.

## Eventos
- `start`: apilar el vértice inicial.
- `traverse`: consumir una arista y apilar su destino.
- `finish`: desapilar un vértice sin aristas libres y añadirlo a la salida provisional.
- `reverse`: invertir la salida para obtener el ciclo.

Manim reconstruye la pila a partir de esos eventos; no calcula un recorrido alternativo ni inventa pasos. Al llegar a `reverse`, un `assert` comprueba que la salida reconstruida coincide con el `circuit` calculado en C++. El marcador desaparece y reaparece durante los retrocesos: es retorno de control, no reutilización de una arista.

## Complejidad y alcance
C++: O(V+E) en tiempo y memoria, incluyendo los eventos y la serialización. Cada arista se marca una sola vez y el puntero `ptr[u]` de cada vértice solo avanza, así que el recorrido de las listas de adyacencia es amortizado lineal. La renderización tiene un costo aparte que no está incluido en esa cota.

- Por convención del programa, un grafo sin aristas (incluido `n = 0`) se considera sin ciclo.
- Los vértices aislados no impiden el ciclo de la componente con aristas.
- Si hay algún vértice de grado impar, o hay aristas en más de una componente, no hay ciclo y `circuit`, `edge_order` y `events` salen vacíos.
- El C++ maneja aristas paralelas y lazos (un lazo suma 2 al grado). La visualización usa líneas rectas y está pensada para grafos simples pequeños como los tres ejemplos: con lazos o aristas paralelas no se cae, pero no los dibuja de forma distinguible.

## Verificación
- El C++ compila sin advertencias con `-Wall -Wextra` (g++ 13.1).
- `generar.ps1` produce trazas idénticas byte a byte a las versionadas en el repositorio, y sin BOM.
- `probar_grafo.py` probado en modo manual (incluida una arista fuera de rango, que vuelve a pedir), desde archivo (con `grafo_retroceso.txt` genera la misma traza que `trace_retroceso.json`) y con un grafo de grados impares.
- `validar_euler.py` pasa: grafo vacío, vértices aislados, grados impares, grafo no conexo, aristas paralelas, lazos, entradas inválidas, 400 grafos aleatorios y grafos de hasta 400 000 vértices y 800 000 aristas.
- Manim Community 0.22.1 (Python 3.14) renderiza los tres traces sin errores, y el `assert` de reconstrucción pasa.

Pendiente para el video final: añadir motivación, explicación conceptual, complejidad y créditos.
