"""Validador independiente de euler.exe.

Uso:  python validar_euler.py [ruta_a_euler.exe]

Comprueba casos de borde (grafo vacío, vértices aislados, grados impares,
no conexo, aristas paralelas, lazos), entradas inválidas, grafos aleatorios
y un grafo grande (tiempo lineal). Para cada salida verifica grados,
has_circuit, que circuit/edge_order formen un ciclo euleriano válido y que
los eventos reconstruyan exactamente el ciclo (lo mismo que hace Manim).
"""
import json
import random
import subprocess
import sys
import time
from pathlib import Path

EXE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / 'euler.exe'


def correr(texto):
    p = subprocess.run([str(EXE)], input=texto, capture_output=True, text=True)
    return p.returncode, p.stdout


def esperado(n, aristas):
    grado = [0] * n
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for u, v in aristas:
        grado[u] += 1
        grado[v] += 1
        padre[raiz(u)] = raiz(v)
    con_aristas = {raiz(i) for i in range(n) if grado[i] > 0}
    ok = bool(aristas) and all(g % 2 == 0 for g in grado) and len(con_aristas) <= 1
    return grado, ok


def validar(n, aristas, nombre):
    entrada = f'{n} {len(aristas)}\n' + ''.join(f'{u} {v}\n' for u, v in aristas)
    rc, out = correr(entrada)
    assert rc == 0, f'{nombre}: código de salida {rc}'
    d = json.loads(out)
    grado, ok = esperado(n, aristas)
    assert d['n'] == n and d['edges'] == [list(e) for e in aristas], nombre
    assert d['degrees'] == grado, f'{nombre}: grados'
    assert d['has_circuit'] == ok, f'{nombre}: has_circuit={d["has_circuit"]}, esperado {ok}'
    c, eo, ev = d['circuit'], d['edge_order'], d['events']
    if not ok:
        assert c == [] and eo == [] and ev == [], f'{nombre}: salida no vacía sin ciclo'
        return d
    m = len(aristas)
    assert len(c) == m + 1 and c[0] == c[-1], f'{nombre}: longitud/cierre del ciclo'
    assert sorted(eo) == list(range(m)), f'{nombre}: edge_order no usa cada arista una vez'
    for i, e in enumerate(eo):
        assert sorted(aristas[e]) == sorted((c[i], c[i + 1])), f'{nombre}: arista {e} no une {c[i]}-{c[i+1]}'
    # Reproducir eventos igual que animacion.py
    pila, salida, usadas = [], [], set()
    assert ev[0]['type'] == 'start' and ev[-1]['type'] == 'reverse'
    for e in ev:
        t = e['type']
        if t == 'start':
            pila.append(e['u'])
        elif t == 'traverse':
            assert pila[-1] == e['u'] and e['edge'] not in usadas
            assert sorted(aristas[e['edge']]) == sorted((e['u'], e['v']))
            usadas.add(e['edge'])
            pila.append(e['v'])
        elif t == 'finish':
            assert pila[-1] == e['u']
            pila.pop()
            salida.append(e['u'])
        elif t == 'reverse':
            salida.reverse()
    assert not pila and salida == c, f'{nombre}: los eventos no reconstruyen el ciclo'
    return d


def main():
    assert EXE.exists(), f'No existe {EXE}; compila primero euler.cpp'
    casos = {
        'vacio n=0': (0, []),
        'solo aislados': (4, []),
        'aislados + triangulo': (6, [(1, 2), (2, 3), (3, 1)]),
        'grado impar (camino)': (3, [(0, 1), (1, 2)]),
        'no conexo (2 triangulos)': (6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]),
        'paralelas': (2, [(0, 1), (0, 1)]),
        'paralelas impar': (2, [(0, 1), (0, 1), (0, 1)]),
        'un lazo': (1, [(0, 0)]),
        'lazo + aislado': (3, [(1, 1)]),
        'lazos y paralelas': (3, [(0, 0), (0, 1), (1, 1), (1, 0), (2, 2), (1, 2), (2, 1)]),
        'lazo desconectado': (3, [(0, 1), (1, 0), (2, 2)]),
    }
    for nombre, (n, a) in casos.items():
        validar(n, a, nombre)
        print(f'OK  {nombre}')

    for nombre, entrada in {'vertice fuera de rango': '2 1\n0 2\n',
                            'negativo': '-1 0\n', 'truncada': '3 2\n0 1\n',
                            'vacia': ''}.items():
        rc, out = correr(entrada)
        assert rc != 0 and out == '', f'{nombre}: debería rechazarse'
        print(f'OK  entrada inválida: {nombre}')

    rnd = random.Random(2023)
    con_ciclo = 0
    for i in range(400):
        n = rnd.randint(1, 8)
        a = [(rnd.randrange(n), rnd.randrange(n)) for _ in range(rnd.randint(0, 12))]
        if rnd.random() < 0.5 and a:  # forzar a menudo grados pares duplicando
            a = a + a
        con_ciclo += validar(n, a, f'aleatorio #{i}')['has_circuit']
    print(f'OK  400 grafos aleatorios ({con_ciclo} con ciclo)')

    for n in (100_000, 400_000):
        a = [(i, (i + 1) % n) for i in range(n)] + [(i, (i + 2) % n) for i in range(n)]
        t0 = time.perf_counter()
        validar(n, a, f'grande n={n}')
        print(f'OK  grande V={n}, E={len(a)}: {time.perf_counter() - t0:.2f}s (incluye validación)')
    print('Todas las pruebas pasaron.')


if __name__ == '__main__':
    main()
