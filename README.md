# Ciclo euleriano con eventos reales

Adaptación de euler.cpp del grupo. Implementación C++17 de Hierholzer para grafos no dirigidos, con IDs de aristas, eventos compactos y animación Manim.

## Uso rápido en Windows
Copiar animacion.py y los JSON a la carpeta del proyecto donde funciona Manim.

    python -m manim -pql animacion.py GrafoEuleriano

Para el ejemplo con retrocesos intermedios (PowerShell):

    $env:EULER_TRACE="trace_retroceso.json"
    python -m manim -pql animacion.py GrafoEuleriano

Para el caso sin ciclo:

    $env:EULER_TRACE="trace_borde.json"
    python -m manim -pql animacion.py GrafoEuleriano

Volver al ejemplo inicial:

    Remove-Item Env:EULER_TRACE

Alta resolución: reemplazar -pql por -pqh.

## Regenerar los JSON desde C++
Requiere g++ con soporte C++17. Desde la carpeta del proyecto:

    g++ -std=c++17 -O2 -Wall -Wextra euler.cpp -o euler.exe
    cmd /c "euler.exe < grafo_ejemplo.txt > trace.json"
    cmd /c "euler.exe < grafo_borde.txt > trace_borde.json"
    cmd /c "euler.exe < grafo_retroceso.txt > trace_retroceso.json"

Se usa cmd para que la redirección funcione también desde PowerShell y no cambie la codificación del JSON. Los JSON incluidos fueron generados por esta versión del C++.

## Probar con un grafo propio
El script probar_grafo.py permite ingresar un grafo propio y ver si tiene ciclo euleriano, sin modificar los traces del proyecto (trace.json, trace_borde.json y trace_retroceso.json se mantienen intactos).

Ingresar el grafo a mano (el programa pide n, m y luego cada arista):

    python probar_grafo.py

Leer el grafo desde un archivo propio:

    python probar_grafo.py mi_grafo.txt

Agregar --animar a cualquiera de los dos para abrir directamente la animación en Manim:

    python probar_grafo.py --animar

Formato del grafo (el mismo que usa euler.cpp): la primera línea es "n m" (número de vértices y de aristas) y luego una arista "u v" por línea, con vértices numerados de 0 a n-1. Ejemplo, un cuadrado:

    4 4
    0 1
    1 2
    2 3
    3 0

Qué hace el script:
- Valida la entrada (enteros, vértices dentro de 0..n-1) y vuelve a pedir el dato si hay un error.
- En modo manual guarda el grafo en grafo_mio.txt para poder reutilizarlo.
- Ejecuta euler.exe (si no existe, lo compila con g++ -std=c++17) y guarda el resultado en trace_mio.json, un archivo aparte.
- Muestra los grados, si existe o no el ciclo y por qué, y el ciclo encontrado.
- Avisa si el grafo tiene lazos, aristas paralelas o más de 10 vértices, porque la animación no los representa bien (el C++ sí los procesa correctamente).

Para animar después un trace propio ya generado (PowerShell):

    $env:EULER_TRACE="trace_mio.json"
    python -m manim -pql animacion.py GrafoEuleriano

Con 5 vértices la animación usa la disposición fija de los ejemplos; con otro número de vértices los coloca en círculo.

## Eventos
- start: apilar el vértice inicial.
- traverse: consumir una arista y apilar su destino.
- finish: desapilar un vértice sin aristas libres y añadirlo a la salida provisional.
- reverse: invertir la salida para obtener el ciclo.

Manim reconstruye la pila a partir de esos eventos; no calcula un recorrido alternativo ni inventa pasos. El marcador desaparece y reaparece durante los retrocesos: es retorno de control, no reutilización de una arista.

## Complejidad y alcance
C++: O(V+E) tiempo y memoria, incluyendo eventos y serialización; se eliminó map y no se copian estados completos de la pila por evento. La renderización tiene un costo independiente y no está incluida en esa cota.
La convención del programa considera sin ciclo a un grafo sin aristas. Los vértices aislados no impiden el ciclo de la componente con aristas.
El C++ maneja aristas paralelas y lazos. Esta visualización con líneas rectas está diseñada para grafos simples pequeños como los tres ejemplos; no representa adecuadamente lazos ni aristas paralelas.

#Link del Drive (Video y Informe) : < aqui ira el link>

## Verificación
C++ compilado con advertencias activadas. Comprobados los eventos y el ciclo de los ejemplos, además de pruebas aleatorias contra condiciones de existencia. Python verificado sintácticamente. No se renderizó Manim en el entorno de preparación; comprobar visualmente en el equipo del usuario.

Esta escena es la demostración del algoritmo; aún deben añadirse motivación, explicación conceptual, complejidad y créditos para completar el video solicitado. Incorporar los cambios al repositorio con commits reales, sin inventar historial.
