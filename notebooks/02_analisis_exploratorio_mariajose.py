# %% [markdown]
# # Laboratorio 6 - Ejercicio 3: Analisis exploratorio
# **Autora de esta seccion:** Maria Jose
#
# Partir SIEMPRE de `data/processed/merged_clean.csv` (generado por
# `01_carga_calidad_leonardo.py`), no de los CSV crudos, para que los tres
# analisis del equipo usen exactamente el mismo dataset integrado y limpio
# (con texto_original, texto_limpio, hashtags, mentions, emojis ya calculados).

# %%
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
import matplotlib.pyplot as plt
import data_utils as du

df = pd.read_csv(ROOT / "data" / "processed" / "merged_clean.csv")
videos = pd.read_csv(ROOT / "data" / "processed" / "videos_clean.csv")

# %% [markdown]
# ## 3.1 Descriptivos minimos (pendiente)
# - numero de videos, canales, comentarios, autores unicos
# - videos por canal
# - comentarios y autores unicos por video
# - visualizaciones (view_count), respuestas (reply_count), "me gusta" (like_count)
# - categorias, consultas de busqueda (source_query), hashtags, palabras y bigramas frecuentes
#   (usar `df['texto_limpio']`)

# %% [markdown]
# ## 3.2 Concentracion de la participacion (pendiente)
# Que proporcion de comentarios corresponde a los videos/canales mas activos
# (ej. top 10% de videos por numero de comentarios -> % del total de comentarios).

# %% [markdown]
# ## 3.3 Popularidad vs. participacion (pendiente)
# Relacion entre view_count (por video) y numero de comentarios por video;
# discutir limitaciones de ambos conteos (vistas no implican interaccion,
# comentarios muestreados no son todos los comentarios reales del video).

# %% [markdown]
# ## 3.4 Visualizaciones (pendiente)
# Graficos de frecuencia/comparacion (barras, histogramas). La nube de
# palabras (wordcloud) es un complemento, no el grafico principal.

# %% [markdown]
# ## 3.5 Preguntas obligatorias del enunciado (pendiente)
# Responder con evidencia (numeros/graficos de este mismo notebook):
# - Que videos y canales concentran la mayor participacion observada?
# - Existen audiencias compartidas entre videos, canales o temas?
# - Que autores funcionan como puentes entre contenidos? (se apoya en ejercicio 8)
# - Que temas y sentimientos caracterizan las comunidades? (se apoya en ejercicios 7 y 9)
# - La visibilidad (view_count) coincide con la participacion (comentarios)?
# - Que conclusiones estan limitadas por la recoleccion/cobertura de los datos?

# %% [markdown]
# ## 3.6 Tres preguntas adicionales propias (pendiente)
