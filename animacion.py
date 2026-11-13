from manim import *
import json
from pathlib import Path
import os
import numpy as np


class GrafoEuleriano(Scene):
    def construct(self):
        ruta = Path(__file__).resolve().parent / os.environ.get('EULER_TRACE', 'trace.json')
        datos = json.loads(ruta.read_text(encoding='utf-8-sig'))
        self.camera.background_color = '#101827'

        def texto(s, punto, ancho=6, color=WHITE, tam=26):
            t = Text(s, font_size=tam, color=color)
            if t.width > ancho:
                t.scale_to_fit_width(ancho)
            return t.move_to(punto)

        titulo = texto('Hierholzer: construyendo el ciclo', [0, 3.45, 0], 12, tam=36)
        self.play(Write(titulo))
        n = datos['n']
        if n == 5:
            pos = {0: [-3.4, 0, 0], 1: [-5.6, 1.5, 0],
                   2: [-5.6, -1.5, 0], 3: [-1.2, 1.5, 0], 4: [-1.2, -1.5, 0]}
        else:
            pos = {i: [-3.4 + 2.2 * np.cos(TAU*i/max(n, 1)),
                       2 * np.sin(TAU*i/max(n, 1)), 0] for i in range(n)}
        aristas = VGroup(*[Line(pos[u], pos[v], buff=0.26, color=GRAY, stroke_width=4)
                           for u, v in datos['edges']])
        nodos = VGroup()
        for i in range(n):
            c = Circle(radius=0.26, color=BLUE, fill_opacity=1).move_to(pos[i])
            t = Text(str(i), font_size=22).move_to(c)
            nodos.add(VGroup(c, t))
        self.play(Create(aristas), FadeIn(nodos))
        aviso = texto('Verificamos conectividad y grados pares', [0, -3.25, 0], 12)
        self.play(Write(aviso))
        grados = texto('Grados: ' + ', '.join(map(str, datos['degrees'])), [3.5, 2.3, 0])
        self.play(Write(grados))
        self.wait(2)
        if not datos['has_circuit']:
            self.play(Transform(aviso, texto(datos['reason'], [0, -3.25, 0], 12, RED)))
            self.wait(4)
            return
        if 'events' not in datos:
            raise ValueError('Este JSON es antiguo: usa el nuevo trace.json con events.')
        self.play(FadeOut(grados))
        pila_label = texto('Pila (tope a la derecha)', [3.5, 2.1, 0])
        salida_label = texto('Salida provisional', [3.5, 0.1, 0])
        pila_text = texto('[]', [3.5, 1.35, 0])
        salida_text = texto('[]', [3.5, -0.65, 0])
        self.play(Write(pila_label), Write(salida_label), Write(pila_text), Write(salida_text))
        pila, salida = [], []
        marcador = Circle(radius=0.36, color=YELLOW, stroke_width=4)
        for ev in datos['events']:
            tipo, u = ev['type'], ev['u']
            if tipo == 'start':
                pila.append(u)
                marcador.move_to(pos[u])
                self.play(Create(marcador))
                mensaje = f'Comenzamos en el vertice {u}'
            elif tipo == 'traverse':
                v, eid = ev['v'], ev['edge']
                pila.append(v)
                mensaje = f'Usamos la arista {u} - {v} y apilamos {v}'
                self.play(aristas[eid].animate.set_color(GREEN),
                          marcador.animate.move_to(pos[v]), run_time=0.8)
            elif tipo == 'finish':
                assert pila[-1] == u
                pila.pop()
                salida.append(u)
                mensaje = f'{u} no tiene aristas libres: desapilamos y guardamos {u}'
                if pila:
                    # Retorno de control: NO se vuelve a recorrer una arista.
                    self.play(FadeOut(marcador), run_time=0.2)
                    marcador.move_to(pos[pila[-1]])
                    self.play(FadeIn(marcador), run_time=0.2)
                else:
                    self.play(FadeOut(marcador), run_time=0.2)
            elif tipo == 'reverse':
                salida.reverse()
                assert salida == datos['circuit']
                mensaje = 'Invertimos la salida provisional: este es el ciclo euleriano'
                self.play(Transform(salida_label, texto('Ciclo final', [3.5, 0.1, 0], color=GREEN)))
            else:
                raise ValueError(f'Evento desconocido: {tipo}')
            self.play(
                Transform(pila_text, texto(str(pila), [3.5, 1.35, 0])),
                Transform(salida_text, texto(' → '.join(map(str, salida)) or '[]', [3.5, -0.65, 0])),
                Transform(aviso, texto(mensaje, [0, -3.25, 0], 12)),
                run_time=0.4)
            self.wait(0.8)
        self.wait(3)
