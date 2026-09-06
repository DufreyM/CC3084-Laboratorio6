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

_fig_counter = [0]


def fig(name, caption):
    """Imagen + leyenda numerada debajo (Figura N. <caption>), como bloque HTML
    para que quede centrada y con estilo de leyenda sin depender de markdown."""
    _fig_counter[0] += 1
    src = (FIGS / name).as_posix()
    return (
        f'\n\n<div class="figura">'
        f'<img src="{src}">'
        f'<p class="leyenda">Figura {_fig_counter[0]}. {caption}</p>'
        f"</div>\n\n"
    )


orden = [
    ("4", "Ejercicio 4 - Construccion de la red bipartita autor-video",
     [fig("09_red_bipartita_completa.png",
          "Red bipartita autor-video completa: autores (circulos pequenos) y "
          "videos (circulos grandes, etiquetados con su titulo).")]),
    ("3", "Ejercicio 3 - Analisis exploratorio",
     [fig("01_top_canales_comentarios.png",
          "Top 10 canales por numero de comentarios recibidos."),
      fig("02_top_videos_comentarios.png",
          "Top 10 videos por numero de comentarios."),
      fig("03_histograma_views.png",
          "Distribucion de visualizaciones por video (293 videos, escala logaritmica)."),
      fig("04_categorias_video_vs_comentario.png",
          "Comparacion de la categoria de video: porcentaje de videos vs. "
          "porcentaje de comentarios que aporta cada categoria."),
      fig("05_scatter_views_vs_comentarios.png",
          "Popularidad (vistas) vs. participacion (numero de comentarios) por video."),
      fig("06_top_palabras.png",
          "15 palabras mas frecuentes en los comentarios, tras la limpieza de texto."),
      fig("07_top_bigramas.png",
          "15 bigramas (pares de palabras consecutivas) mas frecuentes en los comentarios."),
      fig("08_wordcloud.png",
          "Nube de palabras de los comentarios (texto limpio), como complemento visual.")]),
    ("5_6", "Ejercicios 5 y 6 - Proyecciones, topologia y fragmentacion",
     [fig("10_proyeccion_autor_autor.png",
          "Proyeccion autor-autor completa (arista si dos autores comentaron el "
          "mismo video, peso = numero de videos compartidos)."),
      fig("11_proyeccion_autor_autor_filtrada.png",
          "Proyeccion autor-autor filtrada: unicamente los pares de autores que "
          "comparten 2 o mas videos (participacion cruzada genuina)."),
      fig("12_proyeccion_video_video.png",
          "Proyeccion video-video (arista si dos videos comparten al menos un "
          "autor, peso = numero de autores compartidos).")]),
    ("7_8", "Ejercicios 7 y 8 - Comunidades, centralidad y puentes",
     [fig("13_comunidades.png",
          "Comunidades detectadas con el algoritmo de Louvain sobre la red "
          "bipartita (cada color es una comunidad distinta).")]),
    ("9", "Ejercicio 9 - Contenido y sentimiento",
     [fig("14_sentimiento_por_video.png",
          "Proporcion de comentarios negativos, neutros y positivos por video "
          "(videos con 10 o mas comentarios).")]),
    ("10", "Ejercicio 10 - Interpretacion, limitaciones y conclusiones", []),
]

partes = [
    "# Laboratorio 6\n",
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

caratula = """
<div style="text-align: center; margin-top: 60pt;">
<p style="text-align: center; font-size: 15pt; font-weight: bold;">UNIVERSIDAD DEL VALLE DE GUATEMALA</p>
<p style="text-align: center; font-size: 13pt;">Data Science</p>
<p style="text-align: center; font-size: 13pt;">Seccion - 20</p>
<p style="text-align: center; margin-top: 70pt; font-size: 16pt; font-weight: bold;">Laboratorio 6</p>
<p style="text-align: center; font-size: 14pt;">Informe</p>
<p style="text-align: center; font-size: 12pt;">Analisis de redes sociales en YouTube (Guatemala)</p>
<p style="text-align: center; margin-top: 70pt; font-size: 12pt;">Leonardo Dufrey Mejia Mejia<br>
Maria Jose Giron Isidro<br>
Mia Alejandra Fuentes Merida</p>
<p style="text-align: center; margin-top: 70pt; font-size: 12pt;">26 de julio de 2026</p>
</div>
<p style="page-break-after: always;"></p>
"""

html_body = md_lib.markdown(informe_md, extensions=["tables", "nl2br"])
html_full = f"""<html><head><meta charset="utf-8"><style>
@page {{
    size: letter portrait;
    margin: 2.2cm 2cm 2cm 2cm;
    @frame footer_frame {{
        -pdf-frame-content: footer_content;
        bottom: 1cm; margin-left: 2cm; margin-right: 2cm; height: 1cm;
    }}
}}
* {{ color: #000000 !important; }}
body {{ font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 1.45;
        color: #000000; background: #ffffff; }}
h1 {{ font-size: 20pt; font-weight: bold; margin-top: 16pt; margin-bottom: 10pt; }}
h2 {{ font-size: 16pt; font-weight: bold; margin-top: 20pt; margin-bottom: 8pt; }}
h3 {{ font-size: 13pt; font-weight: bold; margin-top: 14pt; margin-bottom: 6pt; }}
p, li {{ text-align: justify; margin-bottom: 6pt; }}
ul, ol {{ margin-bottom: 10pt; }}
.figura {{ text-align: center; margin: 16pt 0; }}
.figura img {{ max-width: 420px; }}
.leyenda {{ font-style: italic; font-size: 10pt; text-align: center; margin-top: 4pt; }}
table {{ border-collapse: collapse; width: 100%; font-size: 11pt; margin-bottom: 10pt; }}
td, th {{ border: 1px solid #000000; padding: 3px; text-align: left; }}
#footer_content {{ text-align: center; font-size: 9pt; }}
</style></head><body>
{caratula}
<div id="footer_content">Pagina <pdf:pagenumber> de <pdf:pagecount></div>
{html_body}
</body></html>"""

pdf_path = OUTPUTS / "informe_final.pdf"
with open(pdf_path, "wb") as f:
    result = pisa.CreatePDF(html_full, dest=f)

print(f"PDF generado en {pdf_path} (errores: {result.err})")
