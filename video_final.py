"""Video educativo completo. Se añade junto a animacion.py; no lo modifica.
Renderizar: python -m manim -pqh video_final.py VideoFinal
Opcional: colocar narracion_final.wav junto a este archivo para añadir la voz.
"""
from manim import *
from pathlib import Path
import json
import os
import animacion as base

RAIZ = Path(__file__).resolve().parent
FONDO = '#101827'
TINTA = '#EDF2F7'
ACENTO = '#56D6D0'
SUAVE = '#9CAFC5'
NOMBRES = [
    'Ucañani Tintaya, Miguel Fernando',
    'Benites Camacho, Alonso Aarón',
    'Ortiz Palomino, David Alonso',
]


class VideoFinal(base.GrafoEuleriano):
    def letra(self, contenido, tam=30, color=TINTA, ancho=12):
        objeto = Text(contenido, font='Arial', font_size=tam, color=color)
        if objeto.width > ancho:
            objeto.scale_to_fit_width(ancho)
        return objeto

    def encabezado(self, numero, titulo):
        etiqueta = self.letra(numero, 19, ACENTO).move_to([-5.4, 3.45, 0])
        texto = self.letra(titulo, 37).move_to([0, 2.75, 0])
        linea = Line([-6, 2.25, 0], [6, 2.25, 0], color=SUAVE, stroke_opacity=0.3)
        self.play(FadeIn(etiqueta), Write(texto), Create(linea), run_time=1.3)

    def limpiar(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.7)

    def bloque(self, titulo, detalle, y, color=ACENTO):
        encabezado = self.letra(titulo, 30, color).move_to([0, y, 0])
        cuerpo = self.letra(detalle, 24).next_to(encabezado, DOWN, buff=0.2)
        self.play(FadeIn(encabezado, shift=UP*0.1), FadeIn(cuerpo), run_time=1)

    def demo_original(self, archivo):
        # Reutiliza exactamente la escena del compañero y sus JSON.
        anterior = os.environ.get('EULER_TRACE')
        os.environ['EULER_TRACE'] = archivo
        try:
            super().construct()
        finally:
            if anterior is None:
                os.environ.pop('EULER_TRACE', None)
            else:
                os.environ['EULER_TRACE'] = anterior

    def construct(self):
        for nombre in ('trace_retroceso.json', 'trace_borde.json'):
            if not (RAIZ / nombre).is_file():
                raise FileNotFoundError(f'Falta {nombre}: copia video_final.py junto a los archivos del proyecto.')
        self.camera.background_color = FONDO
        voz = RAIZ / 'narracion_final.wav'
        if voz.exists():
            self.add_sound(str(voz))

        # 1. Portada y nombres completos.
        curso = self.letra('ALGORITMOS Y ESTRUCTURAS DE DATOS · CS2023', 20, ACENTO).move_to([0, 2.7, 0])
        titulo = self.letra('Ciclo euleriano', 60).move_to([0, 1.65, 0])
        subtitulo = self.letra('El algoritmo de Hierholzer, paso a paso', 28, SUAVE).move_to([0, 0.7, 0])
        nombres = VGroup(*[self.letra(n, 25) for n in NOMBRES]).arrange(DOWN, buff=0.28).move_to([0, -1, 0])
        self.play(FadeIn(curso), Write(titulo), run_time=1.5)
        self.play(FadeIn(subtitulo), FadeIn(nombres), run_time=1)
        self.wait(10)
        self.limpiar()

        # 2. Motivación: un mapa abstracto, sin inventar pasos del algoritmo.
        self.encabezado('01 / PROBLEMA', '¿Podemos recorrer todas las calles una sola vez?')
        datos = json.loads((RAIZ / 'trace_retroceso.json').read_text(encoding='utf-8-sig'))
        posiciones = {0: [-1.2, 0, 0], 1: [1.3, 0, 0], 2: [0.05, 1.5, 0],
                      3: [3.7, 1.5, 0], 4: [3.7, -1.5, 0]}
        lineas = VGroup(*[Line(posiciones[u], posiciones[v], color=SUAVE, stroke_width=6)
                          for u, v in datos['edges']])
        puntos = VGroup(*[Dot(posiciones[i], radius=0.12, color=ACENTO) for i in range(datos['n'])])
        mapa = VGroup(lineas, puntos).scale(0.85).move_to([2.8, -0.15, 0])
        explicacion = VGroup(
            self.letra('Intersecciones → vértices', 25, ancho=5.6),
            self.letra('Calles → aristas', 25, ancho=5.6),
            self.letra('Meta: regresar al inicio', 25, ACENTO, ancho=5.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-3.5, 0, 0])
        self.play(Create(mapa), FadeIn(explicacion), run_time=2)
        self.wait(16)
        nota = self.letra('La posibilidad depende de la estructura del grafo.', 24, SUAVE).move_to([0, -2.65, 0])
        self.play(FadeIn(nota))
        self.wait(4)
        self.limpiar()

        # 3. Definición y condiciones (caso no dirigido con alguna arista).
        self.encabezado('02 / CONCEPTO', '¿Qué es un ciclo euleriano?')
        self.bloque('Cada arista, exactamente una vez', 'El recorrido termina en el vértice donde comenzó.', 1.3)
        self.wait(6)
        self.bloque('Los vértices sí pueden repetirse', 'Lo que no se repite es una arista.', -0.1)
        self.wait(5)
        self.bloque('¿Cuándo existe?', 'Grados pares y todos los vértices con aristas conectados.', -1.6)
        self.wait(10)
        self.limpiar()

        # 4. Preparación para interpretar la ejecución original.
        self.encabezado('03 / MÉTODO', 'Tres ideas para seguir a Hierholzer')
        self.bloque('1. Avanzar', 'Usar una arista libre y apilar el vértice de destino.', 1.3)
        self.wait(5)
        self.bloque('2. Retroceder', 'Sin aristas libres: desapilar y guardar en la salida provisional.', -0.1)
        self.wait(6)
        self.bloque('3. Invertir', 'Al vaciar la pila, invertir la salida para obtener el ciclo.', -1.6)
        self.wait(5)
        self.limpiar()

        # 5. Demostración real: código del compañero, sin cambios.
        self.demo_original('trace_retroceso.json')
        self.limpiar()

        # 6. Caso de borde real: JSON producido por C++.
        self.demo_original('trace_borde.json')
        self.wait(5)
        self.limpiar()
        self.encabezado('04 / CASO DE BORDE', 'Un camino no siempre forma un ciclo')
        self.bloque('0 — 1 — 2', 'Grados: 1, 2, 1. Los extremos tienen grado impar.', 0.9, RED)
        self.wait(6)
        self.bloque('Se puede ir de 0 a 2', 'Pero no regresar a 0 sin repetir alguna arista.', -0.9)
        self.wait(5)
        self.limpiar()

        # 7. Complejidad del motor; no confundirla con renderizar el video.
        self.encabezado('05 / EFICIENCIA', 'Tiempo O(V + E) · Memoria O(V + E)')
        self.bloque('V = vértices · E = aristas', 'Las listas de adyacencia ocupan espacio proporcional al grafo.', 1.3)
        self.wait(5)
        self.bloque('Cada arista se utiliza una sola vez', 'Los punteros avanzan; no reinician la búsqueda en cada paso.', -0.1)
        self.wait(6)
        self.bloque('La pila y los eventos también son lineales', 'Este análisis corresponde al algoritmo C++, no al renderizado.', -1.6)
        self.wait(6)
        self.limpiar()

        # 8. Cierre y créditos.
        titulo = self.letra('Todas las aristas. Un recorrido cerrado.', 39, ACENTO).move_to([0, 2.5, 0])
        detalle = self.letra('Hierholzer construye el ciclo en tiempo lineal.', 27).move_to([0, 1.55, 0])
        nombres = VGroup(*[self.letra(n, 25) for n in NOMBRES]).arrange(DOWN, buff=0.25).move_to([0, -0.1, 0])
        fuentes = self.letra('Referencias: Hierholzer (1873) · Manim Community · Material del curso', 18, SUAVE).move_to([0, -2.0, 0])
        self.play(Write(titulo), FadeIn(detalle), run_time=1.5)
        self.play(FadeIn(nombres), FadeIn(fuentes))
        self.wait(9)
