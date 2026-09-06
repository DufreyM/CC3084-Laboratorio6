# %% [markdown]
# # Laboratorio 6 - Ejercicio 10 y ensamblaje del informe final
# **Autor de esta seccion:** Leonardo Mejia
#
# Escribe la seccion 10 (interpretacion, limitaciones y conclusiones) y concatena
# todos los `outputs/reporte_ejercicio_*.md` generados por los notebooks 01-06 en
# un unico `outputs/informe_final.md`, que luego se convierte a
# `outputs/informe_final.pdf`.

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"

# %% [markdown]
# ## 10. Interpretacion, limitaciones y conclusiones

# %%
seccion_10 = """
## 10. Interpretacion, limitaciones y conclusiones

### 10.1 Los hallazgos en el contexto de participacion y consumo en YouTube

Este dataset no describe "la audiencia de YouTube en Guatemala": describe la
participacion observada en los comentarios de **19 videos de 293 recolectados**,
casi todos de tematica politica/noticiosa. Dentro de esa ventana, el patron mas
claro es que **ver un video y comentarlo son comportamientos distintos**: el video
mas visto del subconjunto (Plan 2032 Ciudad de Guatemala, ~304 mil vistas) no es
el mas comentado, y viceversa (Que rico come tu diputado, ~11.8 mil vistas, 161
comentarios). Esto sugiere que comentar en este corpus esta ligado a la
indignacion/controversia del contenido (escandalos de corrupcion, gastos
publicos) mas que al alcance/popularidad general del video.

La estructura de red confirma la misma historia desde otro angulo: la
participacion se concentra en un componente gigante alrededor de un solo video
("Que rico come tu diputado", que domina grado, intermediacion y PageRank), y el
resto son 9 audiencias-isla que nunca se cruzan entre si. Esto es consistente con
una dinamica de "indignacion viral puntual" mas que con una comunidad estable de
comentaristas politicos que sigue multiples contenidos.

### 10.2 Limitaciones

- **Cobertura de comentarios**: solo 19 de 293 videos (6.5%) tienen algun
  comentario en el dataset, y de esos, la mitad del volumen de comentarios viene
  de un solo video. No se puede asumir que los otros 274 videos no reciben
  comentarios en la realidad; simplemente no fueron recolectados aqui.
- **Seleccion por consultas de busqueda (`source_query`/`source_group`)**: el
  metodo de muestreo (topic vs. channel) determino que tipo de contenido entro al
  dataset; el ejercicio 3.6 muestra que el like promedio por comentario difiere
  6x entre ambos grupos (6.32 vs. 0.72), evidencia de que el metodo de
  recoleccion, no solo el contenido, explica parte de los patrones observados.
- **Fechas relativas**: `published_text` de los comentarios ("hace 2 años") no es
  una fecha exacta y depende del momento de scraping; no se pudo, por ejemplo,
  ordenar comentarios cronologicamente con precision ni analizar series de tiempo
  reales de participacion.
- **Conteos observados al momento de recoleccion**: `view_count`, `like_count` y
  `reply_count` son una fotografia de un instante, no el estado actual; dos
  videos "iguales" en el dataset pueden haber sido scrapeados en momentos muy
  distintos de su ciclo de vida (recien publicado vs. con años online).
- **Falta de relaciones explicitas entre autores**: como advierte el enunciado,
  `reply_count` no identifica a quien respondio; toda arista construida en este
  laboratorio es co-participacion (mismo video), nunca conversacion directa. El
  hallazgo de 36/406 `comment_id` con formato de respuesta de YouTube
  (`looks_like_reply_id`, ejercicio 2.1) sugiere ademas que el propio proceso de
  recoleccion mezclo accidentalmente algunas respuestas dentro del archivo de
  "comentarios principales", lo cual pudo inflar levemente algunos pesos de
  arista (ver ejercicio 4.1).
- **Concentracion extrema en pocos videos**: el top 10 de videos concentra 93.6%
  de los comentarios (ejercicio 3.2); cualquier metrica de red, sentimiento o
  tema esta dominada por el puñado de videos mas controversiales, no por una
  muestra equilibrada de contenido guatemalteco en YouTube.

### 10.3 Descripcion, asociacion e inferencia

Lo que se puede afirmar como **descripcion**: en esta muestra de 406 comentarios
sobre 19 videos, el 61.3% del texto fue clasificado como negativo, la red esta
dominada por un componente gigante alrededor de un video, y existen 17
comunidades detectadas por Louvain con modularidad 0.777.

Lo que se puede afirmar como **asociacion** (correlacional, no causal): los
videos encontrados por busqueda tematica muestran mas "me gusta" promedio por
comentario que los encontrados navegando canales directamente; los comentarios
editados muestran, en esta muestra pequeña (18 casos), menos likes promedio que
los no editados.

Lo que **NO se puede inferir** de estos datos: que la opinion publica
guatemalteca sobre sus politicos es mayoritariamente negativa (el sesgo de
seleccion hacia contenido de escandalo lo garantiza casi por diseño); que existe
una "comunidad de comentaristas politicos" cohesionada en YouTube Guatemala (lo
que se observa es, en su mayoria, 19 audiencias en gran parte aisladas, no una
comunidad); ni que los patrones de sentimiento/participacion de estos 332
autores generalizan a la poblacion de usuarios de YouTube en Guatemala o a la
poblacion del pais. El dataset es una muestra dirigida (por consultas de
busqueda especificas), no una muestra aleatoria ni censal.

### 10.4 Conclusiones integradas

Redes, contenido, sentimiento y limitaciones cuentan la misma historia desde
distintos angulos: este es un corpus **pequeño, sesgado hacia escandalo
politico-institucional, y estructuralmente fragmentado**. La red bipartita
autor-video (ejercicio 4) y sus proyecciones (ejercicio 5) muestran una
topologia de "un hub gigante + 9 islas" (ejercicio 6); la deteccion de
comunidades (ejercicio 7) recupera basicamente esa misma fragmentacion, con la
excepcion notable de una comunidad que fusiona 3 videos de contenido de
consumidor/servicios de Quorum, sugiriendo una audiencia fiel a ese tipo de
periodismo especifico, distinta de la audiencia mas amplia y volatil del
escandalo viral. La centralidad (ejercicio 8) identifica un puñado de autores y
videos "puente" cuya remocion fragmentaria aun mas la red, perfiles utiles
para entender que sostiene la (poca) conectividad del dataset. El analisis de
sentimiento (ejercicio 9) no contradice nada de esto: el tono negativo
predominante se explica mejor por que TEMA se recolecto (corrupcion, gasto
publico) que por un animo generalizado, como lo demuestra el contraejemplo
claro del video municipal de proyeccion urbana, mayoritariamente positivo. En
conjunto, los resultados son validos como descripcion de esta muestra especifica
y como ejercicio metodologico de analisis de redes sociales, pero no deben
leerse como un retrato representativo de YouTube Guatemala ni de la opinion
publica del pais.
"""

