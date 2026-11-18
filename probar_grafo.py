"""
probar_grafo.py  -  Probar el algoritmo con un grafo propio.

Permite ingresar un grafo NO dirigido a mano (o desde un .txt), lo pasa por
euler.cpp (euler.exe) y genera un trace JSON propio, SIN tocar los traces del
proyecto (trace.json, trace_borde.json, trace_retroceso.json).

Uso:
    python probar_grafo.py                 # ingresar el grafo a mano
    python probar_grafo.py mi_grafo.txt    # leer el grafo de un archivo
    python probar_grafo.py --animar        # ademas, abrir la animacion Manim

Formato (el mismo que usa euler.cpp):
    n m        -> numero de vertices y numero de aristas
    u v        -> una arista por linea, vertices numerados de 0 a n-1

Archivos que genera:
    grafo_mio.txt   -> el grafo ingresado (solo en modo manual)
    trace_mio.json  -> la salida de euler.cpp para ese grafo
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
EXE = CARPETA / ('euler.exe' if os.name == 'nt' else 'euler')
CPP = CARPETA / 'euler.cpp'
GRAFO_SALIDA = CARPETA / 'grafo_mio.txt'
TRACE_SALIDA = CARPETA / 'trace_mio.json'
PROTEGIDOS = {'trace.json', 'trace_borde.json', 'trace_retroceso.json'}


def pedir_entero(mensaje, minimo=0):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor >= minimo:
                return valor
            print(f'  Debe ser un entero >= {minimo}.')
        except ValueError:
            print('  Escribe un numero entero.')


def leer_manual():
    print('Grafo NO dirigido. Los vertices se numeran desde 0.')
    n = pedir_entero('Numero de vertices (n): ', 1)
    m = pedir_entero('Numero de aristas (m): ', 0)
    aristas = []
    print(f'Escribe cada arista como "u v" (vertices entre 0 y {n - 1}):')
    while len(aristas) < m:
        partes = input(f'  Arista {len(aristas) + 1}/{m}: ').split()
        try:
            u, v = map(int, partes)
        except ValueError:
            print('  Formato: dos enteros separados por espacio, por ejemplo "0 1".')
            continue
        if not (0 <= u < n and 0 <= v < n):
            print(f'  Los vertices deben estar entre 0 y {n - 1}.')
            continue
        aristas.append((u, v))
    texto = f'{n} {m}\n' + ''.join(f'{u} {v}\n' for u, v in aristas)
    GRAFO_SALIDA.write_text(texto, encoding='utf-8')
    print(f'Grafo guardado en {GRAFO_SALIDA.name}')
    return texto, n, aristas


def leer_archivo(ruta):
    texto = Path(ruta).read_text(encoding='utf-8-sig')
    numeros = texto.split()
    try:
        n, m = int(numeros[0]), int(numeros[1])
        valores = list(map(int, numeros[2:2 + 2 * m]))
    except (IndexError, ValueError):
        sys.exit('Archivo invalido: la primera linea debe ser "n m" y luego m lineas "u v".')
    if len(valores) != 2 * m:
        sys.exit(f'Archivo invalido: se esperaban {m} aristas.')
    aristas = list(zip(valores[::2], valores[1::2]))
    for u, v in aristas:
        if not (0 <= u < n and 0 <= v < n):
            sys.exit(f'Archivo invalido: arista {u} {v} fuera de rango (0..{n - 1}).')
    return texto, n, aristas


def asegurar_ejecutable():
    if EXE.exists():
        return
    gpp = shutil.which('g++')
    if gpp is None:
        sys.exit('No se encontro euler.exe ni g++. Compila euler.cpp con g++ -std=c++17 (ver README).')
    print('Compilando euler.cpp ...')
    subprocess.run([gpp, '-std=c++17', '-O2', '-Wall', '-Wextra', str(CPP), '-o', str(EXE)], check=True)


def avisos_visualizacion(n, aristas):
    vistos = set()
    for u, v in aristas:
        if u == v:
            print(f'Aviso: hay un lazo ({u}-{v}). El C++ lo procesa, pero la animacion no lo dibuja bien.')
        clave = (min(u, v), max(u, v))
        if clave in vistos:
            print(f'Aviso: arista paralela {clave}. La animacion la dibujaria encima de la otra.')
        vistos.add(clave)
    if n > 10:
        print('Aviso: con mas de 10 vertices la animacion puede verse apretada.')


def main():
    args = [a for a in sys.argv[1:] if a != '--animar']
    animar = '--animar' in sys.argv[1:]

    texto, n, aristas = leer_archivo(args[0]) if args else leer_manual()
    assert TRACE_SALIDA.name not in PROTEGIDOS
    avisos_visualizacion(n, aristas)
    asegurar_ejecutable()

    resultado = subprocess.run([str(EXE)], input=texto, capture_output=True, text=True)
    if resultado.returncode != 0:
        sys.exit('euler.exe fallo: ' + resultado.stderr.strip())
    datos = json.loads(resultado.stdout)
    TRACE_SALIDA.write_text(resultado.stdout, encoding='utf-8')

    print()
    print(f'Grados: {datos["degrees"]}')
    print(datos['reason'])
    if datos['has_circuit']:
        print('Ciclo euleriano: ' + ' -> '.join(map(str, datos['circuit'])))
    print(f'Trace guardado en {TRACE_SALIDA.name} (los traces del proyecto no se modificaron).')

    if animar:
        entorno = dict(os.environ, EULER_TRACE=TRACE_SALIDA.name)
        subprocess.run([sys.executable, '-m', 'manim', '-pql', 'animacion.py', 'GrafoEuleriano'],
                       cwd=CARPETA, env=entorno)
    else:
        print('Para animarlo (PowerShell):')
        print(f'    $env:EULER_TRACE="{TRACE_SALIDA.name}"')
        print('    python -m manim -pql animacion.py GrafoEuleriano')


if __name__ == '__main__':
    main()
