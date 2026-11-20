# Video final del ciclo euleriano

## Instalar el complemento sin reemplazar archivos

Copiar únicamente video_final.py a la carpeta del proyecto, junto a animacion.py, trace_retroceso.json y trace_borde.json. Los archivos originales quedan intactos. No copiar el complemento dentro de .venv.

El archivo nuevo importa la escena original y la ejecuta dos veces, una por cada JSON. Las introducciones y el cierre son nuevos. No cambia el algoritmo, las trazas, el informe, el README ni el MP4 anterior.

## Renderizar

Desde la terminal donde ya funciona Manim:

```powershell
python -m manim -pql video_final.py VideoFinal
```

Revisar la versión de prueba y después generar la entrega en alta resolución:

```powershell
python -m manim -pqh video_final.py VideoFinal
```

Salida habitual de la versión final:

media/videos/video_final/1080p60/VideoFinal.mp4

Esta ruta es distinta de la del video de avance. No es necesario recompilar C++: se usan las trazas que ya generó el grupo. La selección de ejemplos se hace dentro del complemento y se restaura el valor previo de EULER_TRACE al terminar.

## Voz

La animación contiene explicaciones escritas y puede renderizarse sin audio. Para añadir tu voz:

1. Renderizar primero la versión de prueba.
2. Abrir el video y grabar la lectura de GUION_NARRACION.txt respetando los cambios de escena. Puede haber silencios mientras se observa el recorrido.
3. Guardar o exportar la grabación completa como narracion_final.wav (un archivo WAV real, no un MP3 renombrado) junto a video_final.py.
4. Repetir el comando de renderizado. El complemento detecta ese archivo y lo añade desde el inicio.

La voz no se genera automáticamente. Como alternativa, añadir la narración en un editor y exportar a 1920 x 1080. No usar el MP4 de 480p como fuente para la entrega final si se puede renderizar en 1080p.

## Contenido y tiempos aproximados

| Escena | Inicio aproximado | Duración |
|---|---|---|
| Portada con integrantes | 00:00 | 13 s |
| Motivación | 00:13 | 25 s |
| Definición y condiciones | 00:38 | 26 s |
| Cómo seguir el algoritmo | 01:04 | 21 s |
| Ejecución original con retrocesos | 01:25 | 43 s |
| Caso de borde original | 02:08 | 17 s |
| Explicación del caso de borde | 02:25 | 15 s |
| Complejidad | 02:40 | 22 s |
| Cierre y créditos | 03:02 | 12 s |

Duración prevista: aproximadamente 3 min 14 s. Los tiempos pueden variar por redondeo de fotogramas y configuración de Manim. La referencia definitiva es el video renderizado.

## Verificación y límites

Se verificó la sintaxis del complemento y la compatibilidad de nombres de escena, eventos y archivos con el ZIP del grupo. Los archivos del ZIP original se conservaron sin cambios. No fue posible renderizar Manim en el entorno de preparación: verificar en tu equipo que los textos se vean completos y ajustar la narración al MP4 resultante.

La escena original conserva su diseño y ritmo. En ella hay breves transiciones donde el marcador cambia antes que el texto; el complemento no modifica ese comportamiento.

## Entrega del proyecto

Añadir video_final.py al repositorio con un commit real. Para reproducir la versión narrada, añadir también el audio o documentar dónde obtenerlo. El informe y README originales no fueron modificados: el grupo aún debe completar sus enlaces reales y actualizar el informe de avance. El video nuevo incluye nombres, motivación, concepto, demostración real, caso de borde y complejidad; luego se debe subir el MP4 y verificar su enlace.