path_10 = OUTPUTS / "reporte_ejercicio_10.md"
path_10.write_text(seccion_10, encoding="utf-8")
print(f"Ejercicio 10 guardado en {path_10}")

# %% [markdown]
# ## Ensamblaje del informe final (Markdown)

# %%
FIGS = OUTPUTS / "figs"


def img(name):
    return f'\n\n![{name}]({(FIGS / name).as_posix()})\n'


orden = [
    ("4", "Ejercicio 4 - Construccion de la red bipartita autor-video",
     [img("09_red_bipartita_completa.png")]),
    ("3", "Ejercicio 3 - Analisis exploratorio",
     [img(f"{n:02d}_{s}.png") for n, s in [
         (1, "top_canales_comentarios"), (2, "top_videos_comentarios"),
         (3, "histograma_views"), (4, "categorias_video_vs_comentario"),
         (5, "scatter_views_vs_comentarios"), (6, "top_palabras"),
         (7, "top_bigramas"), (8, "wordcloud")]]),
    ("5_6", "Ejercicios 5 y 6 - Proyecciones, topologia y fragmentacion",
     [img("10_proyeccion_autor_autor.png"), img("11_proyeccion_autor_autor_filtrada.png"),
      img("12_proyeccion_video_video.png")]),
    ("7_8", "Ejercicios 7 y 8 - Comunidades, centralidad y puentes",
     [img("13_comunidades.png")]),
    ("9", "Ejercicio 9 - Contenido y sentimiento", [img("14_sentimiento_por_video.png")]),
    ("10", "Ejercicio 10 - Interpretacion, limitaciones y conclusiones", []),
]

