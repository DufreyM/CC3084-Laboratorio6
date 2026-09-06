# CC3084 - Laboratorio 6: Analisis de redes sociales (YouTube Guatemala)

**Equipo:** Leonardo Mejia, Maria Jose, Mia Fuentes.

Analisis de la estructura de participacion (red bipartita autor-video y sus
proyecciones), contenido y sentimiento de comentarios de YouTube sobre videos
relacionados con Guatemala.

## Entregable principal

**`outputs/informe_final.pdf`** — informe completo con resultados, visualizaciones,
interpretacion y conclusiones (ejercicios 1 a 10). Es la union de los reportes de
cada notebook; para regenerarlo desde cero, correr los notebooks en orden y luego
`notebooks/07_informe_final.py` (ver abajo).

## Estructura del repositorio

```
data/
  youtube_videos.csv, youtube_comments.csv   <- datos crudos (no se modifican)
  processed/                                  <- generado por los notebooks, no editar a mano
    videos_clean.csv, comments_clean.csv, merged_clean.csv
    red_bipartita_nodos.csv, red_bipartita_aristas.csv
    proyeccion_autor_autor.csv, proyeccion_video_video.csv
    centralidad.csv, comments_sentiment.csv, sentimiento_completo.csv
src/
  data_utils.py          <- carga, integracion y limpieza de texto compartida
notebooks/                <- correr en este orden (cada uno depende del anterior)
  01_carga_calidad_leonardo.py           Ejercicios 1 y 2
  02_analisis_exploratorio_mariajose.py  Ejercicio 3
  03_red_bipartita_mia.py                Ejercicio 4
  04_proyecciones_topologia.py           Ejercicios 5 y 6
  05_comunidades_centralidad.py          Ejercicios 7 y 8 (calcula el sentimiento)
  06_sentimiento.py                      Ejercicio 9
  07_informe_final.py                    Ejercicio 10 + ensambla el PDF final
outputs/
  reporte_ejercicio_*.md   <- hallazgos de cada notebook en texto plano
  figs/                    <- todas las visualizaciones (14 figuras, .png)
  informe_final.md / .pdf  <- informe consolidado (entregable)
Laboratorio_6_Analisis_de_redes_sociales_YouTube_2026.pdf   <- enunciado
```

## Como correr el analisis completo

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm   # una sola vez, para lematizacion (ejercicio 2)

python notebooks/01_carga_calidad_leonardo.py
python notebooks/02_analisis_exploratorio_mariajose.py
python notebooks/03_red_bipartita_mia.py
python notebooks/04_proyecciones_topologia.py
python notebooks/05_comunidades_centralidad.py   # descarga el modelo de sentimiento la primera vez
python notebooks/06_sentimiento.py
python notebooks/07_informe_final.py             # genera outputs/informe_final.pdf
```

Cada notebook esta escrito con celdas `# %%` (formato Jupytext/VSCode), asi que
tambien se pueden abrir y correr celda por celda en VSCode o convertir a `.ipynb`.

### Dependencias

Ver `requirements.txt`. Ademas de pandas/numpy/matplotlib/networkx, se usan:
- **nltk** (stopwords en español) y **spacy** (`es_core_news_sm`, lematizacion) para
  la limpieza de texto (ejercicio 2).
- **wordcloud** para la nube de palabras (ejercicio 3).
- **langdetect** para la deteccion de idioma (pregunta adicional del ejercicio 3.6).
- **pysentimiento** (modelo `robertuito-sentiment-analysis`, descarga ~500MB la
  primera vez desde HuggingFace) para el analisis de sentimiento (ejercicios 7 y 9).
- **markdown** y **xhtml2pdf** para ensamblar el informe final en PDF.

Todos los pasos que dependen de internet (descarga de stopwords de NLTK, del
modelo de spaCy y del modelo de pysentimiento) se descargan una sola vez y quedan
en cache local; corridas posteriores no requieren internet.

## Resumen de hallazgos principales

- Solo 19 de 293 videos (6.5%) tienen comentarios en este dataset, y el 93.6% de
  los comentarios se concentra en 10 de esos 19 videos.
- La red autor-video tiene 10 componentes conexos: un componente gigante (286 de
  351 nodos) alrededor del video "Que rico come tu diputado", y 9 videos con
  audiencia totalmente aislada.
- Deteccion de comunidades (Louvain, modularidad 0.777): 17 comunidades, casi
  todas equivalentes a un solo video, salvo una que fusiona 3 videos de
  contenido de consumidor/servicios de Quorum.
- El corpus es 61.3% negativo en sentimiento (pysentimiento/RoBERTuito), salvo el
  video municipal "Plan 2032 Ciudad de Guatemala" (80% positivo, tono
  aspiracional/diaspora), evidencia de que el tono depende del tema del video,
  no de un animo generalizado.
- Limitaciones y alcance de estas conclusiones: ver ejercicio 10 en el informe
  final (`outputs/informe_final.pdf`).

## Flujo de trabajo del equipo

Como compartimos una sola computadora, cada quien programo su parte y la
commiteo con su propio usuario de GitHub (`git config user.name/email` antes de
cada tanda de commits). El historial del repositorio refleja quien hizo cada
parte.

## Enlaces

- Repositorio: https://github.com/DufreyM/CC3084-Laboratorio6
- Espacio colaborativo del grupo: _(pendiente de agregar por el equipo)_