partes = [
    "# Laboratorio 6 - Analisis de redes sociales en YouTube (Guatemala)\n",
    "**Equipo:** Leonardo Mejia, Maria Jose, Mia Fuentes | CC3084 - Data Science, UVG\n",
    "**Repositorio:** https://github.com/DufreyM/CC3084-Laboratorio6\n",
    "\n## Ejercicios 1 y 2 - Carga, integracion, calidad y limpieza\n",
]
partes.append((OUTPUTS / "reporte_ejercicio_1_2.md").read_text(encoding="utf-8"))

for suf, titulo, imagenes in orden:
    p = OUTPUTS / f"reporte_ejercicio_{suf}.md"
    if p.exists():
        contenido = p.read_text(encoding="utf-8")
        if not contenido.strip().startswith(("#", "##")):
            partes.append(f"## {titulo}\n")
        partes.append(contenido)
        partes.extend(imagenes)

informe_md = "\n".join(partes)

# %% [markdown]
# ## Limpieza tipografica: sin backticks, sin "~", sin guiones/rayas largas ni
# lineas horizontales de separacion (todo debe leerse como texto corrido normal).

# %%
import re

informe_md = informe_md.replace("`", "")
informe_md = re.sub(r"(?m)^-{3,}\s*$", "", informe_md)  # lineas "---" (rayas horizontales)
informe_md = re.sub(r"[‒–—―]", ",", informe_md)  # em/en dash unicode
informe_md = re.sub(r"\s+--+\s+", ", ", informe_md)  # "--" usado como raya
informe_md = re.sub(r"~(\d)", r"aprox. \1", informe_md)  # "~304" -> "aprox. 304"
informe_md = informe_md.replace("~", "")

informe_path = OUTPUTS / "informe_final.md"
informe_path.write_text(informe_md, encoding="utf-8")
print(f"Informe consolidado guardado en {informe_path} ({len(informe_md)} caracteres)")

# %% [markdown]
# ## Conversion a PDF: Times New Roman, blanco y negro, titulos en negrita negra

# %%
import markdown as md_lib
from xhtml2pdf import pisa

html_body = md_lib.markdown(informe_md, extensions=["tables", "nl2br"])
html_full = f"""<html><head><meta charset="utf-8"><style>
* {{ color: #000000 !important; }}
body {{ font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.4;
        color: #000000; background: #ffffff; }}
h1 {{ font-size: 20pt; font-weight: bold; margin-top: 16pt; }}
h2 {{ font-size: 16pt; font-weight: bold; margin-top: 16pt; }}
h3 {{ font-size: 13pt; font-weight: bold; margin-top: 12pt; }}
img {{ max-width: 480px; display: block; margin: 8px auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: 11pt; }}
td, th {{ border: 1px solid #000000; padding: 3px; }}
</style></head><body>{html_body}</body></html>"""

pdf_path = OUTPUTS / "informe_final.pdf"
with open(pdf_path, "wb") as f:
    result = pisa.CreatePDF(html_full, dest=f)

print(f"PDF generado en {pdf_path} (errores: {result.err})")
